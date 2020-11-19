# coding: utf-8
from config import http_host
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

     # 新增方法
     def post(self,mid):
         try:
             headers={"Content-Type":"application/json "}
             self.params={"mid": "%s"%mid}
             log.info("获取设备状态,请求参数为:{}".format(self.params))
             jsonvalue = requests.post("https://uat.aimidea.cn:11003/v1/common/device/getDeviceStatus", json=self.params, headers=headers).json()
             log.info("获取设备状态信息:{}".format(jsonvalue))
             return jsonvalue
         except Exception as e:
             print(e)
             log.info("获取设备状态异常:{}".format(e))
             return {}


if __name__ == '__main__':
   jsonvalue= Api().post("a8072d11f1da203160e2ab3a9d96f680")
   print(jsonvalue)