from AITEST.Common.read_xls_news import Read_xls
from AITEST.Common.write_xls import WriteExcel
from AITEST.Common.T_websocket import WsSingle
from Common.conf import Read_conf
from Conf import Project_path
from Common.log import Logger
from Conf import Project_path
import sys,time,unittest,pytest,allure
from ddt import ddt,data


conf_path=Project_path.Conf_file_path
url=Read_conf(conf_path+"/ws.conf").get_value("WS","url")
audio_path=Read_conf(conf_path+"/ws.conf").get_value("WS","audio_path")
test_data_path=Project_path.TestData_path+"/case.xlsx"
r=Read_xls(test_data_path)
sheet_names=r.get_sheet_names()
print(sheet_names)
for each in sheet_names:
    testdatas=r.read_data(bookname=each,start_line=3)
# print(each,testdatas)
testdatas=r.read_data(bookname="002M30_36",start_line=3)

# writedata = WriteExcel()
# writedata.creattable("result")

now = time.strftime('%Y-%m-%d-%H-%M-%S')

@ddt
@allure.feature("002M30_36")
class TestJJ(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Log = Logger()
        Log.info(u"========%s测试开始:========" % __class__.__name__)
        cls.ws=WsSingle(url)
        cls.Log = Log
    @classmethod
    def tearDownClass(cls):
        cls.Log.info(u"========%s测试结束!========" % __class__.__name__)
        cls.ws.close()
        cls.Log.close()
    def setUp(self):
        pass
    def tearDown(self):
        pass
    @data(*testdatas)
    def test_run(self,data):
        print(data)
        wavfile=audio_path+each+"_"+data[0]+".wav"
        print(wavfile)
        result=self.ws.runsingle(wavfile)
        print(result)
        asr=result["text"]

if __name__=="__main__":
    pytest.main(*sys.argv[1:])