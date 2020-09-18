# coding:utf-8
import subprocess, time, re, os
from Common import log, read_xls_news
from Common import mypyaudio
import contextlib
import wave
import datetime

now = time.strftime('%Y-%m-%d-%H-%M-%S')
excel_path = 'E:\\ws\\test_date\\AI云端ASR测试用例_test.xlsx'  # 映射关系表，命令词
result_path = "E:/ws/test_result/result%s.xls" % now
wakeup_path = "E:/ws/test_audio/002M30_36_010003.wav"  # #唤醒文件：你好小美的音频文件
cmd_path = "E:/ws/002M30_36/"

pattern = "\n(.*)	device"
wakeup_pattern = "ev(.*)wake up"
wakeup_full_duplex_pattern = "New full-duplex timeout =(.*)sec"
asr_pattern = "text\":\\t\"(.*)\""

startTTS_pattern = "ev(.*)speak request start"
endTTS_pattern = "ev(.*)speak end"
in_fullduplex_pattern = "info(.*)full duplex"
mid_pattern = "mid\":	\"(.*)\""
sessionId_patteern = "sessionId\":	\"(.*)\""
info_patteern = "info\":	\"(.*)\""

Log = log.Logger()
Log.info("=======================全双工链路打断精准率与识别率测试率测试========================")


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


def main1(patternlist, wav_path, q, timeout=None):
    if timeout is None:
        timeout = 5
    mypyaudio.play_audio(wav_path)
    time.sleep(timeout)
    resultlist = [False, False, False]
    print("队列的长度。。。。。", q.qsize())
    alldata = ""
    for data in range(q.qsize()):
        datainfo = (q.get(data))
        alldata = alldata + datainfo

    if alldata.find("\"ev\":	\"wake up\"") != -1:
        resultlist[0] = True
    print(alldata)
    if alldata.find("New full-duplex timeout =") != -1:
        resultlist[2] = True
    alldata = alldata.replace("\n", "").replace("\t", "")
    k = re.search("info\":\"(\S+)\"}", alldata)
    if k != None:
        resultlist[1] = k.group(1)

    return resultlist


def wakeup_xiaomei(q):
    if (os.path.exists(wakeup_path)):
        in_fullduplex_path = "E:\\ws\\test_audio\\打开自然对话.wav"
        for i in range(5):
            pattern_list = [wakeup_pattern, info_patteern, wakeup_full_duplex_pattern]
            result_list = main1(pattern_list, wakeup_path, q, timeout=2)
            print(result_list)
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


def wakeup():
    if (os.path.exists(wakeup_path)):
        in_fullduplex_path = "E:\\ws\\test_audio\\打开自然对话.wav"
        for i in range(5):
            pattern_list = [wakeup_pattern, info_patteern, wakeup_full_duplex_pattern]
            result_list = main1(pattern_list, wakeup_path, q, timeout=5)
            print(result_list)
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
    if booknames is None:
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


def main3(patterlist, pre_path, q, timeout):
    mypyaudio.play_audio(pre_path)
    time.sleep(timeout)
    print("队列的长度。。。。。", q.qsize())
    alldata = ""
    for data in range(q.qsize()):
        datainfo = (q.get(data))
        alldata = alldata + datainfo
    print("前置条件测试数据。。。。。")
    print(alldata)
    result_list = [False, False, False]
    if alldata.find("\"text\":	\"天气预报\"") != -1:
        result_list[0] = "天气预报"

    if alldata.find("speak request start") != -1:
        result_list[1] = "speak request start"

    if alldata.find("speak end") != -1:
        result_list[2] = True

    print("返回测试数据", result_list)
    return result_list


def main2(pattern_list, wav_path, q, timeout):
    mypyaudio.play_audio(wav_path)  # 播放命令词
    time.sleep(timeout)
    print("队列的长度。。。。。", q.qsize())
    alldata = ""
    for data in range(q.qsize()):
        datainfo = q.get(data)
        alldata = alldata + "\r\n" + datainfo
    print("命令词的音频测试数据。。。。。")
    print(alldata)
    listinfo = alldata.split('\r\n')
    result_list = []
    for j in range(0, len(pattern_list)):
        pattern = pattern_list[j]
        isexitvalue = False
        for one_line in listinfo:
            result_data = re.findall(pattern, one_line)
            if len(result_data) > 0:
                result = result_data[0]
                if result != "":
                    result_list.append(result)
                    isexitvalue = True
                    break

        if isexitvalue == False:
            result_list.append(False)
    print("测试数据如下：", result_list)
    return result_list


def break_pre(sessionId, q):
    pre_path = "E:\\ws\\test_audio\\天气预报.wav"  # 前置指令，进入全双工用
    re_expect = "天气预报"
    pattern_list = [asr_pattern, startTTS_pattern, endTTS_pattern]
    for i in range(3):
        if 0 < i < 3:
            sessionId = wakeup()
        result_list = main3(pattern_list, pre_path, q, timeout=4)
        try:
            assert re_expect == result_list[0]
            assert result_list[1] != False
            assert result_list[2] == False
        except Exception as e:
            Log.error("未满足打断条件【%s】，即将重新重试 " % e)
            # i += 1
        else:
            Log.info("已进入打断条件，即将播放音频")
            return sessionId


total_num = 0
asr_succese_num = 0
test_num = 0
break_succese_num = 0
asrANDbreak_succese_num = 0
msg = ""


def writlog(lines, path):
    with open(path, "a+", encoding="utf-8") as f:
        # print("写入文件开始......")
        f.writelines(lines)


def thread_adbinfo(que):
    global isend
    isend = False
    startTime = datetime.datetime.now()  # 开始时间
    print("开始运行时间：" + str(startTime))
    wake_count = 0  # 唤醒次数，默认为0
    cmd = "adb shell logread -f"
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         encoding='utf8', errors='ignore')
    path = "D:/1.txt"
    if os.path.exists(path):
        os.remove(path)
    for data in iter(p.stdout.readline, b''):
        if isend:
            break
        writlog(data, path)
        que.put(data)

    p.terminate()
    p.kill()


def run(q):
    global test_num, asr_succese_num, total_num, break_succese_num, asrANDbreak_succese_num, msg, isend
    bookname = '002M30_36'
    booknames = [bookname]
    test_data = get_data(excel_path, booknames)  # 获取所有的测试数据
    devices = adb_devices(pattern)  # 判断是否存在设备信息
    if devices == False:
        raise ("a db异常，未识别到设备")
    else:
        # 设置range，只跑200条.
        for i in range(50):
            Log.info("开始第%s条测试：%s" % (i + 1, test_data[i][:2]))
            except_value = test_data[i][1]
            wav_path = cmd_path + "/002M30_36_" + test_data[i][0] + ".wav"  # wav 路径
            sessionId = wakeup_xiaomei(q)  # 唤醒小美
            print(sessionId)
            if sessionId is None:
                Log.error("連續三次未喚醒！")
            else:
                Log.info("唤醒成功且进入全双工，即将进入播放前置音频")

                if break_pre(sessionId, q) != False:
                    Log.info("已进入打断条件，即将播放音频【%s】" % wav_path)
                    test_num += 1
                    rr = read_xls_news.Read_xls(result_path)
                    rw = rr.copy_book()
                    pattern_list = [asr_pattern, info_patteern, endTTS_pattern, startTTS_pattern]
                    # 获取测试音频时长
                    with contextlib.closing(wave.open(wav_path, 'r')) as f:
                        wav_length = f.getnframes() / float(f.getframerate())

                    result_list = main2(pattern_list, wav_path, q, timeout=wav_length + 5)
                    asr_result = result_list[0]
                    if asr_result == except_value:
                        asr_succese_num += 1
                    if asr_result != False:
                        if result_list[2] != False and result_list[3] != False:
                            # result = "Pass"
                            break_succese_num += 1
                            if asr_result == except_value:
                                asrANDbreak_succese_num += 1
                                result = "Pass"
                            else:
                                result = "Fail"
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
                    # Log.info("用例【%s】ASR识别结果：%s" % (test_data[i][:2], asr_result))
                    print("用例【%s】ASR识别结果：%s" % (test_data[i][:2], asr_result))
                    # Log.info("用例【%s】打断测试结果：%s" % (test_data[i][:2], result))
                    print("用例【%s】打断测试结果：%s" % (test_data[i][:2], result))
                    msg = "当前一共执行测试【%s次】，正常执行【%s】，其中ASR识别正确【%s次】,打断成功【%s次】，打断成功和识别成功次数【%s次】,识别率为：【%s】,打断精准率为：【%s】，打断召回率为：【%s】" % (
                        i + 1, test_num, asr_succese_num, break_succese_num, asrANDbreak_succese_num, asr_succese_rate,
                        break_accurate_rate,
                        break_recall_rate)
                    # Log.info(msg)
                    print(msg)
                    rr.write_linedata(rw, i + 2, [asr_result, result, mid, sessionId], sheetname=bookname, col=2)
                    rr.write_linedata(rw, 0,
                                      ["asr_succese_rate", asr_succese_rate, "break_accurate_rate", break_accurate_rate,
                                       "break_recall_rate", break_recall_rate], sheetname=bookname)
                    rr.save_write(rw, result_path)

        isend = True
    return msg


if __name__ == "__main__":
    import threading
    import queue
    from Common.send_mail import Mail
    from Common.Zipfile import Zipfile

    try:
        q = queue.Queue()
        t1 = threading.Thread(target=thread_adbinfo, args=(q,))
        t2 = threading.Thread(target=run, args=(q,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    except Exception as e:
        msg = "测试中断，原因：%s，测试结果：%s" % (e, msg)
    else:
        msg = "打断测试已完成，测试结果：%s，详情请查看附件" % msg
    finally:
        pass
        '''
        nowdate = time.strftime('%Y-%m-%d')
        logpath = "E:\ws\log\\%s.log" % nowdate
        logzip_path="E:\ws\log\\%s.log.zip" % nowdate
        Zipfile(logpath,logzip_path)
        m = Mail()
        m.creat_mail("打断测试结果",text=msg)
        m.add_attach1(result_path)
        logsize=round(os.path.getsize(logzip_path)/float(1024 * 1024),2)
        if logsize<20:
            m.add_attach1(logzip_path)
        m.sent_mail()
        '''
