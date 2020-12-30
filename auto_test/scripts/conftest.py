# coding: utf-8
# @Time : 2020-11-30 18:10
# @Author : xx
# @File : conftest.py.py
# @Software: PyCharm

from config import host_address_list,device_status_list,alltotal_devices
from tools import configparser_tool
envinfo=configparser_tool.get_env()
if envinfo.find("sit")!=-1:
    current_env="sit"
elif envinfo.find("dit")!=-1:
    current_env="dit"
elif envinfo.find("uat")!=-1:
    current_env="uat"
else:
    current_env="pro"


host=host_address_list[current_env]
# 3、http请求的主机地址,获取设备的状态
http_host=device_status_list[current_env]
# 终端设备信息
terminal_devices=alltotal_devices[current_env]