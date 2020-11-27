# coding: utf-8
# 328
import uuid
from config import terminal_devices
class Deviceset():
    def __init__(self,terminal_type):
        self.devicetype=terminal_type   #  设备类型
        self.device_info=terminal_devices.get(terminal_type)  # 获取设备信息
        self.sn=self.device_info.get("sn")  #sn信息
        self.clientid = self.device_info.get("clientid")  # clientid信息
        self.deviceId = self.device_info.get("deviceId")  # deviceId信息
        self.set_headers()# 初始化列表信息

    # 添加头部信息
    def set_headers(self):
        self.headers = list()
        self.__addonline() # 添加上线信息
        self.__addcontent()  # 添加content信息

    # 添加上线的信息
    def __addonline(self):
        if self.devicetype == "yuyintie_1":
            online_data={
                 "topic": "cloud.online",
                 "version": "3.0",
                 "mid": "%s" % uuid.uuid1().hex,
                 "request": {
                  "apiVer": "1.0.0",
                  "timestamp": 3,
                  "paramsSignBase64": "8b0NLQ0rJ1Vb/MpTZ9vXHLsRMCk="
                 },
                 "params": {
                  "category": "8",
                  "clientId": "%s" % self.clientid,
                  "id": "%s" % self.deviceId,
                  "ip": "127.0.0.1",
                  "mac": "50:2d:bb:b3:e5:a5",
                  "model": "22",
                  "productId": "1596681815",
                  "sn": "%s" % self.sn,
                 }
            }
        else:
            online_data = {
                "topic": "cloud.online",
                "mid": "%s" % uuid.uuid1().hex,
                "version": "3.0",
                "request": {
                    "apiVer": "1.0.0",
                    "timestamp": 1234567890,

                },
                "params": {
                    "id": "%s" % self.deviceId,
                    "sn": "%s" % self.sn,
                    "clientId": "%s" % self.clientid,
                    "category": "0xAC",
                    "magicCode": "TSETIA"
                }
        }

        print(online_data)
        self.headers.append(online_data)


    def __addcontent(self):
        if self.devicetype=="328" :
            content_data = {
                "version": "3.0",
                "topic": "cloud.speech.trans",
                "mid": "%s"% uuid.uuid1().hex,
                "id": "%s" % self.deviceId,
                "category": "AC",
                "request": {
                    "apiVer": "1.0.0",
                    "sessionId": "%s" % uuid.uuid1().hex,
                    "recordId": "%s" % uuid.uuid1().hex,
                    "isMore": False
                },
                "params": {
                    "audio": {
                        "audioType": "wav",
                        "sampleRate": 16000,
                        "channel": 1,
                        "sampleBytes": 2
                    },
                    "ttsIsp": "dui-real-sound",
                    "nluIsp": "DUI",
                    "asrIsp": "DUI",
                    "serverVad": False,
                    "accent": "mandarin",
                    "mixedResEnable": "0"
                }
            }
        elif self.devicetype=="328_fullDuplex":
            content_data = {
                "version": "3.0",
                "topic": "cloud.speech.trans",
                "mid": uuid.uuid1().hex,
                "id": "%s" % self.deviceId,
                "sn": "%s" % self.sn,
                "clientId": "%s" % self.clientid,
                "category": "AC",
                "request": {
                    "apiVer": "1.0.0",
                    "sessionId":"%s" % uuid.uuid1().hex,
                    "recordId":"%s" % uuid.uuid1().hex,
                    "isMore": False
                },
                "params": {
                    "audio": {
                        "audioType": "wav",
                        "sampleRate": 16000,
                        "channel": 1,
                        "sampleBytes": 2
                    },
                    "ttsIsp": "dui-real-sound",
                    "nluIsp": "DUI",
                    "asrIsp": "DUI",
                    "serverVad": False,
                    "accent": "mandarin",
                    "fullDuplex": True
                }
            }

        elif self.devicetype=="yuyintie_1":
            content_data = {
                "topic": "cloud.speech.trans",
                "mid": uuid.uuid1().hex,
                "version": "1.0",
                "request": {
                    "timestamp": 1234567890,
                    "sessionId": "%s" % uuid.uuid1().hex,
                    "recordId": "%s" % uuid.uuid1().hex,
                },
                "params": {
                    "audio": {
                        "audioType": "wav",
                        "sampleRate": 16000,
                        "channel": 1,
                        "sampleBytes": 2
                    }
                }
            }

        self.headers.append(content_data)




