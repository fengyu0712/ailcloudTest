
import unittest,allure,json,os,pytest,ddt
from common.log import Logger
Path = os.path.abspath(os.path.dirname(__file__))
path=os.path.split(Path)[0]
from demo.demo7 import Default_data
from common.read_xls_news import Read_xls
from common.http_request_new import Request
from common.conf import Conf
import Project_path

import jsonpath  #嵌套字典取值s = jsonpath.jsonpath(dic,'$..name')


test_path=Project_path.TestData_path+"空调远程控制-自动化案例.xls"
conf_path=Project_path.conf_path+"ReplyInfo.ini"
result_path=Project_path.TestResult_path+"空调远程控制-自动化案例_Result.xls"
http_conf_path=Project_path.conf_path+"http.ini"
sn_path=Project_path.conf_path+"sn.ini"

host=Conf(http_conf_path).get_value("HTTP","sit")
testmode=Conf(http_conf_path).get_value("AITEST","mode")
sn_yb101=Conf(sn_path).get_value("AC","yb101")
sn_HB=Conf(sn_path).get_value("AC","HB")

r=Read_xls(test_path)
w=r.copy_book()
url="%s/v1/auto_test/control/virtual"%host


def Label_Case(sheet_name=None):
    datalist = r.read_data(sheet_name, start_line=2)
    data = []
    if testmode == '0':
        for each in datalist:
            data.append(each)
    else:
        for each in datalist:
            if str(each[1]) in eval(testmode):
                data.append(each)
    return data

@allure.suite("空调")
class TestAC():

    def setup_class(self):
        Logger().info("========%s测试开始:========" % __class__.__name__)

    def teardown_class(self):
        r.save_write(w,result_path)
        Logger().info("========%s测试结束!========" % __class__.__name__)

    @allure.feature('yb101')
    @pytest.mark.parametrize("tdata",Label_Case('yb101'))
    # @pytest.mark.flaky(reruns=3, reruns_delay=redis_case)#重试机制
    def test_AC_yb101(self,tdata):
        deviceModel = 'yb101'
        data = Default_data(deviceModel)
        test_id = tdata[0]
        test_content = tdata[2]
        data['text'] = tdata[4]
        pre_data = tdata[3]
        try:
            pre_data = json.loads(pre_data)
        except:
            pre_data = '{' + pre_data.replace('&', ',') + '}'
            try:
                pre_data = json.loads(pre_data)
            except Exception as e:
                Logger().error(e)
                raise e
        finally:
                pre_data = dict(data['query_reply'], **pre_data)
                data["query_reply"] = pre_data

        Response = Request().requests(url, data, "POST").json()
        nlu = jsonpath.jsonpath(Response, "$..nlu")[0]
        tts=jsonpath.jsonpath(Response,"$..text")[0]
        test_row = int(test_id.split('_')[-1])
        mid = jsonpath.jsonpath(Response, "$..mid")[0]
        try:
            lua = jsonpath.jsonpath(Response, "$..luaData")[0]
        except:
            lua = ''
        finally:
            r.write_onlydata(w, test_row, 8, str(nlu), sheetname=deviceModel)
            r.write_onlydata(w, test_row, 9, str(lua), sheetname=deviceModel)
            r.write_onlydata(w, test_row, 10, str(tts), sheetname=deviceModel)

        try:
            assert str(nlu)==tdata[5],"NLU异常"
        except Exception as e:
            Logger().error(e)
            result="NLU异常"
            raise e
        else:
            try:
                assert str(lua) == tdata[6], "lua命令转换异常"
            except Exception as e:
                Logger().error(e)
                result = "lua命令转换异常"
                raise e
            else:
                try:
                    assert tts in eval(tdata[7]), "TTS返回异常"
                except Exception as e:
                    Logger().error(e)
                    result = "TTS返回异常"
                    raise e
                else:
                    result="P"
                    Logger().info(u"【%s用例%s--%s】:测试通过！" % ("%s空调"%deviceModel, test_id, test_content))
        finally:
            r.write_onlydata(w, test_row , 11, str(result), sheetname=deviceModel)
            r.write_onlydata(w, test_row, 12, mid, sheetname=deviceModel)

    @allure.feature('HB')
    @pytest.mark.parametrize("tdata", Label_Case('HB'))
    # @pytest.mark.flaky(reruns=3, reruns_delay=redis_case)#重试机制
    def test_AC_HB(self, tdata):
        deviceModel = 'HB'
        data = Default_data(deviceModel)
        test_id = tdata[0]
        test_content = tdata[2]
        data['text'] = tdata[4]
        pre_data = tdata[3]
        try:
            pre_data = json.loads(pre_data)
        except:
            pre_data = '{' + pre_data.replace('&', ',') + '}'
            try:
                pre_data = json.loads(pre_data)
            except Exception as e:
                Logger().error(e)
                raise e
        finally:
                pre_data = dict(data['query_reply'], **pre_data)
                data["query_reply"] = pre_data

        Response = Request().requests(url, data, "POST").json()
        nlu = jsonpath.jsonpath(Response, "$..nlu")[0]
        tts = jsonpath.jsonpath(Response, "$..text")[0].replace("，", ",")
        test_row = int(test_id.split('_')[-1])
        mid = jsonpath.jsonpath(Response, "$..mid")[0]
        try:
            lua = jsonpath.jsonpath(Response, "$..luaData")[0]
        except:
            lua = ''
        finally:
            r.write_onlydata(w, test_row, 8, str(nlu), sheetname=deviceModel)
            r.write_onlydata(w, test_row, 9, str(lua), sheetname=deviceModel)
            r.write_onlydata(w, test_row, 10, str(tts), sheetname=deviceModel)

        try:
            assert str(nlu) == tdata[5], "NLU异常"
        except Exception as e:
            Logger().error(e)
            result = "NLU异常"
            raise e
        else:
            try:
                assert str(lua) == tdata[6], "lua命令转换异常"
            except Exception as e:
                Logger().error(e)
                result = "lua命令转换异常"
                raise e
            else:
                try:
                    assert tts in eval(tdata[7]), "TTS返回异常"
                except Exception as e:
                    Logger().error(e)
                    result = "TTS返回异常"
                    raise e
                else:
                    result = "P"
                    Logger().info(u"【%s用例%s--%s】:测试通过！" % ("%s空调" % deviceModel, test_id, test_content))
        finally:
            r.write_onlydata(w, test_row, 11, str(result), sheetname=deviceModel)
            r.write_onlydata(w, test_row, 12, mid, sheetname=deviceModel)



