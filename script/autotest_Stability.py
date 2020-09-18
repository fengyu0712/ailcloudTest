# -*- coding: UTF-8 -*-
import xlrd
import os
import winsound
import time
import datetime
import serial
import serial.tools.list_ports
from xlutils.copy import copy

'''
稳定性测试
1、记录串口日志
2、循环播放小美小美和命令词
'''

# 全局变量
wakeup_path = "008M27_08_42_0001.wav"   # #唤醒文件：你好小美的音频文件
cmd_path = "./audio/"  #需要执行的，音频文件
log_path = 'E:/log.txt'   #日志文件
#持续执行时间，单位为秒.
# 24 小时=86400
exeute_time=60


def write_file(path, lines, mode='a+'):
    with open(path, mode) as f:
        f.writelines(lines)


def play_audio():
    startTime = datetime.datetime.now()  # 开始时间
    print("开始执行:%s"%startTime)
    is_end = False
    listinfo=os.listdir(cmd_path)
    while(True):
        for wav_value in listinfo:
            endTime = datetime.datetime.now()
            reponse_time = (endTime - startTime).total_seconds()
            if reponse_time >= exeute_time:
                is_end = True
                print("执行结束:%s" % endTime)
                print("共执行:%s时间" % reponse_time)
                break

            wav_path=cmd_path+"/"+wav_value   # wav 路径
            if not os.path.exists(wav_path):
                continue

            winsound.PlaySound(wakeup_path, winsound.SND_FILENAME)
            time.sleep(1)   # 间隔1.
            winsound.PlaySound(wav_path, winsound.SND_FILENAME)
            time.sleep(1)  # 间隔1.

        if is_end:
            break

if __name__=="__main__":
    if (os.path.exists(wakeup_path)==False):
        print("音频文件不存在...,文件路径:"+wakeup_path)
    else:
        play_audio()







