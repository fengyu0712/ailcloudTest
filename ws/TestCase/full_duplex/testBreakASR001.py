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

r = read_xls_news.Read_xls(excel_path)
# booknames=r.get_sheet_names()
sheetname="0191"
booknames = [sheetname]
data = []
for i in range(len(booknames)):
    tdata = r.read_data(booknames[i], start_line=3)
    data += tdata
    i += 1


cmd = "adb shell logread -f"
p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding='utf8',errors='ignore')

# 正則規則表達式
pattern="\n(.*)	device"
wakeup_pattern = "ev(.*)wake up"
asr_pattern = "asr\":\\t\"(.*)\","
startTTS_pattern = "ev(.*)speak request start"
endTTS_pattern = "ev(.*)speak end"
in_fullduplex_pattern = "info(.*)full duplex"
Log = log.Logger()

def adb_devices(pattern):
    p = subprocess.Popen("adb devices",shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding='utf8',errors='ignore').communicate()[0]
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
    for i in iter(p.stdout.readline, r''):
        print(i)
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


def ttsEnd(is_in_fullduplex):
    if is_in_fullduplex == True:
        Log.info("已进入全双工")
        for i in range(3):
            if 0 < i < 3:
                in_fullduplex(wakeup())
            start_ev = adb_info(startTTS_pattern)
            end_ev = adb_info(endTTS_pattern)
            if start_ev != False and end_ev == False:
                return False
            else:
                i += 1
    else:
        raise ("连续多未进入全双工，结束任务！")


total_num = 0
asr_succese_num = 0
break_succese_num = 0


@allure.suite("全双工")
class TestBreakASR():
    def setup_class(cls):
        devices=adb_devices(pattern)
        if devices is None:
            raise ("adb异常，未识别到设备")
        cls.Log = log.Logger()
        cls.w = r.copy_book()
        r.write_onlydata(cls.w, 1, 4, "BreakResult", sheetname=sheetname)  # 修改定义result为BreakResult
        cls.Log.info(u"========%s测试开始:========" % __class__.__name__)
    def teardown_class(cls):
        r.write_linedata(cls.w, 0, ["total_num", "asr_succese_num", "break_succese_num"], sheetname=sheetname, col=6)
        r.write_linedata(cls.w, 1, [total_num, asr_succese_num, break_succese_num], sheetname=sheetname, col=6)
        r.save_write(cls.w, result_path)
        cls.Log.info(u"========%s测试结束!========" % __class__.__name__)
        cls.Log.close()


    def setup(self):
        isfullduplex = in_fullduplex(wakeup())
        is_endTTS = ttsEnd(isfullduplex)
        if is_endTTS == False:
            self.Log.info("已进入打断唤醒条件，即将进行打断测试")
        else:
            raise ("连续三次未进入打断唤醒条件！")
    def teardown(self):
        time.sleep(0.5)

    @allure.feature("语义打断")
    @pytest.mark.parametrize("tdata", data)
    def test_Break(self, tdata):
        global total_num, asr_succese_num, break_succese_num
        self.Log.info("当前执行用例:%s" % tdata)
        testid = int(re.split('_|\.',tdata[0])[-2])
        except_value = tdata[1]
        wav_path = wavs_path + tdata[0]  # wav 路径
        result = "Fail"
        winsound.PlaySound(wav_path, winsound.SND_FILENAME)
        playtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        self.Log.info("音频播放完成时间是：%s" % playtime)
        total_num += 1
        asr_result = adb_info(asr_pattern, timeout=2)
        print(asr_result)
        self.Log.info("ASR识别结果为：%s" % asr_result)
        if asr_result == except_value:
            asr_succese_num += 1
        end_ev = adb_info(endTTS_pattern)
        start_ev = adb_info(startTTS_pattern)
        # print(end_ev,start_ev)
        try:
            assert end_ev != False
            assert start_ev != False
        except:
            result = "Fail"
            raise ("打断失败")
        else:
            result = "Pass"
            break_succese_num += 1
        finally:
            self.Log.info("打断测试结果：%s" % result)
            self.Log.info(
                "当前一共执行测试【%s次】，其中ASR识别正确【%s次】，打断成功【%s次】" % (total_num, asr_succese_num, break_succese_num))
            r.write_linedata(self.w, testid + 1, [asr_result, result], sheetname=sheetname, col=3)


