# coding: utf-8

from websocket import ABNF
import websocket, time, json, gc
from config import base_path
from devices_info_1 import Deviceset
import os
from tools.get_log import GetLog
from tools.mylog import Logger
from scripts.init_env import host, current_env

log = Logger()  # 初始化日志对象

#重试装饰器
def retry(rerun_count):
    def wrapper(request):
        def inner_wrapper(*args, **kwargs):
            nonlocal rerun_count
            for i in range(rerun_count):
                try:
                    response=request(*args, **kwargs)
                except Exception as e:
                    if i ==rerun_count-1:
                        raise e
                    else:
                        print(f"第{i}次请求失败")
                else:
                    return response
        return inner_wrapper
    return wrapper

class AiCloud():
    # rootpath: 音频名称
    # termianl_type : 终端类型
    # is_need_devices_status : 表示为需要获取设备信息
    def __init__(self, terminal_type, env=None):
        # if env==None:
        #     env=current_env
        print("测试环境细腻系：", current_env)
        self.address = host
        # self.address = "wss://link-mock.aimidea.cn:10443/cloud/connect"
        print("当前测试环境为:", host)
        self.step = 3200
        self.terminal_type = terminal_type
        # self.headers = Deviceset(terminal_type).headers
        self.ws=self.client_ws()

    @retry(rerun_count=3)
    def client_ws(self):
        log.info("开始ws的链接")
        ws = websocket.create_connection(self.address, timeout=30)
        log.info("建立ws的链接成功")
        return ws

    def on_line(self):
        try:
            # 开始云端上线
            print(Deviceset(self.terminal_type).online_data())
            self.ws.send(json.dumps(Deviceset(self.terminal_type).online_data()), ABNF.OPCODE_TEXT)
            # 开始上报设备音量信息
            self.ws.send(json.dumps(Deviceset(self.terminal_type).audio_staus_data()), ABNF.OPCODE_TEXT)
            # 开始上报设备OTA信息
            self.ws.send(json.dumps(Deviceset(self.terminal_type).ota_check()), ABNF.OPCODE_TEXT)
        except Exception as e:
            self.ws.close()
            raise (f"错误信息信息为:{e}")
        else:
            return self.ws

    @retry(rerun_count=3)
    def send_data(self, rootpath):
        self.wavpath = os.path.join(base_path + os.sep + "audio_file" + os.sep, rootpath + ".wav")
        if not os.path.exists(self.wavpath):
            raise ("{}路径不存在".format(self.wavpath))
        try:
            # 发送头部信息
            self.ws.send(json.dumps(Deviceset(self.terminal_type).content_data()), ABNF.OPCODE_TEXT)
            log.info("开始发送音频数据......................")
            with open(self.wavpath, 'rb') as f:
                while True:
                    data = f.read(self.step)
                    if data:
                        self.ws.send(data, ABNF.OPCODE_BINARY)
                    if len(data) < self.step:
                        break
                    time.sleep(0.1)
            self.ws.send('', ABNF.OPCODE_BINARY)
            result = self.get_message()
            gc.collect()
            return result
        except Exception as e:
            log.info("发送音频数据异常,原因:{}".format(e))
            self.ws.close()

    def close(self):
        self.ws.close()
        log.info("ws链接关闭")

    def get_message(self):
        result_dict = {"login": {}, "asr": {}, "nlg": {}}
        try:
            log.info("开始接收数据......................")
            i = 0
            while (i < 5):
                result = self.ws.recv()
                result = result.replace("false", "False").replace("true", "True")
                if "cloud.online.reply" in result:
                    log.info("接收的online信息为:{}".format(result))
                    result_dict['login'] = eval(result)
                elif "cloud.speech.trans.ack" in result:
                    log.info("接收的cloud.speech.trans.ack信息为:{}".format(result))
                    result_dict["asr"] = eval(result)
                elif "cloud.speech.reply" in result:
                    log.info("接收的cloud.speech.reply信息为:{}".format(result))
                    nlg_result = eval(result)
                    result_dict["nlg"] = nlg_result
                    # mid=nlg_result.get("mid")
                    break
                time.sleep(0.1)
                i = i + 1
        except Exception as e:
            result_dict["error"] = e
            log.error("错误信息信息为:{}".format(e))

        return result_dict


if __name__ == '__main__':
    aiyuncloud = AiCloud("328_halfDuplex")
    aiyuncloud.on_line()
    result = aiyuncloud.send_data('打开净化器')
    print(result)
    # result = aiyuncloud.send_data('音量设为一档')
    # pass
    # print(result)
    # result = aiyuncloud.send_data('当前音量是多少')
    # print(result)
    # result = aiyuncloud.send_data('音量设为百分之六十五')
    # print(result)
    # result = aiyuncloud.send_data('当前音量是多少')
    # print(result)
    # result = aiyuncloud.send_data('音量调小一点')
    # print(result)
    # result = aiyuncloud.send_data('当前音量是多少')
    # print(result)
    # result = aiyuncloud.send_data('音量设为百分之一百二')
    # print(result)
    # result = aiyuncloud.send_data('当前音量是多少',)
    # print(result)
