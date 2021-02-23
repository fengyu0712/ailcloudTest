# coding: utf-8
# 328
import time
import uuid
from scripts.init_env import terminal_devices


class Deviceset():
    def __init__(self, terminal_type):
        self.devicetype = terminal_type  # 设备类型
        self.device_info = terminal_devices.get(terminal_type)  # 获取设备信息
        self.sn = self.device_info.get("sn")  # sn信息
        self.clientid = self.device_info.get("clientid")  # clientid信息
        self.deviceId = self.device_info.get("deviceId")  # deviceId信息
        self.set_headers()  # 初始化列表信息

    def get_time_stamp(self):
        ct = time.time()
        local_time = time.localtime(ct)
        data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        data_secs = (ct - int(ct)) * 1000
        time_stamp = "%s.%03d" % (data_head, data_secs)
        return time_stamp

    # 添加头部信息
    def set_headers(self):
        self.headers = list()
        self.__addonline()  # 添加上线信息
        self.__add_stausdata()  # 添加上报音量信息
        self.__addcontent()  # 添加content信息

    def __add_stausdata(self):
        status_data = {
            "version": "3.0",
            "topic": "cloud.report.status",
            "mid": uuid.uuid1().hex,
            "category": "AC",
            "id": "10995116462864",
            "clientId": self.clientid,
            "sn": self.sn,
            "request": {
                "timestamp": self.get_time_stamp(),
            },
            "params": {
                "status": [{
                    "class": "audio",
                    "audio": {
                        "level": "4",
                        "max": "99",
                        "min": "1",
                        "volume": "75"
                    }
                }]
            }
        }
        print(status_data)
        self.headers.append(status_data)

    # 添加上线的信息
    def __addonline(self):
        if self.devicetype == "yuyintie_1":
            online_data = {
                "topic": "cloud.online",
                "version": "3.0",
                "mid": uuid.uuid1().hex,
                "request": {
                    "apiVer": "1.0.0",
                    "timestamp": self.get_time_stamp(),
                    "paramsSignBase64": "8b0NLQ0rJ1Vb/MpTZ9vXHLsRMCk="
                },
                "params": {
                    "category": "8",
                    "clientId": self.clientid,
                    "id": self.deviceId,
                    "ip": "127.0.0.1",
                    "mac": "50:2d:bb:b3:e5:a5",
                    "model": "22",
                    "productId": "1596681815",
                    "sn": self.sn,
                }
            }
        elif self.devicetype == "3308_halfDuplex":
            online_data = {
                "topic": "cloud.online",
                "version": "2.0",
                "mid": uuid.uuid1().hex,
                "request": {
                    "apiVer": "1.0.0",
                    "timestamp": self.get_time_stamp()
                },
                "params": {
                    "category": "0xAC",
                    "clientId": self.clientid,
                    "id": self.deviceId,
                    "sn": self.sn,
                    "magicCode": "TSETIA"
                }
            }

        else:
            online_data = {
                "topic": "cloud.online",
                "mid": "%s" % uuid.uuid1().hex,
                "version": "3.0",
                "request": {
                    "apiVer": "1.0.0",
                    "timestamp": self.get_time_stamp(),

                },
                "params": {
                    "id": self.deviceId,
                    "sn": self.sn,
                    "clientId": self.clientid,
                    "category": "0xAC",
                    "magicCode": "TSETIA"
                }
            }

        print(online_data)
        self.headers.append(online_data)

    def __addcontent(self):
        if self.devicetype == "328_halfDuplex":
            content_data = {
                "version": "3.0",
                "topic": "cloud.speech.trans",
                "mid": uuid.uuid1().hex,
                "id": self.deviceId,
                "category": "AC",
                "request": {
                    "apiVer": "1.0.0",
                    "sessionId": uuid.uuid1().hex,
                    "recordId": uuid.uuid1().hex,
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
        elif self.devicetype == "328_fullDuplex":
            content_data = {
                "version": "3.0",
                "topic": "cloud.speech.trans",
                "mid": uuid.uuid1().hex,
                "id": self.deviceId,
                "sn": self.sn,
                "clientId": self.clientid,
                "category": "AC",
                "request": {
                    "apiVer": "1.0.0",
                    "sessionId": uuid.uuid1().hex,
                    "recordId": uuid.uuid1().hex,
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

        elif self.devicetype == "yuyintie_1":
            content_data = {
                "topic": "cloud.speech.trans",
                "mid": uuid.uuid1().hex,
                "version": "1.0",
                "request": {
                    "timestamp": self.get_time_stamp(),
                    "sessionId": uuid.uuid1().hex,
                    "recordId": uuid.uuid1().hex,
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
        elif self.devicetype == "xf__halfDuplex":
            content_data = {
                "topic": "cloud.speech.trans",
                "mid": uuid.uuid1().hex,
                "version": "1.0",
                "request": {
                    "timestamp": self.get_time_stamp(),
                    "sessionId": uuid.uuid1().hex,
                    "recordId": uuid.uuid1().hex,
                },
                "params": {
                    "audio": {
                        "audioType": "wav",
                        "sampleRate": 16000,
                        "channel": 1,
                        "sampleBytes": 2
                    },
                    "fullDuplex": False,
                    "asrIsp": "xf-aiui",
                    "accent": "mandarin",
                }
            }
        elif self.devicetype == "3308_halfDuplex":
            content_data = {
                "version": "2.0",
                "topic": "cloud.speech.trans",
                "mid": uuid.uuid1().hex,
                "id": self.deviceId,
                "sn": self.sn,
                "clientId": self.clientid,
                "category": "AC",
                "request": {
                    "apiVer": "1.0.0",
                    "sessionId": uuid.uuid1().hex,
                    "recordId": uuid.uuid1().hex,
                    "isMore": False
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
