# from Common.MySerial import MySerial
from Common import log,read_xls_news,Serials
import xlrd,pytest
import os,re
import winsound
import time
import datetime


excel_path = 'E:/ws/test_date/case.xlsx'   # 映射关系表，命令词
wakeup_path = "E:/ws/test_audio/002M30_36_010003.wav"   # #唤醒文件：你好小美的音频文件
cmd_path = "E:/ws/002M30_36/"

MySerial=Serials.MySerial()
Log = log.Logger()


r=read_xls_news.Read_xls(excel_path)
booknames=r.get_sheet_names()
data = []
for i in range(len(booknames)):
    tdata=r.read_data(booknames[i],start_line=3)
    data+=tdata
    # print(data)
    i+=1
print(data)


def wakeup():
    if (os.path.exists(wakeup_path)):
        pattern = "\"wakeupWord\"\:\"(.*)\"\,\"major"
        for i in range(3):
            winsound.PlaySound(wakeup_path, winsound.SND_FILENAME)
            result = MySerial.recvCmd(pattern)
            if result  is None:
                Log.info("连续%s次未唤醒" % (i + 1))
                i += 1
            else:
                return True
    else:
        raise ("唤醒的音频文件不存在..." + wakeup_path)

class TestAsr():
    def setup_class(cls):
        cls.now = time.strftime('%Y-%m-%d-%H-%M-%S')
        cls.Log = log.Logger()
        cls.Log.info(u"========%s测试开始:========" % __class__.__name__)

    def teardown_class(cls):
        Log.info(u"========%s测试结束!========" % __class__.__name__)
        Log.close()


    @pytest.mark.parametrize("tdata", data)
    def test_001(self,tdata):
        Log.info(tdata)
        except_value=tdata[1]
        wav_path = cmd_path + "/002M30_36_" + tdata[0] + ".wav"  # wav 路径
        iswakeup=wakeup()
        if iswakeup==True:
            winsound.PlaySound(wav_path, winsound.SND_FILENAME)
            pattern="\"asr\":	\"(.*)\""
            result = MySerial.recvCmd2(pattern)
            Log.info(result)
        else:
            range(iswakeup)

