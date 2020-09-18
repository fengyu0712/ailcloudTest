#coding:utf-8
import subprocess,time,re,os,winsound,pytest
from Common import log,read_xls_news

wakeup_path = "E:/ws/test_audio/002M30_36_010003.wav"  # #唤醒文件：你好小美的音频文件
pre_path = "E:\ws\\002M30_36\天气预报.wav"  # 前置指令，进入全双工用
re_expect = "广州今天天气怎么样"

wakeup_pattern = "ev(.*)wake up"
asr_pattern = "asr\":\\t\"(.*)\","
in_fullduplex_pattern = "info(.*)full duplex"
ttsend_pattern = "ev(.*)speak end"

cmd = "adb shell logread -f /tmp/.lastlog"

p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def adb_info(pattern,timeout=None):
    if timeout is None:
        timeout=5
    # cmd = "adb shell logread -f"
    begin_time = time.time()
    endtime = begin_time + timeout
    result = False
    for i in iter(p.stdout.readline, b''):
        print(i)
        nowtime = time.time()
        if nowtime > endtime:
            break
        result_data = re.findall(pattern,i.decode('utf8',"ignore"))
        try:
            result=result_data[0]
        except:
            continue
        else:
            break
    return result





def adb_info1(pattern,timeout=None):
    if timeout is None:
        timeout=5
    begin_time = time.time()
    endtime = begin_time + timeout
    returncode = p.poll()
    nowtime = time.time()
    while returncode  is None:
        if nowtime > endtime:
            break
        a=p.stdout.readline().strip()
        result_data = re.findall(pattern, a.decode('utf8',"ignore"))
        print(a)
        try:
            result = result_data[0]
        except:
            result = False
        else:
            break
        finally:
            returncode = p.poll()
            nowtime = time.time()
    return result

def adb_info2(pattern,timeout=None):

    if timeout is None:
        timeout=5
    # cmd = "adb shell logread -f"
    begin_time = time.time()
    endtime = begin_time + timeout
    result = False
    for i in iter(p.stdout.readline, b''):
        print(i)
        nowtime = time.time()
        if nowtime > endtime:
            break
        result_data = re.findall(pattern,i.decode('utf8',"ignore"))
        try:
            result=result_data[0]
        except:
            continue
        else:
            break
    return result
def wakeup():
    if (os.path.exists(wakeup_path)):
        for i in range(3):
            winsound.PlaySound(wakeup_path, winsound.SND_FILENAME)
            result = adb_info(wakeup_pattern)
            if result == False:
                print("连续%s次未唤醒" % (i + 1))
                i += 1
            else:
                return result
    else:
        raise ("唤醒的音频文件不存在..." + wakeup_path)

def in_fullduplex(iswakeup):
    # iswakeup=wakeup()
    if iswakeup != None:
        for i in range(3):
            if 0<i<3:
                wakeup()
            winsound.PlaySound(pre_path, winsound.SND_FILENAME)
            result =adb_info(asr_pattern)
            print(result)
            if result != re_expect:
                i += 1
            else:
                result =adb_info(in_fullduplex_pattern)
                if result == False:
                    print("未检测到进入全双工标识")
                    i += 1
                else:
                    return True
    else:
        raise ("连续多次未唤醒，结束任务！")

if __name__=="__main__":
    pattern="asr\":\\t\"(.*)\""
    a=in_fullduplex(wakeup())
    a=adb_info(pattern,timeout=2)
    print(a)

