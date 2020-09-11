import base64
import glob
import os
import uuid
import websocket
from websocket import ABNF
from threading import Thread
import time, json
import sys


class SbcWebSocketApp():
    def __init__(self, datalist, callbadk=None):
        self.ws = None
        self.file = None
        self.datalist = datalist
        self.callbadk = callbadk
        self.step = 3200
        self.dir = ''
        self.type='sbc'

    def on_message(self, message):
        mJson = json.loads(message)
        text = ''
        if 'eof' in message:
            text = mJson['text']
            text = text.replace(" ", "")
        print(self.file, text)
        if self.callbadk:
            self.callbadk({'filename':os.path.basename(self.file),'text':text,'type':self.type})

    def sendWavData(self, file):
        uuid_value = str(uuid.uuid1()).replace('-', '')
        content = { "topic": "recorder.stream.start", "recordId": uuid_value, "sessionId": uuid_value,
                   "audio": {
                       "audioType": "wav",
                       "sampleRate": 16000,
                       "channel": 1,
                       "sampleBytes": 2
                   },
                   "asrParams": {
                       "enableVAD": False,
                       "realBack": False,
                       "toneEnable": True,
                       "res": ""
                   }
                   }
        content['sessionId'] = os.path.basename(file)
        self.ws.send(json.dumps(content))
        with open(file, 'rb') as f:
            while True:
                wave_data = f.read(self.step)
                if wave_data:
                    self.ws.send(wave_data, ABNF.OPCODE_BINARY)
                if len(wave_data) < self.step:
                    break
                time.sleep(0.1)
        self.ws.send('', ABNF.OPCODE_BINARY)
        time.sleep(0.2)

    def readFile(self):
        # input_dir = self.dir + r'\*.wav'
        # list_im = glob.glob(input_dir)
        for file in self.datalist:
            yield file
        yield None

    def on_open(self):
        def run(*args):
            fileFun = self.readFile()
            while True:
                self.file = fileFun.__next__()
                if self.file:
                    # if self.file != r'D:\soft\wav\20200831_wav\fed475bb410e079478fba67417efe3b7_20200831123531_bc1ced45-8bd3-4e71-9ac7-70c592ec2e30.wav':
                    #     continue
                    self.sendWavData(self.file)
                else:
                    break
            print("Thread terminating...")
            # self.ws.close()

        # run()
        Thread(target=run).start()

    def start(self):
        url = 'wss://dds-hb.dui.ai/dds/v1/test?serviceType=websocket&productId=278580818'
        self.ws = websocket.WebSocketApp(url)
        self.ws.on_open = self.on_open
        self.ws.on_message = self.on_message
        self.ws.run_forever()
#
class SbcClient():
    def __init__(self):
        self.ws = None
        self.file = None

        self.url = 'wss://dds-hb.dui.ai/dds/v1/test?serviceType=websocket&productId=278580818'
        self.step = 3200



    def run(self, whole_wav_path):
        url = self.url
        ws = websocket.create_connection(url)
        result = self.sendData(ws, whole_wav_path)
        ws.close()

        return {'filename':os.path.basename(whole_wav_path),'type':'sbc','text':result}

    def sendData(self, ws, wav_path):
        uuid_value = str(uuid.uuid1()).replace('-', '')
        content = {"topic": "recorder.stream.start", "recordId": uuid_value, "sessionId": uuid_value,
                   "audio": {
                       "audioType": "wav",
                       "sampleRate": 16000,
                       "channel": 1,
                       "sampleBytes": 2
                   },
                   "asrParams": {
                       "enableVAD": False,
                       "realBack": False,
                       "toneEnable": True,
                       "res": ""
                   }
                   }
        content['sessionId'] = os.path.basename(wav_path)
        ws.send(json.dumps(content))
        with open(wav_path, 'rb') as f:
            while True:
                wave_data = f.read(self.step)
                if wave_data:
                    ws.send(wave_data, ABNF.OPCODE_BINARY)
                if len(wave_data) < self.step:
                    break
                time.sleep(0.1)
        ws.send('', ABNF.OPCODE_BINARY)
        time.sleep(0.1)
        result=ws.recv()
        return self.on_message(result)

    def on_message(self, message):
        text = ''
        lanuage_value = ''
        mJson = json.loads(message)
        text = ''
        if 'eof' in message:
            text = mJson['text']
            text = text.replace(" ", "")
        print(self.file, text)
        return text
if __name__ == "__main__":
    # dir = r'D:\soft\wav\20200831_wav'
    # ws = websocket.WebSocketApp(url)
    # a = app(ws, dir)
    # ws.on_open = a.on_open
    # ws.on_message = a.on_message
    # ws.run_forever()
    # wst.save('result_1.xlsx')
    sbc=SbcClient()
    t=sbc.run('/home/kangyong/Data/wav/e86c7e26-7716-4fea-9406-501fe4621d35_20200831131932_801775b8-513a-4513-b3ff-4b3f7f9fdd6b.wav')
    print(t)
