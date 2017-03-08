#coding=utf-8

from pymongo import MongoClient as Client
import time



def timestamp2str(timestamp):
    x = time.localtime(timestamp)
    a= time.strftime('%Y/%m/%d-%H:%M:%S',x)
    return a

def insert_speed(speed_dict):
    #连接MongoClient
    client=Client()   #为空则为默认设置 （'localhost',27017）
    #连接数据库
    db=client.traffic_project  #如果存在则连接，不存在则创建
    #连接聚集（collection） 相当于关系型数据库里的表
    speed=db.speed  #如果存在连接，不存在创建
    #插入数据
    speed.insert(speed_dict)

def insert_maccount(maccount_dict):
    #连接MongoClient
    client=Client()   #为空则为默认设置 （'localhost',27017）
    #连接数据库
    db=client.traffic_project  #如果存在则连接，不存在则创建
    #连接聚集（collection） 相当于关系型数据库里的表
    maccount=db.maccount  #如果存在连接，不存在创建
    #插入数据
    maccount.insert(maccount_dict)

def insert_state(state_dict):
    #连接MongoClient
    client=Client()   #为空则为默认设置 （'localhost',27017）
    #连接数据库
    db=client.traffic_project  #如果存在则连接，不存在则创建
    #连接聚集（collection） 相当于关系型数据库里的表
    state=db.state  #如果存在连接，不存在创建
    #插入数据
    state.insert(state_dict)

def insert_congestion_index(congestion_index_dict):
    #连接MongoClient
    client=Client()   #为空则为默认设置 （'localhost',27017）
    #连接数据库
    db=client.traffic_project  #如果存在则连接，不存在则创建
    #连接聚集（collection） 相当于关系型数据库里的表
    congestion_index=db.congestion_index  #如果存在连接，不存在创建
    #插入数据
    congestion_index.insert(congestion_index_dict)

def insert_traffic_state(traffic_state_dict):
    #连接MongoClient
    client=Client()   #为空则为默认设置 （'localhost',27017）
    #连接数据库
    db=client.traffic_project  #如果存在则连接，不存在则创建
    #连接聚集（collection） 相当于关系型数据库里的表
    traffic_state=db.traffic_state  #如果存在连接，不存在创建
    #插入数据
    traffic_state.insert(traffic_state_dict)


def getspeed(timestr):
     #连接MongoClient
    client=Client()   #为空则为默认设置 （'localhost',27017）
    #连接数据库
    db=client.traffic_project  #如果存在则连接，不存在则创建
    #有时间获得速度记录
    result=db.speed.find({'time':timestr})
    return result[0]

def getstate(timestr):
    #连接MongoClient
    client=Client()   #为空则为默认设置 （'localhost',27017）
    #连接数据库
    db=client.traffic_project  #如果存在则连接，不存在则创建
    #由时间获得拥堵等级记录
    result=db.state.find({'time':timestr})
    return result[0]








