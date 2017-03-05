#!/usr/bin/env python
# coding=utf-8
import tornado.web
import os
import sys
import urllib2
import json
import MySQLdb
import MySQLdb.cursors
import random
import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.options import define, options
from getProperties import get_username_and_password

reload(sys)
sys.setdefaultencoding("utf-8")

#访问路网生成页面
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("createRoadnet.html")

#获取距离的函�?
class DistanceHandler(tornado.web.RequestHandler):
    def post(self):
        #获取城市�?
        city = self.get_argument("city")
        #获取起点经纬�?
        slat = self.get_argument("slat")
        slng = self.get_argument("slng")
        #获取终点经纬�?
        elat = self.get_argument("elat")
        elng = self.get_argument("elng")
        #百度地图获取距离提供的URL
        url = "http://api.map.baidu.com/direction/v1?mode=driving&origin="+slat+","+slng+"&destination="+elat+","+elng+\
              "&origin_region="+city+"&destination_region="+city+"&output=json&ak=Q3iFU5VmCqgB35gVUYi94UkQH1TwMhpx";
        #执行URL获取返回�?
        req = urllib2.Request(url)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        #将返回值解析成json格式
        j = json.loads(res)
        #获取距离
        a=j["result"]["routes"][0]["distance"]
        #获取反向的距�?
        url1 = "http://api.map.baidu.com/direction/v1?mode=driving&origin=" + elat + "," + elng + "&destination=" + slat + "," + slng + \
              "&origin_region=" + city + "&destination_region=" + city + "&output=json&ak=Q3iFU5VmCqgB35gVUYi94UkQH1TwMhpx";
        req1 = urllib2.Request(url1)
        res_data1 = urllib2.urlopen(req1)
        res1 = res_data1.read()
        j1 = json.loads(res1)
        b= j1["result"]["routes"][0]["distance"]
        mark=j["result"]["routes"][0]["steps"][0]["path"]
        arr=mark.split(";")
        a1=len(arr)
        mark1=j1["result"]["routes"][0]["steps"][0]["path"]
        arr1=mark1.split(";")
        b1=len(arr1)
        #将正向和反向距离进行比较，确定�?�点和终�?
        if a1<b1:
              c=a
              type=1
        else:
              c=b
              type=0
        if c > 3000:
              c = random.randint(1000, 2000)
              self.write(str(c)+";"+str(type))
        else:
              self.write(str(c)+";"+str(type))


#从location数据表获取AP�?
class LocationHandler(tornado.web.RequestHandler):
    def post(self):
        user=get_username_and_password()['user']
        passwd=get_username_and_password()['passwd']
        print "exc"
        try:
            #连接数据�?
            conn = MySQLdb.connect(host='localhost', port=3306, user=user, passwd=passwd, db='traffic_db', cursorclass = MySQLdb.cursors.DictCursor)
            cur = conn.cursor()
            #查询数据�?
            cur.execute("select * from location")
            #获取返回�?
            results = cur.fetchall()
            #解析为json格式
            arr = json.dumps(results)
            self.write(arr)
            conn.close()
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

#将路网写入数据库
class SqlHandler(tornado.web.RequestHandler):
    def post(self):
        #接收路网数据
        data1 = self.get_argument("rr")
        data=json.loads(data1)
        length=len(data)
        user=get_username_and_password()['user']
        passwd=get_username_and_password()['passwd']
        #循环迭代每条路段的数�?
        for i in range(0,length,1):
            #起点ap
            sap =data[i]["sap"]
            #终点ap
            eap =data[i]["eap"]
            #起点经纬�?
            sposition =data[i]["sposition"]
            #终点经纬�?
            eposition =data[i]["eposition"]
            #路段�?
            name =data[i]["name"]
            #区域�?
            area =data[i]["area"]
            #道路等级
            level =data[i]["level"]
            #道路长度
            dist =data[i]["length"]
            #最大限�?
            maxspeed =data[i]["maxspeed"]
            #速度等级
            line1 =data[i]["line1"]
            line2 =data[i]["line2"]
            line3 =data[i]["line3"]
            line4 =data[i]["line4"]


            try:
                #连接数据�?
                conn = MySQLdb.connect(host='localhost', port=3306, user=user, passwd=passwd, db='traffic_db', charset="utf8")
                cur = conn.cursor()
                #若表不存在则建表
                cur.execute("CREATE TABLE IF NOT EXISTS roadnet (segmentid int(11) AUTO_INCREMENT NOT NULL,"
                            "startAPid int(11) NOT NULL,"
                            "endAPid int(11) NOT NULL,"
                            "dist int(11) NOT NULL,"
                            "level int(11) NOT NULL,"
                            "max_speed double NOT NULL,"
                            "line1 double NOT NULL,"
                            "line2 double NOT NULL,"
                            "line3 double NOT NULL,"
                            "line4 double NOT NULL,"
                            "area varchar(10) DEFAULT NULL,"
                            "sposition varchar(50) DEFAULT NULL,"
                            "eposition varchar(50) DEFAULT NULL,"
                            "name char(20) DEFAULT NULL,"
                            "PRIMARY KEY (segmentid))"
                            "ENGINE=InnoDB DEFAULT CHARSET=utf8");
                conn.commit()
                #查询是否已经存在记录，如果存在则覆盖旧的记录
                count=cur.execute("select * from roadnet where startAPid="+sap+" and endAPid="+eap)
                conn.commit()
                #判断某条记录是否重复插入
                if count>=1:
                    sql="UPDATE roadnet SET dist=%s,level=%s,max_speed=%s,line1=%s,line2=%s,line3=%s,line4=%s,area=%s,sposition=%s,eposition=%s,name=%s where startAPid=%s and endAPid=%s"
                    cur.execute(sql,(dist,level,maxspeed,line1,line2,line3,line4,area,sposition,eposition,name,sap,eap))
                    cur.close()
                    conn.commit()
                    conn.close()
                else:
                    sql="INSERT INTO roadnet (startAPid, endAPid, dist, level, max_speed, line1, line2, line3, line4, area, sposition, eposition, name) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cur.execute(sql,(sap,eap,dist,level,maxspeed,line1,line2,line3,line4,area,sposition,eposition,name))
                    cur.close()
                    conn.commit()
                    conn.close()
                self.write("success")
            except MySQLdb.Error,e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])

#获取区域�?
class GetAreaHandler(tornado.web.RequestHandler):
    def post(self):
        lat = self.get_argument("elat")
        lng = self.get_argument("elng")
        #百度地图提供的获取区域名称的URL
        url = "http://api.map.baidu.com/geocoder/v2/?location="+lat+","+lng+"&output=json&pois=1&ak=Q3iFU5VmCqgB35gVUYi94UkQH1TwMhpx"
        req = urllib2.Request(url)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        self.write(res)
#地址映射
url = [
(r'/createRoadnet', IndexHandler),
(r'/createRoadnet/getArea', GetAreaHandler),
(r'/createRoadnet/distance', DistanceHandler),
(r'/createRoadnet/location', LocationHandler),
(r'/createRoadnet/sql', SqlHandler),
]
#设置路径
settings = dict(
template_path = os.path.join(os.path.dirname(__file__), "templates"),
static_path = os.path.join(os.path.dirname(__file__), "statics")
)
#配置application
application = tornado.web.Application(
handlers = url,
**settings
)



define("port", default = 8801, help="run on the given port", type = int)
def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
if __name__ == "__main__":
 main()