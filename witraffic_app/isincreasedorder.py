#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 定义函数
def isincreasedorder(x):
    if cmp(x,sorted(x))==0:
        return True
    else:
        return False


