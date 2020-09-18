# coding:utf-8
import subprocess, time, re, os
from Common import log, read_xls_news
from Common import mypyaudio
import Project_path

now = time.strftime('%Y-%m-%d-%H-%M-%S')
excel_path = os.path.join(Project_path.test_date_path, 'noise_asr_test.xls')  # 映射关系表，命令词
result_path = os.path.join(Project_path.test_result_path, '噪音误入-result%s.xls' % now)
wakeup_path = os.path.join(Project_path.test_audio_path, "002M30_36_010003.wav")  # #唤醒文件：你好小美的音频文件
in_fullduplex_path = os.path.join(Project_path.test_audio_path, "打开自然对话.wav")  # 重新打开自然对话的音频
pre_path = os.path.join(Project_path.test_audio_path, "打开小天使.wav")  # 前置指令，进入全双工用
cmd_path = "E:/ws/002M30_36/"  # 测试音频文件夹

pattern = "\n(.*)	device"
wakeup_pattern = "ev(.*)wake up"
wakeup_full_duplex_pattern = "New full-duplex timeout =(.*)sec"
asr_pattern = "asr\":\\t\"(.*)\","
startTTS_pattern = "ev(.*)speak request start"
endTTS_pattern = "ev(.*)speak end"
in_fullduplex_pattern = "info(.*)full duplex"
mid_pattern = "mid\":	\"(.*)\""
sessionId_patteern = "sessionId\":	\"(.*)\""
info_patteern = "info\":	\"(.*)\""
out_fullduplex_pattern = "to F_IDLE"

nlg_asr_pattern = "asr\":\t\"(.*)\",\n\n\t\t\"tts"

cmd = "adb shell logread -f"
p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                     encoding='utf8', errors='ignore')
Log = log.Logger()
Log.info("=======================全双工链路噪音误入测试========================")


def adb_devices(pattern):
    p = \
        subprocess.Popen("adb devices", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         encoding='utf8').communicate()[0]
    try:
        devices_list = re.findall(pattern, p)
        assert len(devices_list) > 0
    except:
        reslt = False
    else:
        reslt = devices_list
    return reslt


def noise_info(timeout=None):
    str = ''
    if timeout is None:
        timeout = 35
    endtime = time.time() + timeout
    for i in iter(p.stdout.readline, b''):
        str += i
        Log.debug(i)
        nowtime = time.time()
        if nowtime > endtime:
            Log.info("超过%ss，退出全双工" % timeout)
            break
        if out_fullduplex_pattern in i:
            Log.info("检测到，退出全双工标识")
            break
    p.kill()
    return str


def adb_info_listPatten(pattern_list, timeout):
    endtime = time.time() + timeout
    result_list = []
    for j in range(0, len(pattern_list)):
        pattern = pattern_list[j]
        for i in iter(p.stdout.readline, b''):
            if time.time() > endtime:
                break
            Log.debug(i)
            result_data = re.findall(pattern, i)
            if len(result_data) > 0:
                result = result_data[0]
                if result != "":
                    result_list.append(result)
                    break
        j += 1
    while len(result_list) < len(pattern_list):
        result_list.append(False)
    p.kill()
    return result_list


def main2(patternlist, wav_path, timeout=None):
    if timeout is None:
        timeout = 5
    from concurrent.futures import ThreadPoolExecutor
    threadPool = ThreadPoolExecutor(max_workers=4)
    res = threadPool.submit(adb_info_listPatten, patternlist, timeout, )
    threadPool.submit(mypyaudio.play_audio, wav_path, )
    threadPool.shutdown(wait=True)
    print("结果是：%s" % res.result())
    return res.result()


# def get_info():
#     str=''
#     endtime = time.time() + 5
#     cmd = "adb shell logread -f"
#     p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
#                          encoding='utf8', errors='ignore')
#     for i in iter(p.stdout.readline, b''):
#         Log.debug(i)
#         str+=i
#         if time.time() > endtime:
#             break
#     return str


def wakeup():
    if (os.path.exists(wakeup_path)):
        in_fullduplex_path = "E:\\ws\\test_audio\\打开自然对话.wav"
        for i in range(3):
            pattern_list = [wakeup_pattern, info_patteern, wakeup_full_duplex_pattern]
            result_list = main2(pattern_list, wakeup_path, timeout=4)
            if result_list[0] == False:
                Log.error("连续%s次未唤醒" % (i + 1))
                i += 1
            else:
                if result_list[2] == False:
                    Log.error("已退出全双工，即将重新进入全双工")
                    mypyaudio.play_audio(in_fullduplex_path)
                    i += 1
                else:
                    sessionId = result_list[1]
                    return sessionId
    else:
        raise ("唤醒的音频文件不存在..." + wakeup_path)


total_num = 0
result = ''


def run():
    global total_num, result
    r = read_xls_news.Read_xls(excel_path)
    w = r.copy_book()
    r.save_write(w, result_path)
    devices = adb_devices(pattern)
    if devices == False:
        raise ("a db异常，未识别到设备")
    else:
        for i in range(100):
            Log.info("开始第%s条测试" % (i + 1))
            sessionId = wakeup()
            if sessionId is None:
                Log.error("連續三次未喚醒！")
            else:
                into_time = time.strftime('%Y-%m-%d-%H-%M-%S')
                Log.info("唤醒成功且进入全双工:%s" % into_time)
                info = noise_info()
                out_time = time.strftime('%Y-%m-%d-%H-%M-%S')
                nlg_asr = re.findall(nlg_asr_pattern, info)
                total_num += len(nlg_asr)
                result = "当前累积ASR噪音误识别打断次数为：%s" % total_num
                Log.info("第%s轮，测试结果：误识别%s次，误识别结果：%s" % (i + 1, len(nlg_asr), nlg_asr))
                Log.info(result)
                resul_list = [i, sessionId, into_time, out_time, len(nlg_asr)] + nlg_asr
                rr = read_xls_news.Read_xls(result_path)
                rw = rr.copy_book()
                rr.write_linedata(rw, i + 1, resul_list)
                rr.save_write(rw, result_path)
    return result


if __name__ == "__main__":
    from Common.send_mail import Mail
    from Common.Zipfile import Zipfile

    run()
    # try:
    #     result = run()
    # except Exception as e:
    #     result = "测试中断，原因：%s\n测试结果：%s" % (e, result)
    # else:
    #     result = "噪音误入测试已完成，测试结果：%s，结果请查看附件" % result
    # finally:
    #     nowdate = time.strftime('%Y-%m-%d')
    #     logpath = "E:\ws\log\\%s.log" % nowdate
    #     logzip_path = "%s.zip" % logpath
    #     Zipfile(logpath, logzip_path)
    #     m = Mail()
    #     m.creat_mail("噪音误入测试结果", text=result)
    #     m.add_attach1(result_path)
    #     logsize = round(os.path.getsize(logzip_path) / float(1024 * 1024), 2)
    #     if logsize < 20:
    #         m.add_attach1(logzip_path)
    #     m.sent_mail()
