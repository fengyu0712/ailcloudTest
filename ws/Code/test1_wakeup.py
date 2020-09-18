# -*- coding: UTF-8 -*-
import xlrd
import os
import winsound
import time
import datetime
import serial
import serial.tools.list_ports
from xlutils.copy import copy
from Code.common import log
'''
串口端打印ASR
脚本控制本地唤醒词音频播放——判断是否唤醒成功——唤醒成功，则播放音频语料（如果没有唤醒成功，则再次播放唤醒音频，直到唤醒成功为止）——读取串口端打印的ASR结果——将此ASR结果和期望值比较——完全一样，pass。不一样，fail。
需要注意的是：1.要统计播放唤醒音频测试；2.需要统计唤醒成功次数；3.需要打印唤醒成功率；4.需要打印识别成功率。
'''

# 全局变量
excel_path = 'E:/ws/test_date/TestCase.xlsx'   # 映射关系表，命令词
wakeup_path = "E:\ws\\test_audio\\002M30_36_010005.wav"   # #唤醒文件：你好小美的音频文件
cmd_path = "D:/Users/ex_lijq4/Desktop/yinpin"  #需要执行的，音频文件
log_path = 'E:/ws/test_audio-log--0409.txt'   #日志文件

fileObject = open(log_path, 'w')   # 记录日志信息


cntWkSucc = 0
totalWk = 0
cntWkFail = 0   #唤醒失败次数
ratioWk = 0.0   #唤醒成功率

cntCmdTotal=10
cntCmdSucc = 0  # 识别成功次数s
cntCmdFail = 0   # 识别失败次数
ratioCmd = 0.0   # 识别率
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

def read_excel(serialFd):
    # 获取数据
    data = xlrd.open_workbook(excel_path)
    # 获取sheet
    table = data.sheet_by_name('002M30_36')

    # 获取总行数
    nrows = table.nrows

    for i in range(1,nrows-1):
        wav_value=table.cell(i,0).value  # wav文件值
        if wav_value.strip()=='':
            continue

        wav_path=cmd_path+"/"+wav_value   # wav 路径
        except_value=table.cell(i,1).value  # 预期结果值
        # 判断文件是否存在
        if (os.path.exists(wav_path)):
            issucess=wakeup_File(serialFd)  # 唤醒小美
            print(wav_path)
            if issucess:
                # step 2-2, 播放命令词，读取串口，判断是否正确识别
                #time.sleep(3)   # 间隔3.
                print("播放命令......" + str(except_value))
                fileObject.write("播放命令......" + str(except_value))
                winsound.PlaySound(wav_path, winsound.SND_FILENAME)
                ars_sucess,ars_result = recvCmd(serialFd,str(except_value))
                print("识别结果信息:"+ str(ars_sucess)  + ars_result)
                fileObject.write("识别结果信息:"+ str(ars_sucess)  + ars_result)
                table.put_cell(i, 2, 1, str(ars_result), format)
                table.put_cell(i, 3, 1, str(ars_sucess), format)

    table.put_cell(107, 1, 1, str(totalWk), format)    # 唤醒总数
    table.put_cell(108, 1, 1, str(cntWkSucc), format)
    ratioWk=(cntWkSucc / totalWk) * 100
    ratioWk_value="{:.2f}%".format(ratioWk)
    table.put_cell(109, 1, 1, str(ratioWk_value), format)
    table.put_cell(110, 1, 1, str(cntCmdSucc), format)
    table.put_cell(111, 1, 1, str(cntCmdFail), format)
    ratioCmd=(cntCmdSucc /cntCmdTotal) *100
    ratioCmd_value = "{:.2f}%".format(ratioCmd)
    table.put_cell(112, 1, 1, str(ratioCmd_value), format)
    print("唤醒次数：" + str(totalWk))
    print("唤醒成功次数：" + str(cntWkSucc))
    print("唤醒失败次数：" + str(cntWkFail))
    print("唤醒成功率为：" + ratioWk_value)
    print("识别成功率为：" + ratioCmd_value)
    wb = copy(data)
    wb.save(excel_path)

def recvCmd(serial, txt):
    # codetype = sys.getfilesystemencoding()
    # txt = 'asr'
    global cntCmdSucc,cntCmdFail,cntCmdTotal
    i = 0
    res = 'ASR结果 '
    # 10 秒内收到回应
    for i in range(20):
        data = serial.read_all()
        print(data)
        data = str(data, encoding="utf8")
        print("识别次数:" + str(i) + "识别结果" + data)
        fileObject.write("识别次数:" + str(i) + "识别结果" + data)
        print(data)
        if data == "":
            time.sleep(0.8)
        else:
            break

    print("ASR结果：" + data)
    cntCmdTotal=cntCmdTotal+1
    ret = data.find(txt)
    if ret != -1:
        cntCmdSucc =cntCmdSucc+1
        print('Cmd asr success')
        return True,data
    else:
        cntCmdFail=cntCmdFail+1
        print('Cmd asr failure')
        return False,data



        return False# 唤醒小美,读取音频文件
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

if __name__=="__main__":
    serialFd = query()  # 查询是否有插入串口
    if serialFd != None:
        open_interface(serialFd)
    while (True):
        issucess = wakeup_File(serialFd)  # 唤醒小美
        Log.info("唤醒总数：" + str(totalWk))
        Log.info("唤醒成功次数：" + str(cntWkSucc))
        ratioWk = (cntWkSucc / totalWk) * 100
        ratioWk_value = "{:.2f}%".format(ratioWk)
        Log.info("唤醒成功率：" + str(ratioWk_value))
        wakeup_File(serialFd)
        read_excel(serialFd)






