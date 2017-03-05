#coding=utf-8
import os
import shutil
from mysql_utils import getsegmentlist
from pymongo import MongoClient as Client


def removedir(rootdir):

    filelist=os.listdir(rootdir)
    for f in filelist:
        filepath = os.path.join( rootdir, f )
        if os.path.isfile(filepath):
            os.remove(filepath)
            print filepath+" removed!"
        elif os.path.isdir(filepath):
            shutil.rmtree(filepath,True)
            print "dir "+filepath+" removed!"

def clearmongodb():
    client=Client()
    db=client.traffic_project
    db.speed.remove({})
    db.state.remove({})
    db.maccount.remove({})
    db.congestion_index.remove({})
    db.traffic_state.remove({})


seglist=getsegmentlist()
for seg in seglist:
    filename=os.path.abspath('.')+"/data/wifiresult/"+str(seg['segmentid'])
    removedir(filename)
    clearmongodb()

