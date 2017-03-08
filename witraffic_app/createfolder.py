#coding=utf-8
import os
from mysql_utils import getsegmentlist
from getpath import get_current_dir

#从数据库读所有需要计算的路段信息
seglist=getsegmentlist()
#轮询路段列表并创建结果输出目录
for seg in seglist:
    print seg
    if not os.path.exists(get_current_dir()+'/data/wifiresult/'+str(seg['segmentid'])):
        os.makedirs(get_current_dir()+'/data/wifiresult/'+str(seg['segmentid']))

