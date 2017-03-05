#coding=utf-8
import  xml.dom.minidom
from getpath import get_current_dir

#从properties.xml中获取mysql用户名、密码
def get_username_and_password():
    #打开xml文档
    dom = xml.dom.minidom.parse(get_current_dir()+'/properties.xml')
    #得到文档元素对象
    root = dom.documentElement
    mysql_uesrname= root.getElementsByTagName('mysql_uesrname')
    mysql_password=root.getElementsByTagName('mysql_password')
    #获得用户名与密码
    user= str(mysql_uesrname[0].firstChild.data)
    passwd=str(mysql_password[0].firstChild.data)
    if passwd=='null':passwd=''
    return dict({'user':user,'passwd':passwd})

#properties.xml获取更新时间间隔
def get_update_time_interval():
    #打开xml文档
    dom = xml.dom.minidom.parse(get_current_dir()+'/properties.xml')
    #得到文档元素对象
    root = dom.documentElement
    update_time_interval= root.getElementsByTagName('update_time_interval')
    #获得更新时间间隔
    update_time= int(update_time_interval[0].firstChild.data)
    return dict({'update_time':update_time})


