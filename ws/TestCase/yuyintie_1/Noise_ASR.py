# coding:utf-8
from Common import log, read_xls_news
from Common import mypyaudio
from Common.SimplifyASR import simplify_asr
import os
import re
import time
import serial
import serial.tools.list_ports
import Project_path

now = time.strftime('%Y-%m-%d-%H-%M-%S')
excel_path = os.path.join(Project_path.test_date_path, 'noise_asr_test.xls')  # 映射关系表，命令词
result_path = os.path.join(Project_path.test_result_path, '全双工噪音误打断测试--result%s.xls' % now)
wakeup_path = os.path.join(Project_path.test_audio_path, "002M30_36_010003.wav")  # #唤醒文件：你好小美的音频文件
in_fullduplex_path = os.path.join(Project_path.test_audio_path, "打开自然对话.wav")  # 重新打开自然对话的音频
pre_path = os.path.join(Project_path.test_audio_path, "打开小天使.wav")  # 前置指令，进入全双工用
cmd_path = "E:/ws/002M30_36/"  # 测试音频文件夹

wakeup_sign = "ev\":	\"wake up\""
in_fullduplex_sign = "fullDuplex\":	true"

asr_pattern = "text\":	\"(.*)\""
startTTS_pattern = "ev\":	\"speak request start\""
endTTS_pattern = "ev\":	\"speak end\""
mid_pattern = "mid\":	\"(.*)\","
sessionId_patteern = "sessionId\":	\"(.*)\","
Log = log.Logger()
Log.info("=======================全双工链路打断精准率与识别率测试========================")


class MySerial:
    def __init__(self, baudrate, serialname=None):
        plist = list(serial.tools.list_ports.comports())
        if len(plist) <= 0:
            print("The Serial port can't find!")
        else:
            plist_0 = list(plist[0])
            if serialname is None:
                serialname = plist_0[0]
            self.serialFd = serial.Serial(serialname, baudrate, timeout=60)
            print("check which port was really used >", self.serialFd.name)
            if self.serialFd.isOpen():
                print("Serial port open success")
            else:
                print("Serial port open failed")

    def recvcmd(self, timeout=None):
        if timeout is None:
            timeout = 10
        all_data = ""
        start_time = time.time()
        while True:
            end_time = time.time()
            if end_time - start_time < timeout:
                data = self.serialFd.read(self.serialFd.inWaiting())
                data = data.decode(encoding='utf-8', errors='ignore')
                Log.debug(data)
                if data != '':
                    all_data = all_data + data
            else:
                break
        return all_data

    def recv_data(self, pattern_list=None, checktime=None):
        if checktime is None:
            checktime = 10
        if pattern_list is None:
            pattern_list = []
        new_pattern_list = list(pattern_list)
        result_data = []
        start_time = time.time()
        while time.time() < start_time + checktime:
            data = self.serialFd.read(self.serialFd.inWaiting())
            data = data.decode(encoding='utf-8', errors='ignore')
            Log.debug(data)
            if data != '':
                if new_pattern_list:
                    for i in range(len(new_pattern_list)):
                        m = re.findall(new_pattern_list[0], data)
                        if not m:
                            break
                        if m[0]:
                            new_pattern_list.pop(0)
                            result_data.append(m[0])
                        else:
                            break
            time.sleep(1)
            if len(result_data) == len(pattern_list):
                break
        while len(result_data) < len(pattern_list):
            result_data.append(False)
        print("result_data测试结果：%s" % result_data)
        return result_data


s = MySerial(baudrate="961200")


def wakeup():
    if os.path.exists(wakeup_path):
        for i in range(3):
            mypyaudio.play_audio(wakeup_path)
            wakeup_result = s.recv_data(pattern_list=[wakeup_sign, in_fullduplex_sign, sessionId_patteern], checktime=3)
            if not wakeup_result[0]:
                Log.error("连续%s次未唤醒" % (i + 1))
                i += 1
            else:
                if not wakeup_result[1]:
                    Log.error("已退出全双工，即将重新进入全双工")
                    mypyaudio.play_audio(in_fullduplex_path)
                else:
                    return wakeup_result[2]
    else:
        raise ("唤醒的音频文件不存在..." + wakeup_path)


def break_pre():
    re_expect = "打开小天使"
    pattern_list = [asr_pattern, startTTS_pattern, endTTS_pattern]
    for i in range(3):
        if 0 < i < 3:
            wakeup()
        mypyaudio.play_audio(pre_path)
        pre_result = s.recv_data(pattern_list=pattern_list, checktime=2)
        try:
            assert re_expect in pre_result[0]
            assert pre_result[1]
            assert not pre_result[2]
        except Exception as break_error:
            Log.error("未满足打断条件[%s]，即将重新重试" % break_error)
            i += 1
        else:
            Log.info("符合打断条件")
            return True


def get_data(path, booknames=None):
    r = read_xls_news.Read_xls(path)
    if booknames is None:
        booknames = r.get_sheet_names()
    test_data = []
    for i in range(len(booknames)):
        data = r.read_data(booknames[i], start_line=3)
        test_data += data
        i += 1
    w = r.copy_book()
    r.save_write(w, result_path)
    return test_data


total_num = 0
asr_succese_num = 0
test_num = 0
break_succese_num = 0
asrANDbreak_succese_num = 0


def run():
    global test_num, asr_succese_num, total_num, asrANDbreak_succese_num, break_succese_num
    r = read_xls_news.Read_xls(excel_path)
    w = r.copy_book()
    r.save_write(w, result_path)
    for i in range(100):
        Log.info("开始第%s条测试" % (i + 1))
        sessionId = wakeup()
        if sessionId is None:
            Log.error("連續三次未喚醒！")
        else:
            into_time = time.strftime('%Y-%m-%d-%H-%M-%S')
            Log.info("唤醒成功且进入全双工:%s" % into_time)
            log_info = s.recvcmd(35)
            out_time = time.strftime('%Y-%m-%d-%H-%M-%S')
            nlg_asr = re.findall(asr_pattern, log_info)
            total_num += len(nlg_asr)
            test_result = "当前累积ASR噪音误识别打断次数为：%s" % total_num
            Log.info("第%s轮，测试结果：误识别%s次，误识别结果：%s" % (i + 1, len(nlg_asr), nlg_asr))
            Log.info(test_result)
            resul_list = [i, into_time, out_time, len(nlg_asr)] + nlg_asr
            rr = read_xls_news.Read_xls(result_path)
            rw = rr.copy_book()
            rr.write_linedata(rw, i + 1, resul_list)
            rr.save_write(rw, result_path)


if __name__ == "__main__":
    run()
    # from Common.send_mail import Mail
    # from Common.Zipfile import Zipfile

    # result = ""
    # try:
    #     run()
    # except Exception as e:
    #     result = "测试中断，原因：%s" % e
    # else:
    #     result = "全双工链路噪音误入测试已完成，结果请查看附件"
    # finally:
    #     # nowdate = time.strftime('%Y-%m-%d')
    #     # logpath = "E:\\ws\\log\\%s.log" % nowdate
    #     # logzip_path = "E:\\ws\\log\\%s.log.zip" % nowdate
    #     # Zipfile(logpath, logzip_path)
    #     mail = Mail()
    #     mail.creat_mail(result)
    #     mail.add_attach1(result_path)
    #     # logsize = round(os.path.getsize(logzip_path) / float(1024 * 1024), 2)
    #     # if logsize < 20:
    #     #     mail.add_attach1(logzip_path)
    #     mail.sent_mail()
