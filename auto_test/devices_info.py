# coding: utf-8
# 328
import uuid
from config import terminal_devices
class Deviceset():
    def __init__(self,terminal_type):
        self.devicetype=terminal_type   #  设备类型
        self.sn=terminal_devices.get(terminal_type)  # sn信息
        self.set_headers()# 初始化列表信息

    # 添加头部信息
    def set_headers(self):
        self.headers = list()
        self.__addonline() # 添加上线信息
        self.__addcontent()  # 添加content信息

    # 添加上线的信息
    def __addonline(self):
        online_data = {
            "topic": "cloud.online",
            "mid": "%s" % uuid.uuid1().hex,
            "version": "3.0",
            "request": {
                "apiVer": "1.0.0",
                "timestamp": 1234567890,

            },
            "params": {
                "id": "3298544982176",
                "sn": "%s" % self.sn,
                "clientId": "cf6411ef-976d-4292-a92a-1f0a765615b2",
                "category": "0xAC",
                "magicCode": "TSETIA"
            }
        }
        self.headers.append(online_data)


    def __addcontent(self):
        if self.devicetype=="328":
            content_data = {
                "version": "3.0",
                "topic": "cloud.speech.trans",
                "mid": "%s"% uuid.uuid1().hex,
                "id": "3298544982176",
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
                "id": "3298544982176",
                "sn": "%s" % self.sn,
                "clientId": "cf6411ef-976d-4292-a92a-1f0a765615b2",
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

        self.headers.append(content_data)


