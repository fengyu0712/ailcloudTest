# coding:utf-8
import subprocess, time, re, os, winsound
from Common import log, read_xls_news
from Common import mypyaudio
# from Common import Process_adb_audio
from multiprocessing import Manager, Process, Pool
import contextlib
import wave

now = time.strftime('%Y-%m-%d-%H-%M-%S')
excel_path = 'E:\\ws\\test_date\\AI云端ASR测试用例_test.xlsx'  # 映射关系表，命令词
result_path = "E:/ws/test_result/result%s.xls" % now
wakeup_path = "E:/ws/test_audio/002M30_36_010003.wav"  # #唤醒文件：你好小美的音频文件
cmd_path = "E:/ws/002M30_36/"  #测试音频文件夹

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

cmd = "adb shell logread -f"
p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                     encoding='utf8', errors='ignore')
Log = log.Logger()
Log.info("=======================全双工链路打断精准率与识别率测试========================")

def adb_devices(pattern):
    p = \
    subprocess.Popen("adb devices", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                     encoding='utf8').communicate()[0]
    try:
        devices_list = re.findall(pattern, p)
        assert len(devices_list) > 0
    except:
        reslt = False
    else:
        reslt = devices_list
    return reslt


def adb_info(pattern, timeout=None):
    if timeout  is None:
        timeout = 3
    begin_time = time.time()
    endtime = begin_time + timeout
    result = False
    for i in iter(p.stdout.readline, b''):
        Log.debug(i)
        nowtime = time.time()
        if nowtime > endtime:
            break
        result_data = re.findall(pattern, i)
        try:
            result = result_data[0]
        except:
            result = False
        else:
            if len(result) > 1:
                break
    p.kill()
    return result


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


def main(patternlist, wav_path, timeout=None):
    if timeout  is None:
        timeout = 5
    q = Pool(2)
    res = q.apply_async(adb_info_listPatten, args=(patternlist, timeout,))
    # q.apply_async(winsound.PlaySound, args=(wav_path,winsound.SND_FILENAME,))
    q.apply_async(mypyaudio.play_audio, args=(wav_path,))
    q.close()
    q.join()
    print("结果是：%s" % res.get())
    return res.get()


def main2(patternlist, wav_path, timeout=None):
    if timeout  is None:
        timeout = 5
    from concurrent.futures import ThreadPoolExecutor
    threadPool = ThreadPoolExecutor(max_workers=4, thread_name_prefix="test_")
    res = threadPool.submit(adb_info_listPatten, patternlist, timeout, )
    # q.apply_async(winsound.PlaySound, args=(wav_path,winsound.SND_FILENAME,))
    threadPool.submit(mypyaudio.play_audio, wav_path, )
    threadPool.shutdown(wait=True)
    print("结果是：%s" % res.result())
    return res.result()


def wakeup():
    if (os.path.exists(wakeup_path)):
        in_fullduplex_path = "E:\\ws\\test_audio\\打开自然对话.wav"
        for i in range(5):
            pattern_list = [wakeup_pattern, info_patteern, wakeup_full_duplex_pattern]
            result_list = main2(pattern_list, wakeup_path, timeout=5)
            if result_list[0] == False:
                Log.error("连续%s次未唤醒" % (i + 1))
                i += 1
            else:
                if result_list[2] == False:
                    Log.error("已退出全双工，即将重新进入全双工")
                    # mypyaudio.play_audio(wakeup_path)
                    mypyaudio.play_audio(in_fullduplex_path)
                    time.sleep(1)
                    i += 1
                else:
                    sessionId = result_list[1]
                    return sessionId
    else:
        raise ("唤醒的音频文件不存在..." + wakeup_path)


def get_data(excel_path, booknames=None):
    r = read_xls_news.Read_xls(excel_path)
    if booknames  is None:
        booknames = r.get_sheet_names()
    test_data = []
    for i in range(len(booknames)):
        data = r.read_data(booknames[i], start_line=3)
        test_data += data
        # print(data)
        i += 1
    w = r.copy_book()
    r.save_write(w, result_path)
    return test_data


def break_pre(sessionId):
    pre_path = "E:\\ws\\test_audio\\打开小天使.wav"  # 前置指令，进入全双工用
    re_expect = "打开小天使"
    pattern_list = [asr_pattern, startTTS_pattern, endTTS_pattern]
    for i in range(3):
        if 0 < i < 3:
            sessionId = wakeup()
        result_list = main2(pattern_list, pre_path, timeout=3)
        try:
             assert re_expect == result_list[0]
             assert result_list[1] != False
             assert result_list[2] == False
        except Exception as e:
            Log.error("未满足打断条件，即将重新重试")
            i += 1
        else:
            return sessionId


total_num = 0
asr_succese_num = 0
test_num = 0
break_succese_num = 0
asrANDbreak_succese_num = 0
result_txt=""

def run():
    global test_num, asr_succese_num, total_num, break_succese_num, asrANDbreak_succese_num,result_txt
    bookname = '002M30_36'
    booknames = [bookname]
    test_data = get_data(excel_path, booknames)
    devices = adb_devices(pattern)
    if devices == False:
        raise ("a db异常，未识别到设备")
    else:
        for i in range(20):
            Log.info("开始第%s条测试：%s" % (i + 1, test_data[i][:2]))
            except_value = test_data[i][1]
            wav_path = cmd_path + "/002M30_36_" + test_data[i][0] + ".wav"  # wav 路径
            sessionId = wakeup()
            if sessionId  is None:
                Log.error("連續三次未喚醒！")
            else:
                Log.info("唤醒成功且进入全双工，即将进入播放前置音频")
                if break_pre(sessionId) != False:
                    Log.info("已进入打断条件，即将播放音频【%s】" % wav_path)
                    test_num += 1
                    rr = read_xls_news.Read_xls(result_path)
                    rw = rr.copy_book()
                    pattern_list = [asr_pattern, mid_pattern, endTTS_pattern, startTTS_pattern]
                    # 获取测试音频时长
                    with contextlib.closing(wave.open(wav_path, 'r')) as f:
                        wav_length = f.getnframes() / float(f.getframerate())
                    result_list = main2(pattern_list, wav_path, timeout=wav_length+5)
                    asr_result = result_list[0]
                    if asr_result == except_value:
                        asr_succese_num += 1
                    if asr_result != False:
                        if result_list[2] != False and result_list[3] != False:
                            result = "Pass"
                            break_succese_num += 1
                            if asr_result == except_value:
                                asrANDbreak_succese_num += 1
                        else:
                            result = "Fail"
                    else:
                        result = "Fail"
                    mid = result_list[1]
                    asr_succese_rate = "%.2f%%" % (asr_succese_num / test_num * 100)
                    # 打断召回率
                    break_recall_rate = "%.2f%%" % (asrANDbreak_succese_num / test_num * 100)
                    # 打断精准率
                    if break_succese_num > 0:
                        break_accurate_rate = "%.2f%%" % (asrANDbreak_succese_num / break_succese_num * 100)
                    else:
                        break_accurate_rate = 0
                    Log.info("用例【%s】ASR识别结果：%s" % (test_data[i][:2], asr_result))
                    Log.info("用例【%s】打断测试结果：%s" % (test_data[i][:2], result))
                    result_txt= "当前一共执行测试【%s次】，正常执行【%s】，其中ASR识别正确【%s次】,打断成功【%s次】，识别率为：【%s】,打断精准率为：【%s】，打断召回率为：【%s】" % (
                            i + 1, test_num, asr_succese_num, break_succese_num, asr_succese_rate, break_accurate_rate,
                            break_recall_rate)
                    Log.info(result_txt)

                    rr.write_linedata(rw, i + 2, [asr_result, result, mid, sessionId], sheetname=bookname, col=2)
                    rr.write_linedata(rw, 0, ["asr_succese_rate", asr_succese_rate, "break_accurate_rate", break_accurate_rate,"break_recall_rate",break_recall_rate], sheetname=bookname)
                    rr.save_write(rw, result_path)


if __name__ == "__main__":
    from Common.send_mail import Mail
    from Common.Zipfile import Zipfile
    try:
        result_txt=run()
    except Exception as e:
        result_txt="测试中断，原因：%s，测试结果：%s"%(e,result_txt)
    else:
        result_txt="打断测试已完成，测试结果：%s，详情请查看附件"%result_txt
    finally:
        nowdate = time.strftime('%Y-%m-%d')
        logpath = "E:\ws\log\\%s.log" % nowdate
        logzip_path="E:\ws\log\\%s.log.zip" % nowdate
        Zipfile(logpath,logzip_path)
        m = Mail()
        m.creat_mail("打断测试结果",text=result_txt)
        m.add_attach1(result_path)
        logsize=round(os.path.getsize(logzip_path)/float(1024 * 1024),2)
        if logsize<20:
            m.add_attach1(logzip_path)
        m.sent_mail()