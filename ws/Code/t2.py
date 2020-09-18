# -*- coding: UTF-8 -*-
import xlrd
import os,re
import winsound
import time
import datetime
import serial
import serial.tools.list_ports
from xlutils.copy import copy

'''
串口端打印ASR
脚本控制本地唤醒词音频播放——判断是否唤醒成功——唤醒成功，则播放音频语料（如果没有唤醒成功，则再次播放唤醒音频，直到唤醒成功为止）——读取串口端打印的ASR结果——将此ASR结果和期望值比较——完全一样，pass。不一样，fail。
需要注意的是：1.要统计播放唤醒音频测试；2.需要统计唤醒成功次数；3.需要打印唤醒成功率；4.需要打印识别成功率。
'''

# 全局变量
excel_path = 'E:/ws/test_date/TestCase.xlsx'   # 映射关系表，命令词
wakeup_path = "E:/ws/test_audio/002M30_36_010003.wav"   # #唤醒文件：你好小美的音频文件
cmd_path = "E:/ws/002M30_36/"  #需要执行的，音频文件
log_path = 'E:/ws/test_audio-log--0409.txt'   #日志文件

fileObject = open(log_path, 'w')   # 记录日志信息


cntWkSucc = 0
totalWk = 1
cntWkFail = 0   #唤醒失败次数
ratioWk = 0.0   #唤醒成功率

cntCmdTotal=5
cntCmdSucc = 0  # 识别成功次数s
cntCmdFail = 0   # 识别失败次数
ratioCmd = 0.0   # 识别率


# 查询可用串口
def query():
    plist = list(serial.tools.list_ports.comports())
    if len(plist) <= 0:
        print("The Serial port can't find!")
        return None
    else:
        plist_0 =list(plist[0])
        serialName = plist_0[0]
        serialFd = serial.Serial(serialName,15000000,timeout = 60)
        print("check which port was really used >",serialFd.name)


    return serialFd

# 打开串口
def open_interface(serialFd):
    if serialFd.isOpen():
        print("Serial port open success")
        # data = serialFd.readline()
        # print(data)
    else:
        print("Serial port open failed")


sheet_name='002M30_36'
def read_excel(serialFd):
    # 获取数据
    data = xlrd.open_workbook(excel_path)
    # 获取sheet
    table = data.sheet_by_name(sheet_name)
    # 获取总行数
    nrows = table.nrows

    for i in range(2,nrows-1):
        wav_value=table.cell(i,0).value  # wav文件值
        if wav_value.strip()=='':
            continue
        else:
            wav_value=sheet_name +'_'+wav_value

        wav_path=cmd_path+"/"+wav_value+".wav"   # wav 路径
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
                # print("识别结果信息:"+ str(ars_sucess)  + ars_result)
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
        # print(data)
        data = str(data, encoding="utf8")
        asr=re.findall("\"asr\":	\"(.*)\"",data)[0]
        print("识别次数:" + str(i) + "   识别结果:" + asr)
        fileObject.write("识别次数:" + str(i) + "识别结果" + asr)
        if data == "":
            time.sleep(0.8)
        else:
            break

    print("ASR结果：" + asr)
    cntCmdTotal=cntCmdTotal+1
    ret = asr.find(txt)
    if ret != -1:
        cntCmdSucc =cntCmdSucc+1
        print('Cmd asr success')
        return True,asr
    else:
        cntCmdFail=cntCmdFail+1
        print('Cmd asr failure')
        return False,data


# 唤醒小美,读取音频文件
def  wakeup_File(serialFd):
    global totalWk,cntWkSucc,cntWkFail
    iswake=False
    if (os.path.exists(wakeup_path)):
         winsound.PlaySound(wakeup_path, winsound.SND_FILENAME)
         fileObject.write(wakeup_path)
         fileObject.write(" wakeup ")
         time_stamp = datetime.datetime.now()
         fileObject.write(time_stamp.strftime('%Y.%m.%d-%H:%M:%S'))
         fileObject.write("\n")
         time.sleep(1)
         is_wakeup= recvWakeup(serialFd)
         totalWk=totalWk+1
         print(totalWk)
         if is_wakeup == True:
             cntWkSucc =cntWkSucc+1
             iswake=True
             fileObject.write(" wakeup " +str(iswake))
         else:
            cntWkFail=cntWkFail+1
            iswake=wakeup_File(serialFd)
            fileObject.write(" wakeup " + str(iswake))
         return iswake
    else:
        fileObject.write("唤醒的音频文件不存在..." +wakeup_path)
        print("唤醒的音频文件不存在..." +wakeup_path)
        return False


def recvWakeup(serial):
    txt = 'xiao mei'
    i = 0
    # 5秒内收到数据
    data=""
    while i < 50:
        data = serial.read_all()
        print(data)
        if data == '':
            # continue
            time.sleep(0.1)
            i += 1
        else:
            break

    data = str(data)
    print(data)
    ret=data.find(txt)
    if ret != -1:
        print('wakeup success')
        return True
    else:
        print('wakeup failure')
        return False

if __name__=="__main__":
    serialFd = query()  # 查询是否有插入串口
    if serialFd != None:
        open_interface(serialFd)
        # wakeup_File(serialFd)
        read_excel(serialFd)






