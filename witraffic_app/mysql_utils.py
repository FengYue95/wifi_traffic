#coding=utf-8
import MySQLdb
from getProperties import get_username_and_password



#从数据库获取全路网路段信息列表
def getsegmentlist():
    try:
        user=get_username_and_password()['user']
        passwd=get_username_and_password()['passwd']
        # 打开数据库连接
        #  使用cursor()方法获取操作游标,指定游标的类型为MySQLdb.cursors.DictCursor则结果集以字典返回，带有字段名；不知名类型则默认以元组返回，无字段名
        conn=MySQLdb.connect(host='localhost',user=user,passwd=passwd,db='traffic_db',port=3306)
        # 使用cursor()方法获取操作游标
        cur=conn.cursor(cursorclass =MySQLdb.cursors.DictCursor)
        #执行sql语句
        count=cur.execute('select * from roadnet order by segmentid')
        print 'there are %s segments in the whole roadnet' % count
        #获得结果集
        results=cur.fetchall()
        #必须提交请求
        conn.commit()
        cur.close()
        conn.close()
        print 'there are '+str(len(results))+' roads'
        return results
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        cur.close()
        conn.close()

#从数据库获取指定分区路段信息列表
def get_segmentlist_of_area(area):
    try:
        user=get_username_and_password()['user']
        passwd=get_username_and_password()['passwd']
        # 打开数据库连接
        #  使用cursor()方法获取操作游标,指定游标的类型为MySQLdb.cursors.DictCursor则结果集以字典返回，带有字段名；不知名类型则默认以元组返回，无字段名
        conn=MySQLdb.connect(host='localhost',user=user,passwd=passwd,db='traffic_db',port=3306,cursorclass = MySQLdb.cursors.DictCursor)
        # 使用cursor()方法获取操作游标
        cur=conn.cursor()
        #执行sql语句
        count=cur.execute("select * from roadnet where area like '%"+area+"%'")
        print 'there has %s segments in area %s' % (count,area)
        #获得结果集
        results=cur.fetchall()
        #必须提交请求
        conn.commit()
        cur.close()
        conn.close()
        return results
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        cur.close()
        conn.close()



#上载数据到数据库
def upload2mysql(sql_list):
    try:
       user=get_username_and_password()['user']
       passwd=get_username_and_password()['passwd']
       # 打开数据库连接
       conn=MySQLdb.connect(host='localhost',user=user,passwd=passwd,db='traffic_db',port=3306)
       # 使用cursor()方法获取操作游标
       cursor = conn.cursor()
       for sql in sql_list:
           # 执行sql语句
           cursor.execute(sql)
           # 提交到数据库执行
           conn.commit()

       #关闭游标和链接
       cursor.close()
       conn.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        cursor.close()
        conn.close()

#获得路网覆盖的各区域板块名称
def getAreas():
    seglist=getsegmentlist()
    arealist=[]
    for seg in seglist:
        arealist.append(seg['area'])

    arealist=list(set(arealist))
    print arealist
    return arealist

#由探针编号获得一个探针mac
def getMacByAPid(APid):
    try:
        user=get_username_and_password()['user']
        passwd=get_username_and_password()['passwd']
        # 打开数据库连接
        #  使用cursor()方法获取操作游标,指定游标的类型为MySQLdb.cursors.DictCursor则结果集以字典返回，带有字段名；不知名类型则默认以元组返回，无字段名
        conn=MySQLdb.connect(host='localhost',user=user,passwd=passwd,db='traffic_db',port=3306)
        cur=conn.cursor(MySQLdb.cursors.DictCursor)
        #执行sql语句
        cur.execute("select * from location where num="+str(APid))
        #获得一条结果
        result=cur.fetchone()
        #必须提交请求
        conn.commit()
        cur.close()
        conn.close()
        return result['mac']
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        cur.close()
        conn.close()


def getMacListByAPid(APid):
    mac_list=[]
    try:
        user=get_username_and_password()['user']
        passwd=get_username_and_password()['passwd']
        # 打开数据库连接
        #  使用cursor()方法获取操作游标,指定游标的类型为MySQLdb.cursors.DictCursor则结果集以字典返回，带有字段名；不知名类型则默认以元组返回，无字段名
        conn=MySQLdb.connect(host='localhost',user=user,passwd=passwd,db='traffic_db',port=3306)
        cur=conn.cursor(MySQLdb.cursors.DictCursor)
        #执行sql语句
        cur.execute("select * from location where num="+str(APid))
        #获得一条结果
        results=cur.fetchall()
        #必须提交请求
        conn.commit()
        cur.close()
        conn.close()
        for result in results:
            mac_list.append(result['mac'])

        return mac_list
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        cur.close()
        conn.close()

