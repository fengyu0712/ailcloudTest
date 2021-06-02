# coding: utf-8
# 328
import time
import uuid
from scripts.init_env import terminal_devices


class Deviceset:
    def __init__(self, terminal_type, device_info=None):
        self.devicetype = terminal_type  # 设备类型
        if device_info == None:
            self.device_info = terminal_devices.get(terminal_type)  # 获取设备信息
        else:
            self.device_info = device_info
        if not self.device_info:
            self.device_info = terminal_devices.get("328_halfDuplex")
        self.sn = self.device_info["sn"]  # sn信息
        self.clientid = self.device_info.get("clientid")  # clientid信息
        self.deviceId = self.device_info.get("deviceId")  # deviceId信息
        self.module_version = self.device_info.get("module_version")
        if self.devicetype == "3308_halfDuplex":
            self.version = "1.0"
        else:
            self.version = "3.0"

    # def get_time_stamp(self):
    #     ct = time.time()
    #     local_time = time.localtime(ct)
    #     data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    #     data_secs = (ct - int(ct)) * 1000
    #     time_stamp = "%s.%03d" % (data_head, data_secs)
    #     return time_stamp

    def ota_check(self):
        ota_check_data = {
            "topic": "cloud.ota.check",
            "mid": str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) + "mid")),
            "version": self.version,
            "request": {
                "timestamp": int(time.time())
            },
            "params": {
                "sn": f"{self.sn}",
                "category": "AC",
                "model": "172",
                "id": f"{self.deviceId}",
                "clientId": "%s" % self.clientid,
                "brand": "Midea"
            }
        }

        def ota_module_version(module_version):
            module_version_slitList = module_version.split(".")
            module_version_json = {"hardwarePlat": module_version_slitList[0],
                                   "hardwareVer": module_version[:5],
                                   "hardwareCategory": module_version_slitList[1],
                                   "hardwareModel": module_version_slitList[4],
                                   "hardwareFullVer": module_version[:14],
                                   "firmwareVer": module_version}
            return module_version_json

        ota_check_data["params"].update(ota_module_version(self.module_version))
        return ota_check_data

    def audio_staus_data(self, volume=None):
        if volume == None:
            volume = 50
        status_data = {
            "version": self.version,
            "topic": "cloud.report.status",
            "mid": str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) + "mid")),
            "category": "AC",
            "id": f"{self.deviceId}",
            "clientId": "%s" % self.clientid,
            "sn": f"{self.sn}",
            "request": {
                "timestamp": int(time.time())
            },
            "params": {
                "status": [{
                    "class": "audio",
                    "audio": {
                        "level": "4",
                        "max": "100",
                        "min": "1",
                        "volume": f"{str(volume)}"
                    }
                }]
            }
        }
        return status_data

    def send_play_status(self, status=None):
        if status == None or status == "resume":
            status = "play"
        play_status = {
            "version": self.version,
            "topic": "cloud.report.status",
            "mid": str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) + "mid")),
            "category": "AC",
            "id": f"{self.deviceId}",
            "clientId": "%s" % self.clientid,
            "sn": f"{self.sn}",
            "request": {
                "timestamp": int(time.time())
            },
            "params": {
                "status": [{
                    "class": "player",
                    "player": {
                        "status": status,
                        "resource": {
                            "urlType": "media",
                            "skillType": "",
                            "autoResume": True,
                            "text": "浪人情歌",
                            "url": "http://mp3cdn.hifiok.com/00/0E/wKgBeVBdTYaA_OZBAKfeJQULj-M020.mp3?sign=0b57017c2d9b000b02e130377d008364&t=1613756930",
                            "seq": 1
                        }
                    }
                }]
            }
        }
        return play_status

    # 添加上线的信息
    def online_data(self):
        if self.devicetype == "yuyintie_1":
            online_data = {
                "topic": "cloud.online",
                "version": "3.0",
                "mid": str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) + "mid")),
                "request": {
                    "apiVer": "1.0.0",
                    "timestamp": int(time.time()),
                    "paramsSignBase64": "8b0NLQ0rJ1Vb/MpTZ9vXHLsRMCk="
                },
                "params": {
                    "category": "8",
                    "clientId": f" {self.clientid}",
                    "id": f"{self.deviceId}",
                    "ip": "127.0.0.1",
                    "mac": "50:2d:bb:b3:e5:a5",
                    "model": "22",
                    "productId": "1596681815",
                    "sn": f"{self.sn}",
                }
            }
        elif self.devicetype == "328_halfDuplex":
            online_data = {
                "topic": "cloud.online",
                "version": self.version,
                "mid": str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) + "mid")),
                "request": {
                    "apiVer": "1.0.0",
                    "timestamp": int(time.time()),
                    "paramsSignBase64": "8b0NLQ0rJ1Vb/MpTZ9vXHLsRMCk="
                },
                "params": {
                    "category": "AC",
                    "clientId": f"{self.clientid}",
                    "id": f"{self.deviceId}",
                    "ip": "127.0.0.1",
                    "mac": "f0:c9:d1:b5:f9:a7",
                    "model": "172",
                    "productId": "1596681815",
                    "sn": f"{self.sn}",
                }
            }
        elif self.devicetype == "xf__halfDuplex":
            online_data = {
                "topic": "cloud.online",
                "version": self.version,
                "mid": str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) + "mid")),
                "request": {
                    "apiVer": "1.0.0",
                    "timestamp": int(time.time()),
                    "paramsSignBase64": "BbheFT5fLRmkgtmXPTm/VCOiepg="
                },
                "params": {
                    "category": "AC",
                    "clientId": f"{self.clientid}",
                    "id": f"{self.deviceId}",
                    "ip": "127.0.0.1",
                    "mac": "a0:68:1c:b9:d2:9e",
                    "model": "172",
                    "productId": "1580967876",
                    "sn": f"{self.sn}",
                }
            }
        elif self.devicetype == "3308_halfDuplex":
            online_data = {
                "topic": "cloud.online",
                "version": self.version,
                "mid": str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) + "mid")),
                "request": {
                    "apiVer": "1.0.0",
                    "timestamp": int(time.time())
                },
                "params": {
                    "category": "0xAC",
                    "clientId": f"{self.clientid}",
                    "id": f"{self.deviceId}",
                    "sn": f"{self.sn}",
                    "magicCode": "TSETIA"
                }
            }
        else:
            online_data = {
                "topic": "cloud.online",
                "version": self.version,
                "mid": str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) + "mid")),
                "request": {
                    "apiVer": "1.0.0",
                    "timestamp": int(time.time()),
                    "paramsSignBase64": "8b0NLQ0rJ1Vb/MpTZ9vXHLsRMCk="
                },
                "params": {
                    "category": "AC",
                    "clientId": f"{self.clientid}",
                    "id": f"{self.deviceId}",
                    "ip": "127.0.0.1",
                    "mac": "f0:c9:d1:b5:f9:a7",
                    "model": "172",
                    "productId": "1596681815",
                    "sn": f"{self.sn}",
                }
            }
        return online_data

    def content_data(self):
        if self.devicetype == "328_halfDuplex":
            content_data = {
                "version": self.version,
                "topic": "cloud.speech.trans",
                "mid": str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) + "mid")),
                "id": "%s" % self.deviceId,
                "category": "AC",
                "request": {
                    "apiVer": "1.0.0",
                    "sessionId": str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) + "sessionId")),
                    "recordId": str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) + "recordId")),
                    "isMore": True
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
                "version": self.version,
                "topic": "cloud.speech.trans",
                "mid": str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) + "mid")),
                "id": "%s" % self.deviceId,
                "sn": "%s" % self.sn,
                "clientId": "%s" % self.clientid,
                "category": "AC",
                "request": {
                    "apiVer": "1.0.0",
                    "sessionId": str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) + "sessionId")),
                    "recordId": str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) + "recordId")),
                    # "sessionId": "0fc39a8e-beb2-11eb-9c77-9fbf258fc02bb",
                    # "recordId": "0fc39a8e-beb2-11eb-9c77-9fbf258fc02bb",
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
                "mid": str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) + "mid")),
                "version": self.version,
                "request": {
                    "timestamp": int(time.time()),
                    "sessionId": str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) + "sessionId")),
                    "recordId": str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) + "recordId")),
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
                "version": "3.0",
                "topic": "cloud.speech.trans",
                "mid": str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) + "mid")),
                "id": f"{self.deviceId}",
                "sn": self.sn,
                "clientId": "381f33d9-c25e-4d3e-a1cd-847000683ab3",
                "category": "AC",
                "request": {
                    "apiVer": "1.0.0",
                    "sessionId": str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) + "sessionId")),
                    "recordId": str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) + "recordId")),
                    "isMore": False
                },
                "params": {
                    "audio": {
                        # "audioType": "opus-wb",  #真实设备是opus格式，需要向嵌入式了解该格式上传的逻辑
                        "audioType": "wav",
                        "sampleRate": 16000,
                        "channel": 1,
                        "sampleBytes": 2
                    },
                    "ttsIsp": "dui-real-sound",
                    "nluIsp": "xf-aiui",
                    "asrIsp": "xf-aiui",
                    "serverVad": True,
                    "accent": "mandarin",
                    "mixedResEnable": "0"
                }
            }
        elif self.devicetype == "3308_halfDuplex":
            content_data = {
                "version": self.version,
                "topic": "cloud.speech.trans",
                "mid": str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) + "mid")),
                "id": f"{self.deviceId}",
                "sn": self.sn,
                "clientId": f"{self.clientid}",
                "category": "AC",
                "request": {
                    "apiVer": "1.0.0",
                    "sessionId": str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) + "sessionId")),
                    "recordId": str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) + "recordId")),
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
        else:
            content_data = {
                "version": self.version,
                "topic": "cloud.speech.trans",
                "mid": str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) + "mid")),
                "id": "%s" % self.deviceId,
                "category": "AC",
                "request": {
                    "apiVer": "1.0.0",
                    "sessionId": str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) + "sessionId")),
                    "recordId": str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time()) + "recordId")),
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
        return content_data
