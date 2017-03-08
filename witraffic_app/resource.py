#coding=utf-8
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from pymongo import MongoClient as Client
import re
import json



define("port", default=8800, help="run on the given port", type=int)
#速度
class SpeedHandler_for_URI(tornado.web.RequestHandler):
    #连接MongoClient
    client=Client()   #为空则为默认设置 （'localhost',27017）
    #连接数据库
    db=client.traffic_project #如果存在则连接，不存在则创建
    #连接聚集（collection） 相当于关系型数据库里的表
    collection=db.speed  #如果存在连接，不存在创建
    #get方法
    def get(self, input):
        if input =='all':
            resultset=SpeedHandler_for_URI.collection.find()
        else:
             resultset=SpeedHandler_for_URI.collection.find({},{input:1,'time':1})
        result= resultset[resultset.count()-1]
        if not input=='all' and not result.has_key(input):
            print input+' is not exist!'
            self.write(u'路段id: "'+input+u'" 不存在')
        else:
            del result['_id']
            jsonstr=json.dumps(result)
            self.write(jsonstr)

# 全天速度
class SpeedHandler_for_WholeDay(tornado.web.RequestHandler):
    #连接MongoClient
    client=Client()   #为空则为默认设置 （'localhost',27017）
    #连接数据库
    db=client.traffic_project #如果存在则连接，不存在则创建
    #连接聚集（collection） 相当于关系型数据库里的表
    collection=db.speed  #如果存在连接，不存在创建
    #get方法
    def get(self, input):
         print input
         resultset=SpeedHandler_for_WholeDay.collection.find({'time':re.compile(input)})
         list=[]
         for result in resultset:
             del result['_id']
             list.append(result)
         dict={'history':list}
         string=json.dumps(dict)
         self.write(string)




#车流量
class MaccountHandler_for_URI(tornado.web.RequestHandler):
    #连接MongoClient
    client=Client()   #为空则为默认设置 （'localhost',27017）
    #连接数据库
    db=client.traffic_project #如果存在则连接，不存在则创建
    #连接聚集（collection） 相当于关系型数据库里的表
    collection=db.maccount  #如果存在连接，不存在创建
    #get方法
    def get(self, input):
        if input =='all':
            resultset=MaccountHandler_for_URI.collection.find()
        else:
             resultset=MaccountHandler_for_URI.collection.find({},{input:1,'time':1})
        result= resultset[resultset.count()-1]
        if not input=='all' and not result.has_key(input):
            print input+' is not exist!'
            self.write(u'路段id: "'+input+u'" 不存在')
        else:
            del result['_id']
            jsonstr=json.dumps(result)
            self.write(jsonstr)

# 全天车流量
class MaccountHandler_for_WholeDay(tornado.web.RequestHandler):
    #连接MongoClient
    client=Client()   #为空则为默认设置 （'localhost',27017）
    #连接数据库
    db=client.traffic_project #如果存在则连接，不存在则创建
    #连接聚集（collection） 相当于关系型数据库里的表
    collection=db.maccount  #如果存在连接，不存在创建
    #get方法
    def get(self, input):
         print input
         resultset=MaccountHandler_for_WholeDay.collection.find({'time':re.compile(input)})
         list=[]
         for result in resultset:
             del result['_id']
             list.append(result)
         dict={'history':list}
         string=json.dumps(dict)
         self.write(string)

#拥堵等级
class StateHandler_for_URI(tornado.web.RequestHandler):
    #连接MongoClient
    client=Client()   #为空则为默认设置 （'localhost',27017）
    #连接数据库
    db=client.traffic_project #如果存在则连接，不存在则创建
    #连接聚集（collection） 相当于关系型数据库里的表
    collection=db.state  #如果存在连接，不存在创建
    #get方法
    def get(self, input):
        if input =='all':
            resultset= StateHandler_for_URI.collection.find()
        else:
             resultset= StateHandler_for_URI.collection.find({},{input:1,'time':1})
        result= resultset[resultset.count()-1]
        if not input=='all' and not result.has_key(input):
            print input+' is not exist!'
            self.write(u'路段id: "'+input+u'" 不存在')
        else:
            del result['_id']
            jsonstr=json.dumps(result)
            self.write(jsonstr)

#拥堵指数
class CongestionIndexHandler_for_URI(tornado.web.RequestHandler):
    #连接MongoClient
    client=Client()   #为空则为默认设置 （'localhost',27017）
    #连接数据库
    db=client.traffic_project #如果存在则连接，不存在则创建
    #连接聚集（collection） 相当于关系型数据库里的表
    collection=db.congestion_index  #如果存在连接，不存在创建
    #get方法
    def get(self, input):
        if input =='all':
            resultset= CongestionIndexHandler_for_URI.collection.find()
        else:
             resultset= CongestionIndexHandler_for_URI.collection.find({},{input:1,'time':1})
        result= resultset[resultset.count()-1]
        if not input=='all' and not result.has_key(input):
            print input+' is not exist!'
            self.write(u'路段id: "'+input+u'" 不存在')
        else:
            del result['_id']
            jsonstr=json.dumps(result)
            self.write(jsonstr)

#全路网交通指数
class TrafficIndexHandler_for_URI(tornado.web.RequestHandler):
    #连接MongoClient
    client=Client()   #为空则为默认设置 （'localhost',27017）
    #连接数据库
    db=client.traffic_project #如果存在则连接，不存在则创建
    #连接聚集（collection） 相当于关系型数据库里的表
    collection=db.traffic_state  #如果存在连接，不存在创建
    #get方法
    def get(self):
        resultset= TrafficIndexHandler_for_URI.collection.find({},{'traffic_index':1,'time':1})
        result= resultset[resultset.count()-1]
        del result['_id']
        jsonstr=json.dumps(result)
        self.write(jsonstr)

# 全天全路网交通指数
class TrafficIndexHandler_for_WholeDay(tornado.web.RequestHandler):
    #连接MongoClient
    client=Client()   #为空则为默认设置 （'localhost',27017）
    #连接数据库
    db=client.traffic_project #如果存在则连接，不存在则创建
    #连接聚集（collection） 相当于关系型数据库里的表
    collection=db.traffic_state  #如果存在连接，不存在创建
    #get方法
    def get(self, input):
         print input
         resultset=TrafficIndexHandler_for_WholeDay.collection.find({'time':re.compile(input)},{'traffic_index':1,'time':1})

         list=[]
         for result in resultset:
             del result['_id']
             list.append(result)
         dict={'history':list}
         string=json.dumps(dict)
         self.write(string)

#全路网拥堵里程比例
class CongestionRateHandler_for_URI(tornado.web.RequestHandler):
    #连接MongoClient
    client=Client()   #为空则为默认设置 （'localhost',27017）
    #连接数据库
    db=client.traffic_project #如果存在则连接，不存在则创建
    #连接聚集（collection） 相当于关系型数据库里的表
    collection=db.traffic_state  #如果存在连接，不存在创建
    #get方法
    def get(self):
        resultset= CongestionRateHandler_for_URI.collection.find({},{'congrestion_rate':1,'time':1})
        result= resultset[resultset.count()-1]
        del result['_id']
        jsonstr=json.dumps(result)
        self.write(jsonstr)


#区域交通指数
class AreaIndexHandler_for_URI(tornado.web.RequestHandler):
    #连接MongoClient
    client=Client()   #为空则为默认设置 （'localhost',27017）
    #连接数据库
    db=client.traffic_project #如果存在则连接，不存在则创建
    #连接聚集（collection） 相当于关系型数据库里的表
    collection=db.traffic_state  #如果存在连接，不存在创建
    #get方法
    def get(self, input):
        print input
        if input =='all':
            resultset= AreaIndexHandler_for_URI.collection.find()
        else:
             resultset= AreaIndexHandler_for_URI.collection.find({},{input:1,'time':1})
        result= resultset[resultset.count()-1]
        if not input=='all' and not result.has_key(input):
            print input+' is not exist!'
            self.write(u'区域名称: "'+input+u'" 不存在')
        else:
            del result['_id']
            if result.has_key('traffic_index'):del result['traffic_index']
            if result.has_key('congrestion_rate'):del result['congrestion_rate']
            jsonstr=json.dumps(result)
            self.write(jsonstr)



class SpeedHandler(tornado.web.RequestHandler):
     #连接MongoClient
    client=Client()   #为空则为默认设置 （'localhost',27017）
    #连接数据库
    db=client.traffic_project #如果存在则连接，不存在则创建
    #连接聚集（collection） 相当于关系型数据库里的表
    collection=db.speed  #如果存在连接，不存在创建
    #post方法

    def post(self):
        segmentid = self.get_argument('segmentid','all')
        callback=self.get_argument('callback')
        print segmentid
        if segmentid =='all':
            resultset=SpeedHandler.collection.find()
        else:
             resultset=SpeedHandler.collection.find({},{segmentid:1,'time':1})
        result= resultset[resultset.count()-1]
        if not segmentid=='all' and not result.has_key(segmentid):
            print segmentid+' is not exist!'
            self.write(u'路段id: "'+segmentid+u'" 不存在')
        else:
            del result['_id']
            jsonstr=json.dumps(result)
            self.write(str(callback)+'('+jsonstr+');')

    #get方法
    def get(self):
        segmentid = self.get_argument('segmentid','all')
        callback=self.get_argument('callback','')
        print segmentid
        if segmentid =='all':
            resultset=SpeedHandler.collection.find()
        else:
             resultset=SpeedHandler.collection.find({},{segmentid:1,'time':1})
        result= resultset[resultset.count()-1]
        if not segmentid=='all' and not result.has_key(segmentid):
            print segmentid+' is not exist!'
            self.write(str(callback)+'('+u'路段id: "'+segmentid+u'" 不存在'+');')
        else:
            del result['_id']
            jsonstr=json.dumps(result)
            self.write(callback+'(['+jsonstr+']);')



if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/wifitraffic/speed",SpeedHandler),
            (r"/wifitraffic/speed_by_uri/(\w+)", SpeedHandler_for_URI),
            (r"/wifitraffic/maccount_by_uri/(\w+)",MaccountHandler_for_URI),
            (r"/wifitraffic/state_by_uri/(\w+)", StateHandler_for_URI),
            (r"/wifitraffic/congestion_index_by_uri/(\w+)",CongestionIndexHandler_for_URI),
            (r"/wifitraffic/traffic_state_by_uri/traffic_index",TrafficIndexHandler_for_URI),
            (r'/wifitraffic/traffic_state_by_uri/congestion_rate',CongestionRateHandler_for_URI),
            (r'/wifitraffic/traffic_state_by_uri/area_traffic_index/(\w+)',AreaIndexHandler_for_URI),
            (r"/wifitraffic/speed_by_uri/bydate/(\w+)",SpeedHandler_for_WholeDay),
            (r"/wifitraffic/maccount_by_uri/bydate/(\w+)",MaccountHandler_for_WholeDay),
            (r"/wifitraffic/traffic_state_by_uri/traffic_index/bydate/(\w+)",TrafficIndexHandler_for_WholeDay),

        ]
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


