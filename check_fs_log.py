#!/usr/bin/env python
#coding=utf-8
from os.path import getsize
from sys import exit
from re import compile

#定义日志文件位置
#fs_log = '/usr/local/freeswitch/log/freeswitch.log'
fs_log = 'test.log'
#该文件是用于记录上次读取日志文件的位置,执行脚本的用户要有创建该文件的权限
last_position_logfile = '/tmp/last_position.txt'
#匹配的错误信息关键字的正则表达式
pattern = compile(r'from (\d+\.\d+\.\d+\.\d+)')

#读取上一次日志文件的读取位置
def get_last_position(file):
    try:
        data = open(file,'r')
        last_position = data.readline()
        if last_position:
            last_position = int(last_position)
        else:
            last_position = 0
    except:
        last_position = 0
    return last_position
#写入本次日志文件的本次位置
def write_this_position(file,last_positon):
    try:
        data = open(file,'w')
        data.write(str(last_positon))
        data.write('\n' + "Don't Delete This File,It is Very important for Looking Tomcat Error Log !! \n")
        data.close()
    except:
        print "Can't Create File !" + file
        exit()
#分析文件找出异常的行
def analysis_log(file):
    error_list = []                                      
    try:
        data = open(file,'r')
    except:
        exit()
    print data.tell()             
    last_position = get_last_position(last_position_logfile)
    this_postion = getsize(fs_log)
    if this_postion < last_position:
        data.seek(0)
    elif this_postion == last_position:
        exit()
    elif this_postion > last_position:
        data.seek(last_position)
    for line in data:
        _list = pattern.findall(line)
        if len(_list) >= 1 :
            if _list[0] not in error_list:
                error_list.append(_list[0])
    print data.tell()                 
    write_this_position(last_position_logfile,data.tell())
    data.close()
    return '\n'.join(error_list)
error_info = analysis_log(fs_log)
if error_info:
    a=open('/tmp/ip.list',"w")
    a.write(error_info)
    a.close()
