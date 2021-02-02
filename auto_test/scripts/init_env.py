# coding: utf-8
# @Time : 2021-1-4 10:48 
# @Author : xx
# @File : init_env.py 
# @Software: PyCharm

import config
from config import host_address_list,device_status_list,alltotal_devices
from tools import configparser_tool
envinfo=config.test_env
if envinfo.find("sit")!=-1:
    current_env="sit"
elif envinfo.find("dit")!=-1:
    current_env="dit"
elif envinfo.find("uat")!=-1:
    current_env="uat"
elif envinfo.find("pro")!=-1:
    current_env="pro"
elif envinfo.find("test")!=-1:
    current_env="test"
else:
    current_env="pro"


host=host_address_list[current_env]
# 3、http请求的主机地址,获取设备的状态
http_host=device_status_list[current_env]
# 终端设备信息
terminal_devices=alltotal_devices[current_env]