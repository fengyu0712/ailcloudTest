# coding:utf-8
import subprocess, time, re, os, winsound
from Common import log, read_xls_news
from Common import mypyaudio
import Project_path

now = time.strftime('%Y-%m-%d-%H-%M-%S')
excel_path = os.path.join(Project_path.test_date_path, 'AI云端ASR测试用例_test.xlsx')  # 映射关系表，命令词
result_path = os.path.join(Project_path.test_result_path, '半双工ASR-result%s.xls' % now)
wakeup_path = os.path.join(Project_path.test_audio_path, "002M30_36_010003.wav")  # #唤醒文件：你好小美的音频文件
cmd_path = "E:/ws/002M30_36/"  # 音频文件目录

cmd = "adb shell logread -f"
p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                     encoding='utf8', errors='ignore')
pattern = "\n(.*)	device"
wakeup_pattern = "ev(.*)wake up"
asr_pattern = "asr\":\\t\"(.*)\","
startTTS_pattern = "ev(.*)speak request start"
endTTS_pattern = "ev(.*)speak end"
in_fullduplex_pattern = "info(.*)full duplex"
mid_pattern = "mid\":	\"(.*)\","
sessionId_patteern = "sessionId\":	\"(.*)\","
Log = log.Logger()
Log.info("=======================半双工链路ASR识别率测试========================")


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


def adb_info(pattern, timeout=None):
    if timeout is None:
        timeout = 1
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
    return result


def wakeup():
    if (os.path.exists(wakeup_path)):
        for i in range(3):
            try:
                winsound.PlaySound(wakeup_path, winsound.SND_FILENAME)
            except Exception as e:
                Log.error(e)
                mypyaudio.play_audio(wakeup_path)

            result = adb_info(wakeup_pattern)
            if result == False:
                Log.error("连续%s次未唤醒" % (i + 1))
                i += 1
            else:
                return True
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


total_num = 0
asr_succese_num = 0
test_num = 0


def run():
    global test_num, asr_succese_num, total_num
    devices = adb_devices(pattern)
    if devices == False:
        raise ("a db异常，未识别到设备")
    else:
        bookname = '002M30_36'
        booknames = [bookname]
        test_data = get_data(excel_path, booknames)
        for i in range(len(test_data)):
            Log.info("开始第%s条测试：%s" % (i + 1, test_data[i][:2]))
            except_value = test_data[i][1]
            wav_path = cmd_path + "/002M30_36_" + test_data[i][0] + ".wav"  # wav 路径
            result = "Fail"
            mid = ''
            sessionId = ''
            iswakeup = wakeup()
            if iswakeup is None:
                Log.error("連續三次未喚醒！")
            else:
                test_num += 1
                Log.info("唤醒成功，即将进入播放音频进行ASR测试")
                rr = read_xls_news.Read_xls(result_path)
                rw = rr.copy_book()
                Log.info("开始播放测试音频【%s】" % wav_path)
                try:
                    winsound.PlaySound(wav_path, winsound.SND_FILENAME)
                except Exception as e:
                    Log.error(e)
                    mypyaudio.play_audio(wakeup_path)
                asr_result = adb_info(asr_pattern)
                if asr_result != False:
                    sessionId = adb_info(sessionId_patteern)
                    mid = adb_info(mid_pattern)
                if asr_result == except_value:
                    result = "Pass"
                    asr_succese_num += 1
                asr_succese_rate = "%.2f%%" % (asr_succese_num / test_num * 100)
                Log.info("用例【%s】ASR识别结果：%s" % (test_data[i][:2], asr_result))
                Log.info("用例【%s】ASR测试结果：%s" % (test_data[i][:2], result))
                Log.info(
                    "当前一共执行测试【%s次】，正常执行【%s】，其中ASR识别正确【%s次】,识别率为：【%s】" % (
                        i + 1, test_num, asr_succese_num, asr_succese_rate))
                rr.write_linedata(rw, i + 2, [asr_result, result, mid, sessionId], sheetname=bookname, col=3)
                rr.write_onlydata(rw, 0, 1, asr_succese_rate, sheetname=bookname)
                rr.save_write(rw, result_path)


if __name__ == "__main__":
    run()
