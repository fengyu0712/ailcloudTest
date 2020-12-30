# coding: utf-8
# @Time : 2020-12-30 14:14 
# @Author : xx
# @File : configparser_tool.py 
# @Software: PyCharm
from config import base_path
import configparser
import os

def get_env():
    config = configparser.ConfigParser()  # 注意大小写
    #print(base_path+"\pytest.ini")
    # 配置文件的路径
    config.read(base_path+os.sep+"pytest.ini")
    #得到指定section的所有option
    str_val = config.get("pytest", "addopts")
    return str_val