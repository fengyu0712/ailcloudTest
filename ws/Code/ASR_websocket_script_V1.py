#!/usr/bin/env python
# coding=utf-8
### websocket模块https://pypi.python.org/pypi/websocket-client
### wavfile是一个speex压缩的ogg文件,文件格式是Ogg data, Speex audio
import websocket
from gevent import os
from websocket import ABNF
import time
import _thread
import json
import xlrd
from xlutils.copy import copy
product_id = '278575321' #填入产品Id
apikey = 'x' #填入apikey
# url = 'wss://hn.dui.ai/dds/v1/test_audio?serviceType=websocket&productId='+product_id
url = 'wss://hn.dui.ai/dds/v1/test?serviceType=websocket&productId=278575321' #websocket连接地址
# url = 'wss://speech-test_audio.ainirobot.com:7016/dds/v1/test_audio?serviceType=websocket&productId='+product_id
excel_path="E:\ws\\test_date\case.xlsx"
result_path="E:\ws\\test_date\case.xlsx"
# result_path="E:/ws/AI云端ASR测试用例执行结果1.xlsx"
#音频文件路径
# cmd_path="E:/ws/002M30_36"
cmd_path = "E:\ws\\test_audio"  #需要执行的，音频文件
sheetName="002M30_36"

# 获取数据
data = xlrd.open_workbook(excel_path)
# 获取sheet
table = data.sheet_by_name(sheetName)

# 获取总行数
nrows =table.nrows
index=2
except_value=""  #预期结果
print("nows:"+ str(nrows))


success_total=0
fail_total=0
total=0


def on_message(ws, message):
   print ('Message>>>>>>>>>>>>>>>>>>>>>>>>')
   print(message)
   mJson = json.loads(message)
   if 'eof' in message:
       text = mJson['text']
       global index,success_total,fail_total,total

       print(index)
       print("返回值:",text)
       text=str(text).replace(' ', '')
       print(text)
       table.put_cell(index, 2, 1, text, format)
       total=total+1
       except_value = table.cell(index, 1).value
       print("期望：",except_value)
       if(except_value==text):
           table.put_cell(index , 3, 1, str(True), format)
           success_total=success_total+1
       else:
           table.put_cell(index , 3, 1, str(False), format)
           fail_total=fail_total+1
       index = index + 1
       if (index == nrows) :
           sucess_rate=(success_total / total) * 100
           sucess_rate_value="{:.2f}%".format(sucess_rate)
           table.put_cell(0, 1, 1, sucess_rate_value, format)
           wb = copy(data)
           wb.save(result_path)
   print ('Message<<<<<<<<<<<<<<<<<<<<<<<<')

def on_error(ws, error):
    print ('error>>>>>>>>>>>>>>>>>>>>>>')
    print (error)
    wb = copy(data)
    wb.save(result_path)
    print ('error<<<<<<<<<<<<<<<<<<<<<<')

def on_close(ws):
    print ("### closed ###")
# def on_data(ws, resp, datatype, ctnu):
#     print datatype

def on_open(ws):
    def run(*args):
        for i in range(index, nrows):
            wav_value = table.cell(i, 0).value  # wav文件值
            if wav_value.strip() == '':
                continue
            wav_value=sheetName+"_"+wav_value+".wav"
            print("aaaaaaa"+wav_value)
            wav_path = cmd_path + "/" + wav_value  # wav 路径
            if (os.path.exists(wav_path) == False):
                continue

            except_value = table.cell(i, 1).value  # 预期结果值
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
            ws.send(json.dumps(content))
            step = 3200 #如果audioType是wav，此处需要修改为3200
            with open(wav_path, 'rb') as f:
                while True:
                    data = f.read(step)
                    if data:
                        ws.send(data, ABNF.OPCODE_BINARY)
                    if len(data) < step:
                        break
                    time.sleep(0.1)
            ws.send('', ABNF.OPCODE_BINARY)
            time.sleep(1)
    _thread.start_new_thread(run, ())

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()