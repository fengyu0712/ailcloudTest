# -*- coding: UTF-8 -*-
import os
import time
import datetime
import serial
import threading
import re
#import openpyxl
#from config import base_path

'''
误唤醒后，收集asr的信息，并保存信息
'''

# 全局变量
log_path = 'D:/log/'   #日志文件根路径
#exeute_time=604800  # 执行时间  7天
exeute_time=259200   # 3天

#离线指令词映射表
#excel_path=base_path+os.sep+"data/DF100.xlsx"
file_path=r"E:\script\script\data\DF100_offline.txt"
firm_type="dui"  # 固件类型表示dui，xf ：表示讯飞

# 列表表示的值
#"COM6":{"boudrate":1500000,"word":"\"ev\":	\"wake up\"","state":"1"}
serial_list={"COM4":{"boudrate":115200,"word":"wakeupWord","state":"1"},
             "COM16":{"boudrate":115200,"word":"wakeupWord","state":"0"}}


'''
# 读取excel信息
def readexcel():
    hash=dict()
    workbook=openpyxl.load_workbook(excel_path)
    obj_sheet=workbook[workbook.sheetnames[0]]
    for j in range(1, obj_sheet.max_row + 1):
        except_value = str(obj_sheet.cell(j, 1).value)  # exceptvalue
        wav_value = str(obj_sheet.cell(j, 2).value)  # wav的信息
        if firm_type=="xf":
           hash[wav_value] = except_value
        else:
           hash[except_value] = wav_value

    return hash
'''

def read_file():
    with open(file_path, 'r') as f:
       list1= f.readlines()
    for i in range(0,len(list1)):
        list1[i]=list1[i].rstrip('\n')
    #print(list1)
    return list1

def write_file(path, lines, mode='a+'):
    with open(path, mode) as f:
        f.writelines(lines)


def recvWakeup(serial, logfilepath,wakeup_mark):
    try:
        i = 0
        # 3秒内收到数据
        iswakeup = False
        new_data=""
        now_time=""
        while i < 20:
            data = serial.read_all()
            #print("唤醒测试数据:",data)
            if len(data) == 0:
                time.sleep(0.1)
                i += 1
            elif isinstance(data, bytes):
                new_data = new_data+data.decode(encoding='utf-8', errors='ignore')
                if new_data.find(wakeup_mark) != -1:
                    now_time = str(datetime.datetime.now())  # 唤醒时间
                    write_file(logfilepath, str(now_time))
                    iswakeup = True
                    write_file(logfilepath, new_data)
                    break

        return iswakeup,now_time
    except Exception as e:
        print("异常信息如下: " + str(e))
        return False

def start_test_port(serial,txt,logpath,ware_status,asrpath,hashtable):
    serialname=serial.name
    start_time = datetime.datetime.now()
    print(serialname+"开始运行时间："+str(start_time))
    write_file(logpath,"开始运行时间："+str(start_time)+"\n")
    if ware_status=="0":
        write_file(asrpath, "唤醒时间 离线asr 是否命中离线指令词  是否命中开关机指令" + "\n")
    else:
        write_file(asrpath, "唤醒时间 在线asr" + "\n")
    wakeup_count=0
    while(True):
        endTime = datetime.datetime.now()
        reponse_time = (endTime - start_time).total_seconds()
        if reponse_time >= exeute_time:
            print(serialname+"共执行时间：" + str(reponse_time))
            print(serialname+"结束时间：" + str(endTime))
            print(serialname + "共误唤醒次数：" + str(wakeup_count))
            write_file(logpath, "共执行时间：" + str(reponse_time)+"\n")
            write_file(logpath,  "共误唤醒次数：" + str(wakeup_count)+"\n")
            write_file(logpath,"结束时间：" + str(endTime)+"\n")
            break

        iswake,waketime=recvWakeup(serial,logpath,txt)
        if iswake:
            wakeup_count = wakeup_count + 1
            print("串口%s:时间%s wakeup success，共唤醒%s 次" %(serialname,datetime.datetime.now(),wakeup_count))
            # 要保存的内容
            serialinfo=recvCmd(serial,logpath,ware_status)
            #serialinfo=serialinfo.replace("\n","").replace("\t","").replace("\r","")
            serialinfo = serialinfo.replace("\t", "").replace("\r", "")
            if ware_status=="1":
                #在线asr信息
                asrvalue=getasrvalue(serialinfo)
                print("{}在线asr信息:{}".format(serialname,asrvalue))
                lines = waketime + " " + asrvalue + "\n"
            else:
                asrvalue=get_local_asr(serialinfo)
                print("{}离线asr信息:{}".format(serialname, asrvalue))
                if asrvalue in hashtable:
                    ismingzhong=True
                else:
                    ismingzhong = False

                isopen_commond=is_mingzhong_offline(serialinfo)
                print("是否命中离线指令词",ismingzhong)
                print("是否命中开关机指令",isopen_commond)
                lines = waketime + " " + asrvalue + " " + str(ismingzhong)+" "+ str(isopen_commond) + "\n"

            write_file(asrpath,lines)


# 获取tts返回的asr信息
def getasrvalue(newdata):
    asrvalue = ""
    try:
        if newdata!="":
            #commond = re.compile(".*TTS.*text\"\:\"(.*)\"\,\"endSession\".*")
            #commond = re.compile(".*test_output\"\:\{\"ev\"\:\"online tts\"\,\"text\"\:\"(.*)\"\,\"data\"\:\d+\,\"info\".*")
            #commond=re.compile("\"ev\":\"online tts\",\\n\"text\":\"(.*)\",")
            #commond=re.compile("\"text\":\"(.*)\",\n\"mid\"")
            commond=re.compile("\"asr\":\"(.*)\"")
            c = commond.findall(newdata)
            if len(c) > 0:
                asrvalue = str(c[0]).replace(" ", "")
    except Exception as e:
        print("解析异常了：",e)

    finally:
        return asrvalue

# 获取离线的asr信息
def get_local_asr(newdata):
    local_asr = ""
    try:
        #print(newdata)
        #commond = re.compile(
        #    ".*test_output.*ev\"\:\"local asr\"\,\"text\"\:\"(.*)\"\,\"data\"\:\d+,\"info\"\:\"dui\"")
        #commond=re.compile("\"ev\":\"local asr\",[\n]+\"text\":\"(.*)\",")
        commond=re.compile("\"rec\":\"(.*)\",\"conf\"")
        c = commond.findall(newdata)
        #print(c)

        if len(c) > 0:
            local_asr = str(c[0]).replace(" ", "")

    except Exception as e:
        print("解析异常了：", e)
    finally:
        return local_asr

def is_mingzhong_offline(newdata):
    ismingzhong = False
    try:
        #print(newdata)
        commond = re.compile("operation\":\"(.*)\",\"domain\"")
        c = commond.findall(newdata)
        #print(c)

        if len(c) > 0:
            local_asr = str(c[0]).replace(" ", "")
            if local_asr in ['close','open']:
                ismingzhong=True

    except Exception as e:
        print("解析异常了：", e)
    finally:
        return ismingzhong


def recvCmd(serial,log_filename,firm_state):
    i = 0
    # 10 秒内收到回应
    cmd_data = ""

    try:
        while i < 80:
            count = serial.inWaiting()
            if count > 0:
                #time.sleep(0.1)
                buff = serial.read_all()
                if isinstance(buff, bytes):
                    temp_data = buff.decode(encoding='utf-8', errors='ignore')
                    write_file(log_filename, temp_data)
                    cmd_data = cmd_data + temp_data

            else:
                time.sleep(0.1)
                i += 1
    except Exception as e:
        print("获取asr结果异常：" + str(e))
        write_file(log_filename,"获取asr结果异常：" + str(e))
    finally:
        return cmd_data

if __name__=="__main__":
    if os.path.exists(log_path)==False:
        os.makedirs(log_path)
    threadlist=[]
    print(len(serial_list))

    hashtable=read_file()
    #print(hashtable)

    for key in serial_list.keys():
        listinfo=serial_list[key]
        serialFd = serial.Serial(key, listinfo.get("boudrate"), timeout=60)
        logpath=log_path+key+"_"+datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')+".txt"  # 唤醒日志的路径信息

        asrpath=log_path+key+"_asr_"+datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')+".txt"   ## asr日志的保存

        t = threading.Thread(target=start_test_port, args=(serialFd,listinfo.get("word"),logpath,listinfo.get("state"),asrpath,hashtable,))
        threadlist.append(t)

    for t in threadlist:
        t.start()
        time.sleep(0.2)

    for t in threadlist:
        t.join()







