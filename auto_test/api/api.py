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

     # 新增方法,获取设备状态
     def post(self,mid):
         try:
             headers={"Content-Type":"application/json "}
             self.params={"mid": "%s"%mid}
             log.info("获取设备状态,请求参数为:{},地址:{}".format(self.params,http_host))
             jsonvalue = requests.post(http_host, json=self.params, headers=headers).json()
             log.info("获取设备状态信息:{}".format(jsonvalue))
             return jsonvalue
         except Exception as e:
             print(e)
             log.info("获取设备状态异常:{}".format(e))
             return {}

     def post_orion(self):
         import uuid
         orion_url="http://sit.aimidea.cn:11003//v1/ai/speech/nlu"

         http_body={"clientId":"0e215b2bc3f6cfa41cc3bfdc845b890c",
                    "mid":uuid.uuid1().hex,
                    "version":"1.0",
                    "request":{"timestamp":"1540463976528"},
                     "params":{"text":"打开卧室空调"},
                     "device":{"deviceType":"","deviceId":"111000010213019416Z038","lat":22.80452,"lng":113.29394}}

         import random
         import string
         import hashlib
         ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 20))
         sign_value=str(http_body)+str(ran_str)+"2cddc204b428ef114e29664704698dcd"
         #print(sign_value)

         m = hashlib.md5()

         # Tips
         # 此处必须encode
         # 若写法为m.update(str)  报错为： Unicode-objects must be encoded before hashing
         # 因为python3里默认的str是unicode
         # 或者 b = bytes(str, encoding='utf-8')，作用相同，都是encode为bytes
         b = sign_value.encode(encoding='utf-8')
         print("加密后的值。。",b)
         m.update(b)
         str_md5 = m.hexdigest()
         print(str_md5)

         headers = {"Content-Type": "application/json ", "sign":str_md5 , "random": ran_str}
         jsonvalue = requests.post(orion_url, json=http_body, headers=headers)
         print(jsonvalue)
         print(jsonvalue.content)



if __name__ == '__main__':
   jsonvalue= Api().post("e98bcf4b1530491b98ca91788b3a4c08")
   print(jsonvalue)