# coding: utf-8
from scripts.init_env import http_host
import os
import requests
from tools.get_log import GetLog
log=GetLog.get_logger()  # 初始化日志对象

class Api:
     # 初始化
     def __init__(self):
         pass

     # 查询方法
     def _get(self):
         pass

     # 新增方法,获取设备状态
     def post(self,mid):
         try:
             headers={"Content-Type":"application/json "}
             self.params={"mid": "%s"%mid}
             device_host = http_host + "/v1/common/device/getDeviceStatus"
             log.info("获取设备状态,请求参数为:{},地址:{}".format(self.params, device_host))
             jsonvalue = requests.post(device_host, json=self.params, headers=headers).json()
             log.info("获取设备状态信息:{}".format(jsonvalue))
             return jsonvalue
         except Exception as e:
             print(e)
             log.info("获取设备状态异常:{}".format(e))
             return {}



if __name__ == '__main__':
   jsonvalue= Api().post("ac1879e649ae11eb94fd005056c00008")
   print(jsonvalue)