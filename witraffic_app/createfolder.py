#coding=utf-8
import os
from mysql_utils import getsegmentlist
from getpath import get_current_dir

seglist=getsegmentlist()

for seg in seglist:
    print seg
    if not os.path.exists(get_current_dir()+'/data/wifiresult/'+str(seg['segmentid'])):
        os.makedirs(get_current_dir()+'/data/wifiresult/'+str(seg['segmentid']))

