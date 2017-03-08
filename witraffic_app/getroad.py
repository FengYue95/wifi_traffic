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

#璁块棶璺綉鐢熸垚椤甸潰
class ShowHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("show.html")

#浠巐ocation鏁版嵁琛ㄨ幏鍙朅P鐐?
class GetRoadHandler(tornado.web.RequestHandler):
    def post(self):
        user=get_username_and_password()['user']
        passwd=get_username_and_password()['passwd']
        print "exc"
        try:
            #杩炴帴鏁版嵁搴?
            conn = MySQLdb.connect(host='localhost', port=3306, user=user, passwd=passwd, db='traffic_db', cursorclass = MySQLdb.cursors.DictCursor)
            cur = conn.cursor()
            #鏌ヨ鏁版嵁搴?
            cur.execute("select * from roadnet")
            #鑾峰彇杩斿洖鍊?
            results = cur.fetchall()
            #瑙ｆ瀽涓簀son鏍煎紡
            arr = json.dumps(results)
            self.write(arr)
            conn.close()
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])


class LevelHandler(tornado.web.RequestHandler):
    def post(self):
        url = "http://139.129.110.99:8800/wifitraffic/state_by_uri/all";
        #执行URL获取返回值
        req = urllib2.Request(url)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        #将返回值解析成json格式
        j = json.loads(res)
        self.write(j)



class BuptHandler(tornado.web.RequestHandler):
    def post(self):
        url = "http://139.129.110.99:8800/wifitraffic/speed_by_uri/bydate/20160625";
        #执行URL获取返回值
        req = urllib2.Request(url)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        #将返回值解析成json格式
        j = json.loads(res)
        self.write(j)



#鍦板潃鏄犲皠
url = [
(r'/show', ShowHandler),
(r'/show/getroad', GetRoadHandler),
(r'/show/level', LevelHandler),
(r'/show/bupt', BuptHandler),
]
#璁剧疆璺緞
settings = dict(
template_path = os.path.join(os.path.dirname(__file__), "templates"),
static_path = os.path.join(os.path.dirname(__file__), "statics")
)
#閰嶇疆application
application = tornado.web.Application(
handlers = url,
**settings
)



define("port", default = 8802, help="run on the given port", type = int)
def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
if __name__ == "__main__":
 main()