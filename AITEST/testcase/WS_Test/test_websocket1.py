from common.read_xls_news import Read_xls
from common.T_websocket import WsSingle
from common.conf import Conf
from common.log import Logger
import Project_path
import time, pytest,allure

conf_path= Project_path.conf_path
url=Conf(conf_path+"/ws.ini").get_value("WS","url")
audio_path=Conf(conf_path+"/ws.ini").get_value("WS","audio_path")
test_data_path= Project_path.TestData_path + "/case.xlsx"
r=Read_xls(test_data_path)
w=r.copy_book()
sheet_names=r.get_sheet_names()

sheet_name="002M30_36"
testdatas=r.read_data(bookname=sheet_name,start_line=3)

#

now = time.strftime('%Y-%m-%d-%H-%M-%S')
result_path= Project_path.TestResult_path + now + sheet_name + ".xls"
pass_num=0
faile_num=0
pass_rate=0
pass_rate_formula="=COUNTIF(E:E,\"=Pass\")/(COUNTIF(E:E,\"=Pass\")+COUNTIF(E:E,\"=Fail\"))"

@allure.feature(sheet_name)
class TestWebsocket2:
    @classmethod
    def setup_class(cls):
        cls.Log = Logger()
        cls.Log.info(u"========%s测试开始:========" % __class__.__name__)
        cls.ws = WsSingle(url)
    @classmethod
    def teardown_class(cls):
        cls.ws.close()
        cls.Log.info(u"========%s测试结束!========" % __class__.__name__)
        r.save_write(w, result_path)
        cls.Log.close()

    # @allure.sub_suite(testdatas)
    @pytest.mark.parametrize("data", testdatas)
    def test_run(self,data):
        pass
        global pass_num,faile_num,pass_rate
        test_id = data[0]
        wavfile = audio_path + sheet_name + "_" + data[1] + ".wav"
        expect_value = data[2]
        result = eval(self.ws.runsingle(wavfile))
        test_asr = str(result["text"].replace(' ', ''))
        r.write_onlydata(w, int(test_id) + 1, 3, test_asr, sheetname=sheet_name)
        try:
            assert test_asr==expect_value, "识别结果和期望值不一致"
        except Exception as e:
            test_result = "Fail"
            faile_num = faile_num + 1
            raise e
        else:
            test_result = "Pass"
            pass_num = pass_num + 1
        finally:
            pass_rate = pass_num / (pass_num + faile_num)
            self.Log.info("当前测试结果【通过:%r,失败:%r,通过率为:%.2f %%]" % (pass_num,faile_num,(pass_rate*100)))
            r.write_onlydata(w, int(test_id) + 1, 4, test_result, sheetname=sheet_name)
            r.write_onlydata(w, 0, 3, pass_rate_formula,sheetname=sheet_name)


