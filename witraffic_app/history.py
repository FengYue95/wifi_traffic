#coding=utf-8
import pandas
import os
import re


#从开头开始进行正则匹配
def get_re_file_list(file_list,re_rule):
    file_list_re=[]
    for file in file_list:
        if re.match(re_rule,file):
            file_list_re.append(file)
    return file_list_re

#从历史数据集里获取给定mac对应的历史数据
def gethistoryByMAC(target_mac,history_df):
    return history_df['mac','speed'][history_df.mac==target_mac]

#获取当前时间分片里的所有mac的历史数据
def gethistory(timestamp,rootpath):
    files=os.listdir(rootpath)
    allfl=[]
    for segid in files:
        #获得各路段文件夹下历史数据文件列表
        fl=get_re_file_list(os.listdir(rootpath+segid+'/'),r'1')
        fl=map(int,fl)
        fl=[rootpath+segid+'/'+str(i) for i in fl if (i>=timestamp-3600) and (i<=timestamp)]
        allfl=allfl+fl
    allfl.sort()
    print allfl
    history_df=pandas.DataFrame()
    for filename in allfl:
        if os.path.getsize(filename)==0:
            print filename+'is empty file'
            continue
        temp_df=pandas.read_table(filename,names=['mac','speed','time'],sep=',',header=None)
        history_df=pandas.concat([history_df,temp_df],ignore_index=True)
    return history_df




