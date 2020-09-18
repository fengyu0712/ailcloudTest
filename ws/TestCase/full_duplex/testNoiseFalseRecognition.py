#coding:utf-8

#噪音误识别测试
import subprocess,time,re,os,winsound,pytest
from Common import log,read_xls_news

excel_path = 'E:/ws/test_date/case.xlsx'  # 映射关系表，命令词
result_path="E:/ws/test_result/result.xlsx"
wakeup_path = "E:/ws/test_audio/002M30_36_010003.wav"  # #唤醒文件：你好小美的音频文件
pre_path = "E:\ws\\002M30_36\\002M30_36_010001.wav"  # 前置指令，进入全双工用
cmd_path = "E:/ws/002M30_36/"

r=read_xls_news.Read_xls(excel_path)
booknames=r.get_sheet_names()
data = []
for i in range(len(booknames)):
    tdata=r.read_data(booknames[i],start_line=3)
    data+=tdata
    # print(data)
    i+=1
print(data)

cmd = "adb shell logread -f"
p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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


class TestAsr():
    def setup_class(cls):
        devices = adb_devices(pattern)
        if devices  is None:
            raise ("adb异常，未识别到设备")
        cls.now = time.strftime('%Y-%m-%d-%H-%M-%S')
        cls.Log = log.Logger()
        cls.w = r.copy_book()
        cls.Log.info(u"========%s测试开始:========" % __class__.__name__)

    def teardown_class(cls):
        r.save_write(cls.w, result_path)
        cls.Log.info(u"========%s测试结束!========" % __class__.__name__)
        cls.Log.close()

    def setup(self):
        iswakeup=wakeup()
        if iswakeup != None:
            self.Log.info("唤醒成功，即将进入播放音频进行ASR测试")
        else:
            raise ("連續三次未喚醒！")
    def teardown(self):
        time.sleep(1)
    @pytest.mark.parametrize("tdata", data)
    def test_FalseRecognition(self,tdata):
        self.Log.info(tdata)
        testid=int(tdata[0])
        except_value=tdata[1]
        wav_path = cmd_path + "/002M30_36_" + tdata[0] + ".wav"  # wav 路径
        result = "Fail"

        winsound.PlaySound(wav_path, winsound.SND_FILENAME)
        pattern = "asr\":\\t\"(.*)\","
        time.sleep(0.5)
        asr_result = adb_info(pattern)
        print(asr_result)
        try:
            assert asr_result==except_value
        except Exception as e:
            result="Fail"
            raise e
        else:
            result = "Pass"
            self.Log.info("ASR识别结果：%s"%asr_result)
        finally:
            r.write_linedata(self.w, testid+1, [asr_result,result],sheetname="002M30_36",col=3)

