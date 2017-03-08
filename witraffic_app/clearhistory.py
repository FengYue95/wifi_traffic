#coding=utf-8
import os
import shutil
from mysql_utils import getsegmentlist
from pymongo import MongoClient as Client
from getpath import get_current_dir

#删除指定文件夹下所有内容的操作，包括非空文件夹
def removedir(rootdir):
    #获得文件夹下的文件列表
    filelist=os.listdir(rootdir)
    #遍历文件列表
    for f in filelist:
        filepath = os.path.join( rootdir, f )
        #如果是文件，则删除文件
        if os.path.isfile(filepath):
            os.remove(filepath)
            print filepath+" removed!"
        #如果是文件夹则整个文件夹删除
        elif os.path.isdir(filepath):
            shutil.rmtree(filepath,True)
            print "dir "+filepath+" removed!"

#清空mongodb数据库
def clearmongodb():
    client=Client()
    db=client.traffic_project
    #清空速度
    db.speed.remove({})
    #清空状态
    db.state.remove({})
    #清空流量
    db.maccount.remove({})
    #清空清空拥堵指数
    db.congestion_index.remove({})
    #清空其他指标数据
    db.traffic_state.remove({})

#主入口
#清楚各路段的旧记录
seglist=getsegmentlist()
for seg in seglist:
    filename=get_current_dir()+"/data/wifiresult/"+str(seg['segmentid'])
    removedir(filename)
    clearmongodb()

