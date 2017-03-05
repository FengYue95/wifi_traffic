#coding=utf-8
import mysql_utils as mqu
import mongodb_utils as mongo



#求全路网拥堵路长比例
def get_congrestion_rate(timestr):
    print "get_congrestion_rate"
    seglist=mqu.getsegmentlist()
    state=mongo.getstate(timestr)
    sum_len=0.0
    congestion_len=0.0
    for seg in seglist:
        seg_state=state[str(seg['segmentid'])]
        seg_len=seg['dist']
        if seg_state==1:
            congestion_len+=seg_len
        sum_len+=seg_len
    congestion_rate=congestion_len/sum_len
    return congestion_rate

#求全路网交通拥堵指数
def get_traffic_index(timestr):
    print "get_traffic_index"
    seglist=mqu.getsegmentlist()
    realspeedlist=mongo.getspeed(timestr)

    sum_len=0.0
    sum_index=0.0
    for seg in seglist:
        seg_len=seg['dist']
        seg_index=get_segment_index(realspeedlist,seg)

        sum_index+=seg_len*seg_index
        sum_len+=seg_len
    traffic_index=sum_index/sum_len
    return traffic_index

#求区域分块路网交通拥堵指数
def get_traffic_index_of_area(timestr,area):
    print "get_traffic_index_of_area "+area
    seglist=mqu.get_segmentlist_of_area(area)
    realspeedlist=mongo.getspeed(timestr)
    sum_len=0.001
    sum_index=0.0
    for seg in seglist:

        seg_len=seg['dist']
        seg_index=get_segment_index(realspeedlist,seg)

        sum_index+=seg_len*seg_index
        sum_len+=seg_len
    traffic_index=sum_index/sum_len
    return traffic_index


#求某段路拥堵指数
def get_segment_index(realspeedlist,seg):
    print realspeedlist[str(seg['segmentid'])]
    realspeed=realspeedlist[str(seg['segmentid'])]
    maxspeed=seg['max_speed']
    segment_index=10*(maxspeed-realspeed)/maxspeed
    return segment_index