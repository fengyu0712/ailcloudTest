# coding:utf-8
import subprocess
import time, re, os, winsound, pytest, allure
from Common import log, read_xls_news

now = time.strftime('%Y-%m-%d')
excel_path = 'E:/音频资源/019.xlsx'  # 映射关系表，命令词
result_path = "E:/ws/test_result/result%s.xls" % now
wakeup_path = "E:/ws/test_audio/002M30_36_010003.wav"  # #唤醒文件：你好小美的音频文件
pre_path = "E:\ws\\002M30_36\天气预报.wav"  # 前置指令，进入全双工用
re_expect = "广州今天天气怎么样"
wavs_path = "E:\音频资源\\019\\"

cmd = "adb shell logread -f"
p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding='utf8',errors='ignore')

# 正則規則表達式
pattern = "\n(.*)	device"
wakeup_pattern = "ev(.*)wake up"
asr_pattern = "asr\":\\t\"(.*)\","
startTTS_pattern = "ev(.*)speak request start"
endTTS_pattern = "ev(.*)speak end"
in_fullduplex_pattern = "info(.*)full duplex"
Log = log.Logger(level="debug")


def adb_devices(pattern):
    p = subprocess.Popen("adb devices", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
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
        timeout = 2
    begin_time = time.time()
    endtime = begin_time + timeout
    result = False
    for i in iter(p.stdout.readline, b''):
        Log.debug(i)
        # print(i)
        nowtime = time.time()
        if nowtime > endtime:
            break
        result_data = re.findall(pattern, i)
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
            winsound.PlaySound(wakeup_path, winsound.SND_LOOP|winsound.SND_FILENAME)
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
            winsound.PlaySound(pre_path, winsound.SND_LOOP|winsound.SND_FILENAME)
            asr = adb_info(asr_pattern, timeout=2)
            fullduplex = adb_info(in_fullduplex_pattern, timeout=1.5)
            Log.info("预置ASR:====%s，fullduplex:====%s" % (asr, fullduplex))
            try:
                re_expect in asr and fullduplex != False
            except:
                Log.error("未检测到进入全双工标识")
                i += 1
            else:
                return True
    else:
        raise ("连续多次未唤醒，结束任务！")


r = read_xls_news.Read_xls(excel_path)
w = r.copy_book()
r.save_write(w, result_path)
# booknames=r.get_sheet_names()
sheetname = "0191"
booknames = [sheetname]
data = []
for i in range(len(booknames)):
    tdata = r.read_data(booknames[i], start_line=3)
    data += tdata
    i += 1

total_num = 0
asr_succese_num = 0
test_num=0

@allure.suite("全双工")
class TestASR():
    def setup_class(cls):
        devices = adb_devices(pattern)
        if devices  is None:
            raise ("adb异常，未识别到设备")
        cls.Log = log.Logger()
        cls.Log.info(u"========%s测试开始:========" % __class__.__name__)

    def teardown_class(cls):
        cls.Log.info(u"========%s测试结束!========" % __class__.__name__)
        cls.Log.close()

    def setup(self):
        global total_num
        total_num+=1
        isfullduplex = in_fullduplex(wakeup())
        if isfullduplex == True:
            self.Log.info("已进入全双工，即将进行ASR测试")
            self.rr = read_xls_news.Read_xls(result_path)
            self.rw = self.rr.copy_book()
        else:
            raise ("连续三次未进入全双工，退出当前用例！")

    def teardown(self):
        self.rr.save_write(self.rw, result_path)

    @allure.feature("全双工链路ASR识别")
    @pytest.mark.parametrize("tdata", data[:3])
    def test_ASR(self, tdata):
        global test_num, asr_succese_num
        self.Log.info("当前执行用例:%s" % tdata)
        except_value = tdata[1]
        wav_path = wavs_path + tdata[0]  # wav 路径
        result = "Fail"
        time.sleep(1)
        self.Log.info("开始播放测试音频【%s】" % wav_path)
        winsound.PlaySound(wav_path, winsound.SND_LOOP|winsound.SND_FILENAME)
        asr_result = adb_info(asr_pattern, timeout=2)
        self.Log.info("ASR识别结果为：%s" % asr_result)
        try:
            assert asr_result == except_value
        except Exception as e:
            raise e
        else:
            result = "Pass"
            asr_succese_num += 1
        finally:
            test_num += 1
            asr_succese_rate = "%.2f%%" % (asr_succese_num / total_num * 100)
            self.Log.info("用例【%s】的ASR测试结果是：%s" % (tdata[:2], result))
            self.rr.write_linedata(self.rw, total_num + 1, [asr_result, result], sheetname=sheetname, col=2)
            self.Log.info(
                "当前一共执行测试【%s次】，正常执行【%s】，其中ASR识别正确【%s次】,识别率为：【%s】" % (
                    total_num, total_num, asr_succese_num, asr_succese_rate))
            self.rr.write_onlydata(self.rw, 0, 1, asr_succese_rate, sheetname=sheetname)



