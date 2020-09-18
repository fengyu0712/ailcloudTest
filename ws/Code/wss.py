import websocket,json
from gevent import os
from websocket import ABNF

url = 'wss://hn.dui.ai/dds/v1/test?serviceType=websocket&productId=278575321' #websocket连接地址
ws = websocket.create_connection(url)  #创建连接
import socket
from websocket import create_connection, WebSocket
class MyWebSocket(WebSocket):
    # def __init__(self,url):
    def recv_frame(self):
        frame = super().recv_frame()
        print('yay! I got this frame: ', frame)
        return frame
    def send(self, data):
        send_frame=super().send()
        return send_frame
    def recv(self):
        recv_data=super().recv()

ws = create_connection("ws://echo.websocket.org/",
                        sockopt=((socket.IPPROTO_TCP, socket.TCP_NODELAY, 1),), class_=MyWebSocket)

content = {
    "topic": "recorder.stream.start",
    "recordId": "21354578ijhgbvdrt35",
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
if ws.connected:
    ws.send(json.dumps(content))
    r1=ws.recv()
    print(r1)
    step = 3200 #如果audioType是wav，此处需要修改为3200
    with open("E:\ws\\test_audio\\002M30_36_010001.wav",'rb') as a:
        data = a.read(step)
        print(data)
    ws.send(data, ABNF.OPCODE_BINARY)
    r2=ws.recv_data()
    print(r2)
# text=json.loads(b)["text"]
# print(text)
ws.close()