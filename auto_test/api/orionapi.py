# coding: utf-8
# @Time : 2020-12-29 15:18
# @Author : xx
# @File : orionapi.py
# @Software: PyCharm

import requests
import random
import string
import json
import time
import datetime
import uuid
import hashlib, base64
import config
from api import apis
from scripts.init_env import http_host, current_env, terminal_devices


class OrionApi():
    def __init__(self, text):
        self.device_info = terminal_devices["yinxiang"]
        self.orion_url = http_host + "/v1/ai/speech/nlu"
        self.invoke_url = http_host + '/v1/orion/skill/invoke'
        self.asr_text = text
        self.deviceid = self.device_info["deviceid"]

    def gen_ranvalue(self):
        datetime_now = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        if len(datetime_now) == 20:
            datetime_now = datetime_now[:-1]
        # print("随机数：", datetime_now)
        return datetime_now

    def get_token(self, sign_value):
        m = hashlib.md5()
        b = sign_value.encode(encoding='utf-8')
        m.update(b)
        str_md5 = m.hexdigest()
        # print(str_md5)
        return str_md5

    def orion_nlu_post(self):
        clientid = self.device_info["clientid"]
        clientKey = self.device_info["clientKey"]
        time_stamp = round(time.time() * 1000)
        midvalue = uuid.uuid1().hex
        http_body = {
            "clientId": clientid,
            "device": {
                "deviceId": self.deviceid,
                "deviceType": "2",
                "lat": "0.000000",
                "lng": "0.000000"
            },
            "mid": midvalue,
            "params": {"text": self.asr_text},
            "request": {
                "timestamp": time_stamp
            },
            "version": "1.0"
        }
        str_http_body = json.dumps(http_body, ensure_ascii=False).replace(" ", "")
        ran_value = self.gen_ranvalue()
        sign_value = str_http_body + ran_value + clientKey
        token_key = self.get_token(sign_value)
        self.header_host = http_host.split("//")[-1]
        headers = {
            "host": self.header_host,
            "remoteip": '218.13.14.225',
            "sign": token_key,
            "random": ran_value,
            "content-type": "application/json",
            "accept-encoding": "gzip",
            "user-agent": "AIokhttp/3.14.2",
        }
        response = requests.post(self.orion_url, json=http_body, headers=headers)
        jsonvalue = response.text
        print("orion_nlu_post:" + jsonvalue)
        return {"mid": midvalue, "nlu": jsonvalue}

    def orion_invoke_post(self, midvalue):
        uid = self.device_info["uid"]
        third_access_token = apis.Api().get_token(uid)
        info = {
            "request": {
                "asr": {
                    "text": self.asr_text
                },
                "nlu": {
                    "slots": {
                        "nlu": {
                            "classifier": "mideaDomain"
                        }
                    },
                    "domain": "mideaDomain",
                    "intent": "transmit",
                    "english_domain": "mideaDomain"
                },
                "type": "IntentRequest"
            },
            "session": {
                "application": {
                    "client": {
                        "clientId": "orion.ovs.client.1507867446289"
                    },
                    "skill": {
                        "linkAccount": {
                            "orion.ovs.rsplatform.1488857923": {
                                "third_access_token": third_access_token,
                                "bind": 1,
                                "third_uid": uid,
                                "third_refresh_token": third_access_token,
                                "type": "fusion_msmart"
                            }
                        },
                        "skillId": "orion.ovs.skill.1540972223847",
                        "skillStatus": "online"
                    }
                },
                "attributes": {

                },
                "sessionId": midvalue,
                "user": {
                    "isLogin": True,
                    "openId": "fcb5d68518a4e52f2b0f19a8b1ffbc7a",
                    "unionAccessToken": "eyJhbGciOiJIUzI1NiJ9.eyJjbGllbnRJZCI6Im9yaW9uLnVjZW50ZXIuYzZjYmJkOWRhYWE2NDI1YSIsIm9wZW5JZCI6ImZjYjVkNjg1MThhNGU1MmYyYjBmMTlhOGIxZmZiYzdhIiwic2NvcGUiOiJvdnM6ZGV2aWNlIiwiaXNzIjoiaHR0cDovL2FwaS5jaGlsZC5jbWNtLmNvbSIsImV4cCI6MTYwOTIyNjcxOSwidHlwZSI6ImFjY2Vzc190b2tlbiIsImlhdCI6MTYwOTIxOTUxOSwidmVyc2lvbiI6IjEuMCJ9.xEBaj9H-Pb5b6wzn6X25rGRhRHh_94ghvn31PwE87jo",
                    "userId": "872965",
                    "voiceprintExists": False,
                    "voiceprintPay": False
                }
            },
            "context": {
                "System": {
                    "cookies": {

                    },
                    "device": {
                        "deviceId": self.deviceid,
                        "deviceType": "2",
                        "lang": "zh_CN",
                        "lat": "0.000000",
                        "lng": "0.000000",
                        "osType": "0",
                        "sys_lang": "auto",
                        "version": "1.0.0"
                    },
                    "params": {
                        "lng": "0.000000",
                        "os_version": "1.2.14",
                        "device_type": 2,
                        "deviceid": self.deviceid,
                        "version": "1.0.0",
                        "client_id": "orion.ovs.client.1507867446289",
                        "dt": 7,
                        "ovs_sdk_version": "0.3.0",
                        "union_access_token": "eyJhbGciOiJIUzI1NiJ9.eyJjbGllbnRJZCI6Im9yaW9uLnVjZW50ZXIuYzZjYmJkOWRhYWE2NDI1YSIsIm9wZW5JZCI6ImZjYjVkNjg1MThhNGU1MmYyYjBmMTlhOGIxZmZiYzdhIiwic2NvcGUiOiJvdnM6ZGV2aWNlIiwiaXNzIjoiaHR0cDovL2FwaS5jaGlsZC5jbWNtLmNvbSIsImV4cCI6MTYwOTIyNjcxOSwidHlwZSI6ImFjY2Vzc190b2tlbiIsImlhdCI6MTYwOTIxOTUxOSwidmVyc2lvbiI6IjEuMCJ9.xEBaj9H-Pb5b6wzn6X25rGRhRHh_94ghvn31PwE87jo",
                        "user_id": "872965",
                        "ovs_sdk_os": "linux",
                        "os_type": "0",
                        "model": "MOBE-VA013",
                        "lat": "0.000000"
                    }
                }
            },
            "version": "0.2.0"
        }
        heads = {
            "host": self.header_host,
            "remoteip": "218.13.14.225",
            "sid": "2c18f55d65e71260ad15d5ec7cbb8084",
            "content-type": "application/json; charset=utf-8",
            "accept-encoding": "gzip",
            "user-agent": "okhttp/3.14.2",
            "x-forwarded-proto": "http"
        }
        jsonvalue = requests.post(self.invoke_url, json=info, headers=heads)
        return jsonvalue.json()

    def orion_post(self):
        nlu_result = self.orion_nlu_post()
        print(nlu_result)
        mid = nlu_result["mid"]
        resultinfo = self.orion_invoke_post(mid)
        result = {**resultinfo, **nlu_result}
        return result


if __name__ == '__main__':
    api = OrionApi("打开净化器")
    a = api.orion_post()
    print(a)
