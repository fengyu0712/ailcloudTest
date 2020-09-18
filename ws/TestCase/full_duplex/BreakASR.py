# coding:utf-8
import subprocess, time, re, os, winsound, pytest, datetime,allure
from Common import log, read_xls_news
now = time.strftime('%Y-%m-%d-%H-%M-%S')
excel_path = 'E:/音频资源/019.xlsx'  # 映射关系表，命令词
result_path = "E:/ws/test_result/result%s.xls"%now
wakeup_path = "E:/ws/test_audio/002M30_36_010003.wav"  # #唤醒文件：你好小美的音频文件
pre_path = "E:\ws\\002M30_36\天气预报.wav"  # 前置指令，进入全双工用
re_expect = "广州今天天气怎么样"
wavs_path = "E:\音频资源\\019\\"




cmd = "adb shell logread -f"
p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# 正則規則表達式
pattern="\n(.*)	device"
wakeup_pattern = "ev(.*)wake up"
asr_pattern = "asr\":\\t\"(.*)\","
startTTS_pattern = "ev(.*)speak request start"
endTTS_pattern = "ev(.*)speak end"
in_fullduplex_pattern = "info(.*)full duplex"
Log = log.Logger()

def adb_devices(pattern):
    p = subprocess.Popen("adb devices",shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding='utf8').communicate()[0]
    try:
        devices_list = re.findall(pattern, p)
        assert len(devices_list) > 0
    except:
       reslt=None
    else:
        reslt=devices_list
    return reslt

def adb_info(pattern, timeout=None):
    if timeout  is None:
        timeout = 1
    begin_time = time.time()
    endtime = begin_time + timeout
    result = False
    for i in iter(p.stdout.readline, b''):
        # print(i)
        nowtime = time.time()
        if nowtime > endtime:
            break
        result_data = re.findall(pattern, i.decode('utf8', "ignore"))
        try:
            result = result_data[0]
        except:
            result = False
        else:
            break
    return result


def wakeup():
    if (os.path.exists(wakeup_path)):
        for i in range(3):
            winsound.PlaySound(wakeup_path, winsound.SND_FILENAME)
            result = adb_info(wakeup_pattern)
            if result == False:
                Log.error("连续%s次未唤醒" % (i + 1))
                i += 1
            else:
                return True
    else:
        raise ("唤醒的音频文件不存在..." + wakeup_path)


def in_fullduplex(iswakeup):
    if iswakeup == True:
        for i in range(3):
            if 0 < i < 3:
                wakeup()
            # time.sleep(0.5)
            winsound.PlaySound(pre_path, winsound.SND_FILENAME)
            asr = adb_info(asr_pattern, timeout=2)
            fullduplex = adb_info(in_fullduplex_pattern, timeout=1.5)
            Log.info("预置ASR识别结果:====%s，fullduplex:====%s" % (asr, fullduplex))
            try:
                re_expect in asr and fullduplex != False
            except:
                Log.error("未检测到进入全双工标识")
                i += 1
            else:
                return True
    else:
        Log.error ("连续多次未唤醒，结束任务！")


def ttsEnd(is_in_fullduplex):
    if is_in_fullduplex == True:
        Log.info("已进入全双工")
        for i in range(3):
            if 0 < i < 3:
                in_fullduplex(wakeup())
            start_ev = adb_info(startTTS_pattern,timeout=1)
            print(start_ev)
            end_ev = adb_info(endTTS_pattern,timeout=0.5)
            print(end_ev)
            # try:
            #     assert
            if start_ev != False and end_ev == False:
                return False
            else:
                i += 1
    else:
        Log.error ("连续多未进入全双工，结束任务！")



total_num = 0
asr_succese_num = 0
break_succese_num = 0

r = read_xls_news.Read_xls(excel_path)
# booknames=r.get_sheet_names()
sheetname="020"
booknames = [sheetname]
data = []
for i in range(len(booknames)):
    tdata = r.read_data(booknames[i], start_line=3)
    data += tdata
    i += 1

w=r.copy_book()
#检测ADB
devices = adb_devices(pattern)
if devices  is None:
    raise ("adb异常，未识别到设备")
else:
    for i in range(len(data)):
        Log.info("===============当前测试项：%s=============="%data[i])
        isfullduplex = in_fullduplex(wakeup())
        is_endTTS = ttsEnd(isfullduplex)
        if is_endTTS == False:
            Log.info("已进入打断唤醒条件，即将进行打断测试")
            except_value = data[i][1]
            wav_path = wavs_path + data[i][0] # wav 路径
            result = "Fail"
            winsound.PlaySound(wav_path, winsound.SND_FILENAME)
            playtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            Log.info("音频播放完成时间是：%s" % playtime)
            total_num += 1
            asr_result = adb_info(asr_pattern, timeout=2)
            Log.info("ASR识别结果为：%s" % asr_result)
            if asr_result == except_value:
                asr_succese_num += 1
            end_ev = adb_info(endTTS_pattern,timeout=1)
            start_ev = adb_info(startTTS_pattern,timeout=0.5)
            # print(end_ev,start_ev)
            try:
                assert end_ev != False
                assert start_ev != False
            except:
                result = "Fail"
                Log.error ("打断失败")
            else:
                result = "Pass"
                break_succese_num += 1
            finally:
                Log.info("打断测试结果：%s" % result)
                Log.info(
                    "当前一共执行测试【%s次】，其中ASR识别正确【%s次】，打断成功【%s次】" % (total_num, asr_succese_num, break_succese_num))
                r.write_linedata(w, i + 2, [asr_result, result], sheetname=sheetname, col=3)
        else:
            Log.error ("连续三次未进入打断唤醒条件！")

        i+=1

r.write_linedata(w, 0, ["total_num", "asr_succese_num", "break_succese_num"], sheetname=sheetname, col=6)
r.write_linedata(w, 1, [total_num, asr_succese_num, break_succese_num], sheetname=sheetname, col=6)
r.save_write(w, result_path)
Log.info(u"========测试结束!========" )

