#coding=utf-8
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from getProperties import get_username_and_password
import MySQLdb





define("port", default=8900, help="run on the given port", type=int)

class Loaction_Handler(tornado.web.RequestHandler):

     def post(self):
        #从手机端报文里获取mac，lon，lat参量
        mac = str(self.get_argument('mac'))
        lon=str(self.get_argument('lon'))
        lat=str(self.get_argument('lat'))
        #插入数据库并获取返回
        response=uploadlocation(mac,lon,lat)

        print response
        self.write(str(response))






#上载数据到数据库
def uploadlocation(mac,lon,lat):
    try:
       user=get_username_and_password()['user']
       passwd=get_username_and_password()['passwd']
       # 打开数据库连接
       conn=MySQLdb.connect(host='localhost',user=user,passwd=passwd,port=3306)
       # 使用cursor()方法获取操作游标
       cursor = conn.cursor()
       #如果数据库不存在，则创建数据库
       cursor.execute("create database if not exists traffic_db")
       conn.select_db('traffic_db')
       #若表不存在则建表
       cursor.execute("CREATE TABLE IF NOT EXISTS location(num INTEGER NOT NULL AUTO_INCREMENT,lon DOUBLE NOT NULL,lat DOUBLE NOT NULL,mac CHAR(12) NOT NULL UNIQUE,PRIMARY KEY (num))")
       conn.commit()

       #查询数据库里是否已经存在该探针记录
       recordcount=cursor.execute("SELECT * FROM location WHERE mac='"+mac+"'")
       conn.commit()


       if recordcount>0:
           #执行更新语句
           print 'update location set lon='+lon+',lat='+lat+" where mac='"+mac+"'"
           cursor.execute('update location set lon='+lon+',lat='+lat+" where mac='"+mac+"'")
           conn.commit()
           response=cursor.execute("SELECT * FROM location WHERE mac='"+mac+"'")
           conn.commit()
       else:
           # 执行插入语句
           response=cursor.execute('INSERT INTO location VALUES(null,'+lon+','+lat+",'"+mac+"')")
           conn.commit()

       cursor.close()
       conn.close()
       return response
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/wifitraffic/location",Loaction_Handler),
        ],
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
