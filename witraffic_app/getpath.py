#coding=utf-8
import os
import sys

#获得应用根目录绝对路径
#注意，网上说的三个常用的获取当前路径的方法：
#os.getcwd()
#os.path.abspath('.')
#os.path.abspath(os.curdir)
# 在linux运行机制里返回的当前路径并不是脚本所在当前路径，而是当前工作路径服务器即用户账号根目录路径，并不是脚本所处目录路径
#Python另一个获取当前路径的接口是sys.path[0]，返回的是包含了启动Python解析器的脚本文件的文件夹，就是.py文件所处文件夹
def get_current_dir():
    current_dir = sys.path[0]
    #如果rootpath是一个通过py2exe把当前脚本打包成的exe文件，则需额外考虑
    if os.path.isfile(current_dir):
        current_dir = os.path.dirname(current_dir)
    return current_dir