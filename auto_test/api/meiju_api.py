# coding: utf-8
# @Time : 2021-1-7 14:14
# @Author : xx
# @File : test_xf.py.py
# @Software: PyCharm
import time

import requests
from urllib import parse
import uuid
from api.apis import Api
from scripts.init_env import terminal_devices, http_host


class Meijuapi():
    def __init__(self, device_info=None):
        if device_info == None:
            self.device_info = terminal_devices["meiju"]
        else:
            self.device_info = device_info
        self.uid = self.device_info["uid"]
        self.homeId = self.device_info["homeId"]

    def post(self, text, accessToken=None):
        uuid_value = str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) + "mid"))
        if accessToken == None:
            accessToken = Api().get_token(self.uid)
        try:
            url = http_host + "/v1/base2pro/data/transmit"
            data = {
                "data": {
                    "mid": str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) + "mid")),
                    "version": "v2",
                    "params": {"text": "%s" % text},
                    "device": {},
                    "user": {"homeId": "%s" % self.homeId,
                             "accessToken": "%s" % accessToken,
                             "uid": "%s" % self.uid}
                },
                "serviceUrl": "/v2/speech/nlp/meiju"
            }

            data = parse.urlencode(data)
            headres = {"Content-Type": "application/x-www-form-urlencoded"}
            a = requests.post(url, data=data, headers=headres)
            return a.json()
        except Exception as ex:
            return uuid_value


if __name__ == '__main__':
    # while True:
    # info={"mobile": "13017659465", "uid": "e870a1c7cc38ce4ee15f900e9e0ee88c", "homeId": "162681",
    #  "accessToken": "T15ig02nvchs4sngu"}
    # a = Meijuapi(device_info=info).post("空调开机")
    a = Meijuapi().post("冰箱里面有什么")
    # b = Meijuapi().post("风速小一点")
    # a = Meijuapi().post("晚上二十三点五十九分的")
    print(a)
