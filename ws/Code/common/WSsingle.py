import websocket
from websocket import ABNF
import time
import json
product_id = '278575321' #填入产品Id
apikey = 'x' #填入apikey
data0={
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

class WsSingle:
    def __init__(self,url):
        self.ws = websocket.create_connection(url)  # 创建连接
        pass
    def runsingle(self,wavfile,data=None,step=None):
        if data is None:
            data=data0
        if step is None:  # 如果audioType是wav，此处需要修改为3200
            step=3200
        self.ws.send(json.dumps(data0))
        with open(wavfile, 'rb') as f:
            while True:
                data2 = f.read(step)
                if data2:
                    self.ws.send(data2, ABNF.OPCODE_BINARY)
                if len(data2) < step:
                    break
                time.sleep(0.1)
        self.ws.send('', ABNF.OPCODE_BINARY)
        result=self.ws.recv()
        return result
    def close(self):
        self.ws.close()



from multiprocessing import Process, Value

url = 'wss://dds-hb.dui.ai/dds/v1/test?serviceType=websocket&productId=278575321'
wavfile1="E:\ws\\test_audio\\002M30_36_010001.wav"
wavfile2="E:\ws\\test_audio\\002M30_36_010002.wav"

if __name__ == "__main__":
    ws=WsSingle(url)
    start = time.clock()
    a=ws.runsingle(wavfile1)
    b=ws.runsingle(wavfile2)
    ws.close()
    time = time.clock() - start
    print(a, b,start, time)

