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
w = r.copy_book()


testdatas=[]
sheet_names=r.get_sheet_names()
for sheetname in sheet_names:
    sheet_data=r.read_data(sheetname,start_line=3)
    for each in sheet_data:
        each.append(sheetname)
    testdatas+=sheet_data
# writedata = WriteExcel()
# testdatas = r.read_data("002M30_36", start_line=3)
pass_num=0
faile_num=0
pass_rate=0
pass_rate_formula="=COUNTIF(E:E,\"=Pass\")/(COUNTIF(E:E,\"=Pass\")+COUNTIF(E:E,\"=Fail\"))"
now = time.strftime('%Y-%m-%d-%H-%M-%S')
#setup_module 一个py文建只执行一次
#setup_class  class里只执行一次

def setup_module(module):
    Logger().info(module.__name__.split('.')[-1])

def teardown_module(module):
    # Logger().info(module.module.__name__)
    result_path = Project_path.TestResult_path + now + module.__name__.split('.')[-1] + ".xls"
    r.save_write(w, result_path)
    Logger().info("end")

@allure.feature("测试全部语料")
class TestALLWebsocket3:
    def setup_class(cls):
        cls.Log = Logger()
        cls.Log.info(u"========%s测试开始:========" % __class__.__name__)
        cls.ws=WsSingle(url)

    def teardown_class(cls):
        cls.ws.close()
        cls.Log.info(u"========%s测试结束!========" % __class__.__name__)
        cls.Log.close()



    @pytest.mark.parametrize("data", testdatas)
    # @pytest.mark.flaky(reruns=3, reruns_delay=redis_case)  # 重试机制
    def test_run(self,data):
        global pass_num, faile_num, pass_rate
        test_id = data[0]
        sheet_name=data[-1]
        wavfile = audio_path + sheet_name + "_" + data[1] + ".wav"
        expect_value = data[2]
        result = eval(self.ws.runsingle(wavfile))
        test_asr = str(result["text"].replace(' ', ''))
        r.write_onlydata(w, int(test_id) + 1, 3, test_asr, sheetname=sheet_name)
        try:
            assert test_asr == expect_value, "识别结果和期望值不一致"
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
            # time.sleep(0.5)
