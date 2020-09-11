import base64
import datetime
import glob
import hashlib
import os
import uuid

import websocket
from websocket import ABNF, WebSocketApp
from threading import Thread
import time, json
import sys

import openpyxl

wst = openpyxl.Workbook()
sheet = wst.create_sheet('result', -1)

url = 'wss://wsapi.xfyun.cn/v1/aiui'


class XfWebSocketApp():
    def __init__(self, url, dir):
        self.ws = None
        self.file = None
        self.use_scene = "main_box"
        self.APIKEY = "b1c9db5797d7bd16567bb2e6a34cf075"
        self.APPID = "5e017c12"
        self.PARAM = {'result_level': 'plain', 'auth_id': '894c985bf8b1111c6728db79d3479aef', 'data_type': 'audio',
                      'aue': 'raw', 'scene': 'main_box', 'sample_rate': '16000'}
        self.URL = "wss://wsapi.xfyun.cn/v1/aiui"
        self.END_FLAG = "--end--"
        self.ws = None
        self.step=3200

    def getHandShakeParams(self):
        temp_data = base64.b64encode(bytes(json.dumps(self.PARAM), 'utf-8'))
        paramBase64 = temp_data.decode(encoding='utf-8', errors='ignore')
        curtime = str(time.time()).split(".")[0]
        signtype = "sha256"
        originStr = self.APIKEY + curtime + paramBase64
        checksum = self.sha256hex(originStr)
        handshakeParam = "?appid=" + self.APPID + "&checksum=" + checksum + "&curtime=" + curtime + "&param=" + paramBase64 + "&signtype=" + signtype
        return handshakeParam

    def sha256hex(self, data):
        sha256 = hashlib.sha256()
        sha256.update(data.encode())
        res = sha256.hexdigest()
        return res

    def on_message(self, message):
        text=None
        if (message == "音频为空"):
            text = "音频为空"
        else:
            mJson = json.loads(message)
            resultid = mJson['data']['result_id']
            if resultid == 1:
                text = str(mJson['data']['text']).strip().lower().replace(" ", "")
                # print("返回的asr测试结果", text)
                # 获取语种信息
                accent_dict = mJson['data']['json_args']
                lanuage_value = accent_dict["accent"]
                isright = False
                except_value = ""
                # print(mJson)
        # print(message)

        sheet.append([os.path.basename(self.file), text])

    def sendWavData(self, file):
        with open(file, 'rb') as f:
            while True:
                data = f.read(self.step)
                if data:
                    self.ws.send(data, ABNF.OPCODE_BINARY)
                if len(data) < self.step:
                    break
                time.sleep(0.1)
            self.ws.send(self.END_FLAG, ABNF.OPCODE_BINARY)
        time.sleep(0.2)

    def on_open(self):
        def run(*args):
            # fileFun = self.readFile()

            url = 'wss://wsapi.xfyun.cn/v1/aiui'
            self.ws.url = url + self.getHandShakeParams()
            self.sendWavData(self.file)
            # print("Thread terminating...")
            self.ws.close()

        # run()
        Thread(target=run).start()

    def start(self):
        url = 'wss://wsapi.xfyun.cn/v1/aiui'
        current_url = url + self.getHandShakeParams()
        self.ws = websocket.WebSocketApp(current_url)
        self.ws.on_open = self.on_open
        self.ws.on_message = self.on_message
        self.ws.run_forever()
class XfClient():
    def __init__(self):
        self.ws = None
        self.file = None
        self.use_scene = "main_box"
        self.APIKEY = "b1c9db5797d7bd16567bb2e6a34cf075"
        self.APPID = "5e017c12"
        self.PARAM = {'result_level': 'plain', 'auth_id': '894c985bf8b1111c6728db79d3479aef', 'data_type': 'audio',
                      'aue': 'raw', 'scene': 'main_box', 'sample_rate': '16000'}

        self.url = "wss://wsapi.xfyun.cn/v1/aiui"
        self.END_FLAG = "--end--"
        self.ws = None
        self.step = 3200

    def getHandShakeParams(self):
        temp_data = base64.b64encode(bytes(json.dumps(self.PARAM), 'utf-8'))
        paramBase64 = temp_data.decode(encoding='utf-8', errors='ignore')
        curtime = str(time.time()).split(".")[0]
        signtype = "sha256"
        originStr = self.APIKEY + curtime + paramBase64
        checksum = self.sha256hex(originStr)
        handshakeParam = "?appid=" + self.APPID + "&checksum=" + checksum + "&curtime=" + curtime + "&param=" + paramBase64 + "&signtype=" + signtype
        return handshakeParam

    def sha256hex(self, data):
        sha256 = hashlib.sha256()
        sha256.update(data.encode())
        res = sha256.hexdigest()
        return res

    def run(self, whole_wav_path):
        url = self.url + self.getHandShakeParams()
        ws = websocket.create_connection(url)
        result = self.sendData(ws, whole_wav_path)
        ws.close()

        return {'filename':os.path.basename(whole_wav_path),'type':'xf','text':result}

    def sendData(self, ws, wav_path):
        with open(wav_path, 'rb') as f:
            while True:
                data = f.read(self.step)
                if data:
                    ws.send(data, ABNF.OPCODE_BINARY)
                if len(data) < self.step:
                    break
                time.sleep(0.1)
        ws.send(self.END_FLAG, ABNF.OPCODE_BINARY)
        while True:
            result = ws.recv()
            if 'iat' in result:
                break
        return self.on_message(result)

    def on_message(self, message):
        text = ''
        lanuage_value = ''
        if (message == "音频为空"):
            text = "音频为空"
        else:
            mJson = json.loads(message)
            resultid = mJson['data']['result_id']
            if resultid == 1:
                text = str(mJson['data']['text']).strip().lower().replace(" ", "")
                # 获取语种信息
                accent_dict = mJson['data']['json_args']
                lanuage_value = accent_dict["accent"]
        return text
if __name__ == "__main__":
    # dir = r'D:\soft\wav\20200831_wav'
    # input_dir = dir + r'\*.wav'
    # list_im = glob.glob(input_dir)
    # for file in list_im:
    #     a=XfWebSocketApp(url,dir)
    #     whole_wavpath = r'D:\soft\wav\20200831_wav\372a6120-c75c-4fc0-955f-b12f7774ba82_20200831122858_0af7bfa0-25cb-48c6-bf51-a509bb953315.wav'
    #     a.file=file
    #     a.start()
    # wst.save('result_1_2_xf.xlsx')
    # for i in range(3):
    #     xf = XfLogConnectClient()
    #     xf.start()
    socket = XfClient()
    whole_wavpath = r'/home/kangyong/Data/wav/993ea1f5-5558-43e4-9baa-c9b043534e2b_20200831204743_8fa3168e-4840-4f52-b16a-0b88801bc08a.wav'
    result = socket.run(whole_wavpath)
    print(result)