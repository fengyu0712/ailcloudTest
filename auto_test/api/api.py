# coding: utf-8
from scripts.init_env import http_host
import os
import requests
from tools.mylog import Logger
from urllib import parse

log = Logger()  # 初始化日志对象


class Api:
    # 初始化
    def __init__(self):
        pass

    # 查询方法
    def _get(self):
        pass

    # 新增方法,获取设备状态
    def post(self, mid):
        try:
            headers = {"Content-Type": "application/json "}
            self.params = {"mid": "%s" % mid}
            device_host = http_host + "/v1/common/device/getDeviceStatus"
            log.info("获取设备状态,请求参数为:{},地址:{}".format(self.params, device_host))
            jsonvalue = requests.post(device_host, json=self.params, headers=headers).json()
            log.info("获取设备状态信息:{}".format(jsonvalue))
            return jsonvalue
        except Exception as e:
            print(e)
            log.info("获取设备状态异常:{}".format(e))
            return {}

    def open_api(self, data):
        # headers = {"Content-Type": "application/x-www-form-urlencoded"}

        device_host = http_host + "/v1/base2pro/data/transmit"
        log.info(f"open_api测试,请求参数为:{data},地址:{device_host}")
        try:
            response = requests.post(device_host, params=parse.urlencode(data))
            jsonvalue = response.json()
        except Exception as e:
            raise e
        else:
            log.info("open_api接口返回信息:{}".format(jsonvalue))
            return jsonvalue


if __name__ == '__main__':
    # jsonvalue = Api().post("b41572f563e011ebb48598e7f4f1e716")
    # print(jsonvalue)
    # data = {"serviceUrl": "/v1/device/speech/fullDuplex",
    #         "data": {"deviceId": 3298544982176, "fullDuplex": 1,
    #                  "fullDuplexSkillConfig": [{"skillId": "midea-deviceControl", "timeOut": "10"}]}}
    # data = {"serviceUrl": "/v1/tts/voice/set",
    #         "data": {"deviceId":"3298544982176","voiceId":"xiyaof"}}
    data = {'serviceUrl': '/v1/accent/set',
            'data': {'deviceId': '160528698598412', 'accentId': 'cantonese', 'enableAccent': '1',
                     'mixedResEnable': '1'}}
    r = Api().open_api(data)
    print(r)

