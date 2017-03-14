#coding=utf-8

from isincreasedorder import *
from rssi import *
from history import gethistory
from mysql_utils import *
from traffic_index import *
from mongodb_utils import *
from getProperties import get_update_time_interval
from datamerge import *
from getpath import get_current_dir
from kmeans_sklearn import clusting

import numpy as np
import pandas as pd
import threading
import time
import Queue
import math
import multiprocessing
import os




#由时间戳提取出日期
def timestamp2date(timestamp):
    x = time.localtime(timestamp)
    a= time.strftime('%Y%m%d',x)
    return a

#时间戳转成字符串，格式yyyymmdd-hhMMss
def timestamp2str(timestamp):
    x = time.localtime(timestamp)
    a= time.strftime('%Y/%m/%d-%H:%M:%S',x)
    return a



#数据处理任务
def task(date,current_time,seg,sourcefolder,resultfolder,his_df):

    #从字典seg里提取路段各参数
    startPoint=str(seg['startAPid'])
    endPoint=str(seg['endAPid'])
    segmentid=str(seg['segmentid'])
    distance=seg['dist']
    maxspeed=seg['max_speed']
    line1=seg['line1']
    line2=seg['line2']
    line3=seg['line3']
    line4=seg['line4']

    #如果结果文件还没创建则创建文件
    if not os.path.exists(resultfolder+segmentid):
        os.makedirs(resultfolder+segmentid)

    #候选集时间片长度,当前时刻往前T分钟,最低车速按3km/h,确保最低车速也可通过路段
    T=distance*0.02
    #计算速度用的数据时间片长度t
    t=T
    begintime=current_time-60*T
    endtime=current_time

    #获得路段起始地点包含的所有AP的融合数据集（已经按时间排好序）
    startMacs=getMacListByAPid(startPoint)
    node1_path_list=get_node_path_list(startMacs,sourcefolder,date)
    df_list_1=[]
    for path in node1_path_list:
        df=get_df_by_path(path)
        df_list_1.append(df)
    node1_df=merge_datafeame(df_list_1).sort_values(by=['time'])


    #获得路段终止地点包含的所有AP的融合数据集(已经按时间排好序）
    endMacs=getMacListByAPid(endPoint)
    node2_path_list=get_node_path_list(endMacs,sourcefolder,date)
    df_list_2=[]
    for path in node2_path_list:
        df=get_df_by_path(path)
        df_list_2.append(df)
    node2_df=merge_datafeame(df_list_2).sort_values(by=['time'])


    #截取T分钟的数据量
    node1_df=node1_df[(node1_df.time<endtime)&(node1_df.time>begintime)]
    node2_df=node2_df[(node2_df.time<endtime)&(node2_df.time>begintime)]

    #选出首尾节点共同mac集
    macset=list(set(node1_df.mac).intersection(set(node2_df.mac)))
    output_mac=[]
    output_time=[]
    output_speed=[]
    i=0
    for mac in macset:
        t1=list(node1_df['time'][node1_df.mac==mac])
        t2=list(node2_df['time'][node2_df.mac==mac])
        #判断是否在时间T内在被考察路段来回移动
        if isincreasedorder(t1+t2)or isincreasedorder(t2+t1):
            labeltime1=max(t1)
            labeltime2=min(t2)
            #rssi转距离，距离修正
            rssi1=np.mean(list(node1_df['signal'][node1_df.time==labeltime1]))
            rssi2=np.mean(list(node2_df['signal'][node2_df.time==labeltime2]))
            dist1=rssi2dist(rssi1)
            dist2=rssi2dist(rssi2)

            output_mac.append(mac)
            output_time.append(int(np.mean([labeltime1,labeltime2])))
            #计算各个mac平均速度
            delta_t=(labeltime2-labeltime1)
            #speed单位km/h, 3.6是由m/min转km/h的准换因素
            speed=3.6*(distance+dist2-dist1)/delta_t
            output_speed.append(speed)
            i=i+1

    #如果没有捕捉到mac的情况
    if i==0:
        return [None,endtime,0,5,0.0]


    #经过两点的mac信息
    middle_df=pd.DataFrame({'mac':output_mac,'speed':output_speed,'time':output_time})
    #速度过滤阈值
    min_speed_limit=0
    max_speed_limit=maxspeed
    #速度过滤
    middle_df=middle_df[(middle_df.speed>=min_speed_limit)&(middle_df.speed<=max_speed_limit)]
    #统计T分钟内速度正常的mac数
    mac_count=len(middle_df.mac)
    #截取近10分钟
    middle_df=middle_df[(middle_df.time>=endtime-t*60)&(middle_df.time<=endtime)]
    # print '当前十分钟速度数据'
    # print(middle_df)
    #将当前速度写入文件，以逗号隔开，去掉行索引，不带列名写入
    middle_df.to_csv(resultfolder+segmentid+'/'+str(endtime),sep=',',index=None,header=None)



    #把当前数据也添加到历史数据里，保证在历史数据框里能找到当前每一个mac

    new_his_df=pd.concat([his_df,middle_df],ignore_index=True)
    new_his_df=new_his_df.drop('time',axis=1)
    print "去重前历史条数"+str(len(new_his_df))
    new_his_df= new_his_df.drop_duplicates()
    new_his_df=new_his_df.sort_values(by=['mac'])
    print "去重后历史条数"+str(len(new_his_df))
    #历史数据统计
    his_var=[]
    his_mean=[]
    his_len=[]
    #针对当前测到的所有mac，求其历史均值方差和历史样本大小
    for mac in middle_df.mac:
        mac_his_speed=list(new_his_df['speed'][new_his_df.mac==mac])
        his_var.append("%.3f" % np.var(mac_his_speed))
        his_mean.append("%.3f" % np.mean(mac_his_speed))
        his_len.append(len(mac_his_speed))
    #历史统计数据
    statistic_df=pd.DataFrame({'mac':middle_df.mac,'current_speed':middle_df.speed,'his_var':his_var,'his_mean':his_mean,'his_len':his_len,'segid':segmentid})
    statistic_df=statistic_df.sort_values(by=['mac'])
    #历史统计数据写入对应路段文件夹下
    statistic_df.to_csv(resultfolder+segmentid+'/'+'history_statistic_'+str(endtime),sep='|',index=None,header=None)

    #聚类结果
    target_mac_set=clusting(resultfolder+segmentid+'/'+'history_statistic_'+str(endtime))
    #提取目标mac的记录
    middle_df=middle_df[middle_df.mac.isin(target_mac_set)]


    #路段速度确定
    #如果mac少于10个，取平均速度和最高限速的折中值，否则取平均速度
    if mac_count<10:
        speed_result=(maxspeed+np.mean(middle_df.speed))/2.0
    else:
        speed_result=np.mean(middle_df.speed)
    #如果求出来的速度>最大限速，取最大限速
    if speed_result>maxspeed:
        speed_result=maxspeed

    #路段拥堵评定，数字越高越畅通
    #共5级
    if mac_count<=5:
        state=5
    elif speed_result>line4:
        state=5
    elif speed_result>line3:
        state=4
    elif speed_result>line2:
        state=3
    elif speed_result>line1:
        state=2
    else:
        state=1

    segment_index=10.0*(maxspeed-speed_result)/maxspeed


    result=[speed_result,endtime,mac_count,state,segment_index]
    print result
    return result

#分块
def separation(size,block_size):
    block_q=Queue.Queue()
    block_count=int(math.ceil(float(size)/block_size));
    print "总共要计算"+str(size)+"个路段，每个子线程负责计算"+str(block_size)+"个路段，共分"+str(block_count)+"个子线程"

    lask_start=block_size*(size/block_size)
    lastblock={'start':lask_start,'end':size-1}


    end=block_size-1
    while end<size:
        block={'start':end-block_size+1,'end':end}
        block_q.put(block)
        end+=block_size
    if lask_start<size:
        block_q.put(lastblock)
    return block_q



#子线程
def sonthread(input):

    m_dict={}
    s_dict={}
    state_dict={}
    congestion_index_dict={}

    date=input['date']
    current_time=input['current_time']
    sourcefolder=input['sourcefolder']
    resultfolder=input['resultfolder']
    subseglist=input['seglist']
    his_df=input['history']

    for seg in subseglist:
        print "计算路段"+str(seg['segmentid'])
        taskresult=task(date,current_time,seg,sourcefolder,resultfolder,his_df)
        #由task返回结果拼sql语句
        m_dict[str(seg['segmentid'])]=taskresult[2]


        if taskresult[0] is None or str(taskresult[0])=="nan":
            s_dict[str(seg['segmentid'])]=seg['max_speed']
            congestion_index_dict[str(seg['segmentid'])]=0.0
        else :
            s_dict[str(seg['segmentid'])]=taskresult[0]
            congestion_index_dict[str(seg['segmentid'])]=taskresult[4]

        state_dict[str(seg['segmentid'])]=taskresult[3]

    #子线程结果
    sonthread_result= [m_dict,s_dict,state_dict,congestion_index_dict]
    return sonthread_result



#调度父线程
def fatherthread():
    #测试数据开始时间
    test_begin_time=1477843200
    #测试数据总时长
    test_time_long=24
    #模拟测试数据单前时间
    delta=int(time.time())-test_begin_time
    current_time=int(time.time())-delta
    #当前日期，格式yyyymmdd
    date=timestamp2date(current_time)
    #探针数据目录
    sourcefolder=get_current_dir()+"/WiFiData/"
    #数据处理结果存放目录
    resultfolder=get_current_dir()+"/data/wifiresult/"

    print "程序启动日期："+date
    print "程序启动时间："+timestamp2str(current_time)



    #循环执行计算任务，每5分钟计算一次，知道指定时间停止
    while current_time<=(test_begin_time+test_time_long*3600):
        print "当前时间："+timestamp2str(current_time)

        timestr=time.strftime('%Y%m%d%H%M%S',time.localtime(current_time))

        speed_d={'time':timestr}
        mac_d={'time':timestr}
        state_d={'time':timestr}
        congestion_index_d={'time':timestr}
        #获取历史速度数据(不含当前)
        his_df=gethistory(current_time,resultfolder)


        #耗时计算的起始时刻
        start_time=time.time()
        #任务分块,确定各个子线程的输入参数
        inputs=[]
        #从数据库获得路段列表
        segmentlist=getsegmentlist()

        #任务切割与分配
        block_q = separation(len(segmentlist),90)
        while not block_q.empty():
            block = block_q.get()
            start=block.get('start')
            end=block.get('end')
            inputs.append({'seglist':segmentlist[start:end+1],'date':date,'current_time':current_time,'sourcefolder':sourcefolder,'resultfolder':resultfolder,'history':his_df})


        #使用multiprocessing并行进程池来并行处理任务，充分利用cup资源

        #确定进程池大小
        pool_size=multiprocessing.cpu_count()*2
        print "进程数"+str(pool_size)
        # 初始化线程池
        pool=multiprocessing.Pool(processes=pool_size,initializer=start_process,maxtasksperchild=2)
        # 获得各子线程的返回结果，存在列表final_result里
        final_result=pool.map(sonthread, inputs,)
        #关闭进程池，阻止其他进程进入，等待各个任务完成
        pool.close()
        #将进程池join到父线程里
        pool.join()
        pool.terminate()


        #父线程在所有子线程结束后，把结果取出来整合
        for list in final_result:
            mac_d=dict(mac_d,**list[0])
            speed_d=dict(speed_d,**list[1])
            state_d=dict(state_d,**list[2])
            congestion_index_d=dict(congestion_index_d,**list[3])

        # mac_d=sorted(mac_d.iteritems(),key=lambda d:d[0])
        # speed_d=sorted(speed_d.iteritems(),key=lambda d:d[0])
        # state_d=sorted(state_d.iteritems(),key=lambda d:d[0])
        # congestion_index_d=sorted(congestion_index_d.iteritems(),key=lambda d:d[0])

        #插入速度，流量，拥堵状态数据
        print speed_d
        print mac_d
        print state_d
        print congestion_index_d



        #车流量
        insert_maccount(mac_d)
        #速度
        insert_speed(speed_d)
        #状态
        insert_state(state_d)
        #拥堵指数
        insert_congestion_index(congestion_index_d)


        #交通指数
        traffic_index=get_traffic_index(timestr)
        #路网拥堵比率
        congrestion_rate=get_congrestion_rate(timestr)

        traffic_state_dict={'time':timestr,'traffic_index':traffic_index,'congrestion_rate':congrestion_rate}

        #区域交通指数
        area_name=getAreas()
        for area in area_name:
            area_dict={area:get_traffic_index_of_area(timestr,area)}
            traffic_state_dict=dict(traffic_state_dict,**area_dict)

        print traffic_state_dict
        #交通状态指标插入数据库
        insert_traffic_state(traffic_state_dict)

        #标记耗时
        time_cost=time.time()-start_time
        print "用时"+str(time_cost)
        #线程休眠，
        # 休眠间隔与更新周期相关
        sleeptime=get_update_time_interval()['update_time']-time_cost
        if sleeptime<0:
            sleeptime=0
        time.sleep(sleeptime)
        #更新当前时间
        current_time=current_time+get_update_time_interval()['update_time']



def start_process():
      print 'Starting',multiprocessing.current_process().name

if __name__ == '__main__':
    father_t=threading.Thread(target=fatherthread,args=())
    #将父线程设为守护线程
    father_t.setDaemon(True)
    #启动父线程
    father_t.start()
    #主线程要等待父线程执行完才退出
    father_t.join()
    print "测试结束"

