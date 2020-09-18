# -*- coding: UTF-8 -*-
import os
import time
import datetime
import serial
import threading
import subprocess

'''
误唤醒率
'''

# 全局变量
log_path = 'D:/log/'   #日志文件根路径
#exeute_time=604800  # 执行时间  7天
exeute_time=120
serial_list={"COM5":[115200,"\"ev\":	\"wake up\"","语音贴2.0"],"COM7":["921600","\"ev\":	\"wake up\"","语音贴1.0"]}


def write_file(path, lines, mode='a+'):
    with open(path, mode) as f:
        f.writelines(lines)


def recvWakeup(serial, logfilepath,wakeup_mark):
    try:
        i = 0
        # 3秒内收到数据
        iswakeup = False
        new_data=""
        while i < 20:
            data = serial.read_all()
            if len(data) == 0:
                time.sleep(0.1)
                i += 1
            elif isinstance(data, bytes):
                new_data = new_data+data.decode(encoding='utf-8', errors='ignore')
                write_file(logfilepath, new_data)
                if new_data.find(wakeup_mark) != -1:
                    iswakeup = True
                    #print("唤醒成功。。。。。。。")
                    break

        return iswakeup
    except Exception as e:
        print("异常信息如下: " + str(e))
        return False

def start_test_adbshell(devicesid,logfilepath,wakup_mark):
    start_time = datetime.datetime.now()
    print(devicesid + "开始运行时间：" + str(start_time))
    write_file(logfilepath, "开始运行时间：" + str(start_time))

    cmd = "adb shell logread -f"
    wakeup_count=0
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         encoding='utf8', errors='ignore')

    for data in iter(p.stdout.readline, 'b'):
        endTime = datetime.datetime.now()
        reponse_time = (endTime - start_time).total_seconds()
        if reponse_time >= exeute_time:
            print(devicesid + "共执行时间：" + str(reponse_time))
            print(devicesid + "结束时间：" + str(endTime))
            print(devicesid + "共误唤醒次数：" + str(wakeup_count))
            write_file(logfilepath, "共执行时间：" + str(reponse_time))
            write_file(logfilepath, "共误唤醒次数：" + str(wakeup_count))
            write_file(logfilepath, "结束时间：" + str(endTime))
            break

        log_ts_str = "[" + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S.%f') + "] " + data
        write_file(logfilepath, log_ts_str)
        if data.find(wakup_mark) != -1:
            print("****************")
            wakeup_count = wakeup_count + 1
            print(devicesid + 'wakeup success')
            #write_file(logfilepath, "误唤醒，wakup success")


def start_test_port(serial,txt,logpath,descinfo):
    serialname=serial.name
    start_time = datetime.datetime.now()
    print(serialname+"开始运行时间："+str(start_time))
    write_file(logpath,"开始运行时间："+str(start_time)+"\n")
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

        iswake=recvWakeup(serial,logpath,txt)
        if iswake:
            wakeup_count = wakeup_count + 1
            print("%s串口%s:时间%s wakeup success，共唤醒%s 次" %(descinfo,serialname,datetime.datetime.now(),wakeup_count))
            #print(serialname+":" +str(datetime.datetime.now())+ 'wakeup success')
            #write_file(logpath, "误唤醒，wakup success")

if __name__=="__main__":
    if os.path.exists(log_path)==False:
        os.makedirs(log_path)
    threadlist=[]
    print(len(serial_list))
    for key in serial_list.keys():
        listinfo=serial_list[key]
        serialFd = serial.Serial(key, listinfo[0], timeout=60)
        logpath=log_path+key+"_"+datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')+".txt"
        t = threading.Thread(target=start_test_port, args=(serialFd,listinfo[1],logpath,listinfo[2]))
        threadlist.append(t)

    for t in threadlist:
        t.start()
        time.sleep(0.5)

    for t in threadlist:
        t.join()







