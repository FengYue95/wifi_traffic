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
class ShowHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("show.html")

#从location数据表获取AP�?
class GetRoadHandler(tornado.web.RequestHandler):
    def post(self):
        user=get_username_and_password()['user']
        passwd=get_username_and_password()['passwd']
        print "exc"
        try:
            #连接数据�?
            conn = MySQLdb.connect(host='localhost', port=3306, user=user, passwd=passwd, db='traffic_db', cursorclass = MySQLdb.cursors.DictCursor)
            cur = conn.cursor()
            #查询数据�?
            cur.execute("select * from roadnet")
            #获取返回�?
            results = cur.fetchall()
            #解析为json格式
            arr = json.dumps(results)
            self.write(arr)
            conn.close()
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])


class LevelHandler(tornado.web.RequestHandler):
    def post(self):
        url = "http://139.129.110.99:8800/wifitraffic/state_by_uri/all";
        #ִ��URL��ȡ����ֵ
        req = urllib2.Request(url)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        #������ֵ������json��ʽ
        j = json.loads(res)
        self.write(j)


#地址映射
url = [
(r'/show', ShowHandler),
(r'/show/getroad', GetRoadHandler),
(r'/show/level', LevelHandler),
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



define("port", default = 8802, help="run on the given port", type = int)
def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
if __name__ == "__main__":
 main()