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
    def __init__(self):
        self.device_info = terminal_devices["meiju"]
        self.uid = self.device_info["uid"]
        self.homeId = self.device_info["homeId"]
        self.accessToken = Api().get_token(self.uid)

    def post(self, text):
        uuid_value = str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) + "mid"))
        try:
            url = http_host + "/v1/base2pro/data/transmit"
            data = {
                "data": {
                    "mid": str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) + "mid")),
                    "version": "v2",
                    "params": {"text": "%s" % text},
                    "device": {},
                    "user": {"homeId": "%s" % self.homeId,
                             "accessToken": "%s" % self.accessToken,
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
    a = Meijuapi().post("帮我定个闹钟")
    a = Meijuapi().post("晚上二十三点五十九分的")
    print(a)
