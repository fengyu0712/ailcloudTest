# coding: utf-8
import time
from websocket import ABNF
import websocket, time, json, os, gc
from config import base_path,host
from devices_info import Deviceset
import os
from tools.get_log import GetLog
log=GetLog.get_logger()  # 初始化日志对象

class Mywebscoket():
    # rootpath: 音频名称
    # termianl_type : 终端类型
    # is_need_devices_status : 表示为需要获取设备信息
    def __init__(self,rootpath,terminal_type):
        self.wavpath = os.path.join(base_path+os.sep+"audio_file"+os.sep,rootpath+".wav")
        self.address = host
        self.step = 3200
        self.headers = Deviceset(terminal_type).headers

    def get_time_stamp(self):
        ct = time.time()
        local_time = time.localtime(ct)
        data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        data_secs = (ct - int(ct)) * 1000
        time_stamp = "%s.%03d" % (data_head, data_secs)
        return time_stamp

    def start_websocket(self):
        if not os.path.exists(self.wavpath):
            log.info("{}路径不存在".format(self.wavpath))
            return ""
        log.info("开始ws的链接")
        ws = websocket.create_connection(self.address, timeout=30)
        log.info("建立ws的链接")
        try:
            result_asr = self.send_data(ws, self.wavpath)  # 获取预期结果
            log.info("ws接口返回的信息为:{}".format(result_asr))
            gc.collect()
            ws.close()

        except Exception as e:
            log.error("错误信息信息为:{}".format(e))
            result_asr={}
        finally:
            gc.collect()
            ws.close()
            log.info("ws链接关闭")
            return result_asr

    def send_data(self, ws, wav_path):
        try:
            log.info("开始发送头部数据......................")
            for key in self.headers:
                ws.send(json.dumps(key), ABNF.OPCODE_TEXT)
                time.sleep(0.1)
            log.info("开始发送音频数据......................")
            with open(wav_path, 'rb') as f:
                while True:
                    data = f.read(self.step)
                    if data:
                        ws.send(data, ABNF.OPCODE_BINARY)
                    if len(data) < self.step:
                        break
                    time.sleep(0.1)
            ws.send('', ABNF.OPCODE_BINARY)
            result = self.get_message(ws)
            return result
        except Exception as e:
            log.info("发送音频数据异常,原因:{}".format(e))
            ws.close()

    def get_message(self, ws):
        try:
            log.info("开始接收数据......................")
            mid=""
            result_dict={"login":{},"asr":{},"nlg":{}}
            i = 0
            while (i<5):
                result = ws.recv()
                result=result.replace("false","False").replace("true","True")
                if "cloud.online.reply" in result:
                    log.info("接收的online信息为:{}".format(result))
                    result_dict['login']=eval(result)
                elif "cloud.speech.trans.ack" in result:
                    log.info("接收的cloud.speech.trans.ack信息为:{}".format(result))
                    result_dict["asr"]=eval(result)
                elif "cloud.speech.reply" in result:
                    log.info("接收的cloud.speech.reply信息为:{}".format(result))
                    nlg_result=eval(result)
                    result_dict["nlg"]=nlg_result
                    #mid=nlg_result.get("mid")
                    break
                time.sleep(0.1)
                i = i + 1
        except Exception as e:
            result_dict["error"]=e
            log.error("错误信息信息为:{}".format(e))

        return result_dict

if __name__ == '__main__':
    '''
    Mywebscoket("打开卧室空调.wav", 1)
    time.sleep(2)
    Mywebscoket("我回来了.wav", 1)

    '''
    result = Mywebscoket('打开空调', "yuyintie_1").start_websocket()
    print(result)

    result = Mywebscoket('打开空调', "yuyintie_1").start_websocket()
    print(result)
    #result = Mywebscoket("我回来了.wav", "328").start_websocket()
    #print(result)
