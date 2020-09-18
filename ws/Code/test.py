#!/usr/bin/env python
# coding=utf-8
### websocket模块https://pypi.python.org/pypi/websocket-client
### wavfile是一个speex压缩的ogg文件,文件格式是Ogg data, Speex audio
import websocket
from gevent import os
from websocket import ABNF
from threading import Thread
import time
import _thread
import json
import xlrd
from xlutils.copy import copy
product_id = '278575321' #填入产品Id
apikey = 'x' #填入apikey

from multiprocessing import Process, Value

# sit环境执行地址
# 地址修改为：dds-hb.dui.ai
#后续你们测试的环境从hn.dui.ai迁到dds-hb.dui.ai，由于我们内部集群的迁移，华南环境今晚下线了@何胖橙子
url = 'wss://dds-hb.dui.ai/dds/v1/test?serviceType=websocket&productId='+product_id

# 旧地址
#url = 'ws://dds.dui.ai/dds/v1/test?serviceType=websocket&productId='+product_id
wavfile1="E:\ws\\test_audio\\002M30_36_010001.wav"
class Mywss(websocket.WebSocketApp):
    def data(self,wavfile):
        self.wavfile=wavfile
    def creat_connect(self,url):
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(url,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        return self.ws
    def on_message(self, message):
        print('Message>>>>>>>>>>>>>>>>>>>>>>>>')
        print(message)
        mJson = json.loads(message)
        text = ""
        if 'eof' in message:
            text = mJson['text']
            print(text.replace(" ", ""))

        print('Message<<<<<<<<<<<<<<<<<<<<<<<<')

    def on_error(self, error):
        print('error>>>>>>>>>>>>>>>>>>>>>>')
        print(error)
        print('error<<<<<<<<<<<<<<<<<<<<<<')

    def on_close(self):
        print("### closed ###")

    # def on_data(ws, resp, datatype, ctnu):
    #     print datatype

    def on_open(self,ws):
        def run(*args):
            content = {
                "topic": "recorder.stream.start",
                "recordId": "21354578ijhgbvdrt33",
                "sessionId": "testaasdfas2333666",
                "audio": {
                    "audioType": "wav",
                    "sampleRate": 16000,
                    "channel": 1,
                    "sampleBytes": 2
                },
                "asrParams": {
                    "enableVAD": False,
                    "realBack": False,
                    "toneEnable": True
                },
                "aiType": "asr"
            }
            ws.send(json.dumps(content))
            step = 3200  # 如果audioType是wav，此处需要修改为3200
            with open(self.wavfile, 'rb') as f:
                while True:
                    data = f.read(step)
                    if data:
                        ws.send(data, ABNF.OPCODE_BINARY)
                    if len(data) < step:
                        break
                    time.sleep(0.1)

            ws.send('', ABNF.OPCODE_BINARY)
            # print("结束")
            time.sleep(5)
            ws.close()

        _thread.start_new_thread(run, ())

    def func_one(self):
        websocket.enableTrace(True)
        w=self.data(wavfile1)
        ws = websocket.WebSocketApp(url,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        ws.on_open = self.on_open
        ws.run_forever()

if __name__ == "__main__":

    Mywss(url).func_one()
