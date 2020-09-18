# -*- coding: UTF-8 -*-
import os,sys
#获取绝对路径，以便shell脚本跑
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import xlrd
import winsound
import time
import datetime
import serial
import serial.tools.list_ports
from conf import path
from Code.common import log
from xlutils.copy import copy

'''
串口端打印ASR
脚本控制本地唤醒词音频播放——判断是否唤醒成功——唤醒成功，则播放音频语料（如果没有唤醒成功，则再次播放唤醒音频，直到唤醒成功为止）——读取串口端打印的ASR结果——将此ASR结果和期望值比较——完全一样，pass。不一样，fail。
需要注意的是：1.要统计播放唤醒音频测试；2.需要统计唤醒成功次数；3.需要打印唤醒成功率；4.需要打印识别成功率。
'''

# 全局变量
wakeup_path = path.audio_path+"002M30_36_010005.wav"   # #唤醒文件：你好小美的音频文件
cmd_path = path.audio_path   #需要执行的，音频文件
now = time.strftime('%Y-%m-%d-%H-%M')
# log_path = path.log_path+now+".txt"   #日志文件
# fileObject = open(log_path, 'a+')   # 记录日志信息

cntWkSucc = 0
totalWk = 0
cntWkFail = 0   #唤醒失败次数
ratioWk = 0.0   #唤醒成功率



#定义日志
Log=log.Logger()

# 查询可用串口
def query():
    plist = list(serial.tools.list_ports.comports())
    if len(plist) <= 0:
        Log.warning("The Serial port can't find!")
        return None
    else:
        # plist_0 =list(plist[0])
        # serialName = plist_0[0]
        serialName="COM5"
        serialFd = serial.Serial(serialName,9600,timeout = 60)
        Log.info("check which port was really used >"+serialFd.name)
    return serialFd

# 打开串口
def open_interface(serialFd):
    if serialFd.isOpen():
        Log.info("Serial port open success")
    else:
        Log.error("Serial port open failed")


# 唤醒小美,读取音频文件
def  wakeup_File(serialFd):
    global totalWk,cntWkSucc,cntWkFail
    iswake=False
    if (os.path.exists(wakeup_path)):
         totalWk = totalWk + 1
         print(totalWk)
         winsound.PlaySound(wakeup_path, winsound.SND_FILENAME)
         time_stamp = datetime.datetime.now()
         # fileObject.write("\n")
         # fileObject.write(time_stamp.strftime('%Y.%m.%d-%H:%M:%S'))
         # # fileObject.write("\n")
         time.sleep(1)
         try:
            is_wakeup= recvWakeup(serialFd)
         except Exception as e:
             Log.error(e)
         else:
             if is_wakeup == True:
                 cntWkSucc =cntWkSucc+1
                 iswake=True
             else:
                cntWkFail=cntWkFail+1
                iswake=wakeup_File(serialFd)
         return iswake
    else:
        Log.warning("唤醒的音频文件不存在..." + wakeup_path)
        return False


def recvWakeup(serial):
    txt = 'xiaomei'
    i = 0
    # 5秒内收到数据
    new_data=""
    while i < 50:
        data = serial.read_all()
        if len(data) == 0:
            # continue
            time.sleep(0.1)
            i += 1
        elif isinstance(data,bytes):
            Log.info(data)
            try:
                # new_data = bytes.decode(data)
                new_data=data.decode()
            except Exception as e:
                Log.error("解析出错："+e)
                new_data=''
            else:
                Log.info(new_data)
            break

    ret=new_data.find(txt)
    if ret != -1:
        Log.info('wakeup success')
        return True
    else:
        Log.warning('wakeup failure')
        return False

def run_test():
    serialFd = query()  # 查询是否有插入串口
    if serialFd!=None:
        open_interface(serialFd)
    while (True):
        issucess = wakeup_File(serialFd)  # 唤醒小美
        Log.info("唤醒总数：" + str(totalWk))
        Log.info("唤醒成功次数：" + str(cntWkSucc))
        ratioWk = (cntWkSucc / totalWk) * 100
        ratioWk_value = "{:.2f}%".format(ratioWk)
        Log.info("唤醒成功率：" + str(ratioWk_value))


# def run_shibie():
#     serialFd = query()  # 查询是否有插入串口
#     if serialFd != None:
#         open_interface(serialFd)
#         wakeup_File(serialFd)
#         read_excel(serialFd)
if __name__ == "__main__":
    run_test()

    # serialFd=query()   # 查询是否有插入串口
    # if serialFd!=None:
    #     open_interface(serialFd)
    #     while(True):
    #     #for i in range(2):
    #         issucess = wakeup_File(serialFd)  # 唤醒小美
    #         # fileObject.write("唤醒总数："+str(totalWk)+"\n")
    #         # print("唤醒总数："+str(totalWk))
    #         # fileObject.write("唤醒成功次数：" + str(cntWkSucc)+"\n")
    #         # print("唤醒成功次数：" + str(cntWkSucc))
    #         # ratioWk = (cntWkSucc / totalWk) * 100
    #         # ratioWk_value = "{:.2f}%".format(ratioWk)
    #         # fileObject.write("唤醒成功率：" + str(ratioWk_value)+"\n")
    #         # print("唤醒成功率：" + str(ratioWk_value))
    #         issucess = wakeup_File(serialFd)  # 唤醒小美
    #         Log.info("唤醒总数：" + str(totalWk))
    #         Log.info("唤醒成功次数：" + str(cntWkSucc))
    #         ratioWk = (cntWkSucc / totalWk) * 100
    #         ratioWk_value = "{:.2f}%".format(ratioWk)
    #         Log.info("唤醒成功率：" + str(ratioWk_value))







