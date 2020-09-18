# coding:utf-8

# 噪音误识别测试
import subprocess, time, re, os, winsound, pytest,datetime
from Common import log, read_xls_news

testdata_path = 'E:\ws\\test_date\FalseRecognition.xls'  # 映射关系表，命令词
result_path = "E:/ws/test_result/result.xlsx"
wakeup_path = "E:/ws/test_audio/002M30_36_010003.wav"  # #唤醒文件：你好小美的音频文件
pre_path = "E:\ws\\002M30_36\天气预报.wav"  # 前置指令，进入全双工用
re_expect = "广州今天天气怎么样"

cmd_path = "E:/ws/002M30_36/"

r = read_xls_news.Read_xls(result_path)
booknames = r.get_sheet_names()
data = []
for i in range(len(booknames)):
    tdata = r.read_data(booknames[i], start_line=2)
    data += tdata
    i += 1
# print(data)


cmd = "adb shell logread -f"
p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
pattern = "\n(.*)	device"
wakeup_pattern = "ev(.*)wake up"
asr_pattern = "asr\":\\t\"(.*)\","
startTTS_pattern = "ev(.*)speak request start"
endTTS_pattern = "ev(.*)speak end"
in_fullduplex_pattern = "info(.*)full duplex"
in_half_pattern = "info(.*)half duplex"


online_tts="ev(.*)online tts"
Log = log.Logger()


def adb_devices(pattern):
    p = subprocess.Popen("adb devices", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                     encoding='utf8').communicate()[0]
    try:
        devices_list = re.findall(pattern, p)
        assert len(devices_list) > 0
    except:
        reslt = None
    else:
        reslt = devices_list
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
            time.sleep(0.5)
            winsound.PlaySound(pre_path, winsound.SND_FILENAME)
            # asr = adb_info(asr_pattern, timeout=2)
            fullduplex = adb_info(in_fullduplex_pattern, timeout=1.5)
            # Log.info("预置ASR:====%s，fullduplex:====%s" % (asr, fullduplex))
            try:
                # assert  re_expect in asr
                assert fullduplex != False
            except:
                Log.error("未检测到进入全双工标识")
                i += 1
            else:
                return True
    else:
        raise ("连续多次未唤醒，结束任务！")

timeout = 10
N = 0
w = r.copy_book()
while N < 3:
    isfullduplex = in_fullduplex(wakeup())
    if isfullduplex == True:
        N += 1
        into_fullduplex_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        Log.info("已进入全双工,时间是：%s"%into_fullduplex_time)
        r.write_onlydata(w, N, 3,into_fullduplex_time )
        begin_time = time.time()
        endtime = begin_time + timeout
        asr_list = []
        asr_num = 0
        break_num = 0
        for i in iter(p.stdout.readline, b''):
            # print(i)
            nowtime = time.time()
            if nowtime > endtime:
                out_fullduplex_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                Log.info("超过40s自动退出全双工,当前时间是：%s" % out_fullduplex_time)
                r.write_onlydata(w, N, 3, out_fullduplex_time)
                break
            exit_fullduplex = re.findall(in_half_pattern, i.decode('utf8', "ignore"))
            if len(exit_fullduplex) > 0:
                out_fullduplex_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                Log.info("检测到退出全双工日志,当前时间是：%s" % out_fullduplex_time)
                r.write_onlydata(w, N, 3, out_fullduplex_time)
                break
            r.write_onlydata(w, N, 3, into_fullduplex_time)
            asr_result = re.findall(asr_pattern, i.decode('utf8', "ignore"))
            break_result = re.findall(online_tts, i.decode('utf8', "ignore"))
            if asr_result!=[]:
                asr_list.append(asr_result[0])
                print("第%s轮，误识别到：%s" % (N, asr_result[0]))
                asr_num += 1
            if break_result!= []:
                break_num += 1
                if break_num>1:
                    print("第%s轮，第%s次被成功噪音打断" % (N, break_num-1))
        r.write_linedata(w, N, asr_list, col=4)
        r.write_onlydata(w, N, 3, break_num - 1)
    else:
        print("连续3次未进入全双工")
r.save_write(w,result_path)