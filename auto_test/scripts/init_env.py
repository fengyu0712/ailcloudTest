# coding: utf-8
# @Time : 2021-1-4 10:48 
# @Author : xx
# @File : init_env.py 
# @Software: PyCharm

import config
from config import ws_host_list, device_status_host_list, alltotal_devices, yinxiang_host_list, meiju_host_list, \
    api_host_list
from tools import configparser_tool

envinfo = config.test_env
if envinfo.find("sit") != -1:
    current_env = "sit"
elif envinfo.find("dit") != -1:
    current_env = "dit"
elif envinfo.find("uat") != -1:
    current_env = "uat"
elif envinfo.find("pro") != -1:
    current_env = "pro"
elif envinfo.find("test") != -1:
    current_env = "test"
else:
    current_env = "pro"

host = ws_host_list[current_env]
# 3、http请求的主机地址,获取设备的状态
ws_host = ws_host_list[current_env]

# 音箱地址
yinxiang_host = yinxiang_host_list[current_env]

# 美居地址
meiju_host = meiju_host_list[current_env]

# 终端设备信息
terminal_devices = alltotal_devices[current_env]

# open_api地址
api_host = api_host_list[current_env]

# 设备状态查询地址
device_status_host = device_status_host_list[current_env]
