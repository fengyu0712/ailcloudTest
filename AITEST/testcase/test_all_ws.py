from AITEST.Common.read_xls_news import Read_xls
from AITEST.Common.write_xls import WriteExcel
from AITEST.Common.T_websocket import WsSingle
from Common.conf import Read_conf
from Common.log import Logger
from Conf import Project_path
import sys,time,unittest,pytest,allure
from ddt import ddt,data


conf_path=Project_path.Conf_file_path
url=Read_conf(conf_path+"/ws.conf").get_value("WS","url")
audio_path=Read_conf(conf_path+"/ws.conf").get_value("WS","audio_path")
test_data_path=Project_path.TestData_path+"/case.xlsx"
r=Read_xls(test_data_path)
w=r.copy_book()

#执行有问题，抛错后不会继续执行
testdatas=[]
sheet_names=r.get_sheet_names()
for each in sheet_names:
    sheet_data=r.read_data(each,start_line=3)
    sheet_data.append(each)
    testdatas+=sheet_data
# writedata = WriteExcel()
# testdatas = r.read_data("002M30_36", start_line=3)

@allure.feature("测试全部语料")
class TestALLWebsocket:
    def setup_class(cls):
        cls.now = time.strftime('%Y-%m-%d-%H-%M-%S')
        cls.Log = Logger()
        cls.Log.info(u"========%s测试开始:========" % __class__.__name__)
        cls.ws=WsSingle(url)
    def teardown_class(cls):
        cls.ws.close()
        cls.Log.info(u"========%s测试结束!========" % __class__.__name__)
        cls.Log.close()
        result_path = Project_path.TestResult_path + cls.now + __class__.__name__ + ".xls"
        r.save_write(w,result_path)
    def setup(self):
        pass
    def teardown(self):
        pass


    @pytest.mark.parametrize("sheet_name", sheet_names)
    # @pytest.mark.flaky(reruns=3, reruns_delay=1)  # 重试机制
    def test_run(self,sheet_name):
        pass_num = 0
        faile_num = 0
        pass_rate = 0
        self.Log.info(u"开始测试【%s】" %sheet_name)
        # writedata.creattable(sheet_name)
        # writedata.write_linedata(0, ["test_id", "expect_value", "test_asr", "test_result", "pass_rate"])
        testdatas = r.read_data(bookname=sheet_name, start_line=3)
        for data in testdatas:
            test_id=data[0]
            wavfile=audio_path+sheet_name+"_"+data[1]+".wav"
            expect_value=data[2]
            result=eval(self.ws.runsingle(wavfile))
            test_asr=result["text"].replace(' ', '')
            r.write_onlydata(w, int(test_id) + 1, 3, test_asr, sheetname=sheet_name)
            try:
                assert test_asr==expect_value,"识别结果和期望值不一致"
            except Exception as e:
                test_result = "Faile"
                faile_num=faile_num+1
                raise e
            else:
                test_result = "Pass"
                pass_num=pass_num+1
            finally:
                pass_rate = pass_num / (pass_num + faile_num)
                self.Log.info("当前测试通过:%r" % pass_num)
                self.Log.info("当前测试失败:%r" % faile_num)
                self.Log.info("当前通过率为:%r %%" % (pass_rate*100))
                r.write_onlydata(w, int(test_id) + 1 ,4, test_result,sheetname=sheet_name)
        r.write_onlydata(w, 0, 3, pass_rate)
if __name__=="__main__":
    unittest.main()
