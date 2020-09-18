import unittest, allure, json, os, pytest, ddt
from common.log import Logger

Path = os.path.abspath(os.path.dirname(__file__))
path = os.path.split(Path)[0]
from common.read_xls_news import Read_xls
from common.http_request_new import Request
from common.conf import Conf
from collections import Counter
import Project_path

import jsonpath  # 嵌套字典取值s = jsonpath.jsonpath(dic,'$..name')

test_path = Project_path.TestData_path + "电压力锅自动化案例.xlsx"
conf_path = Project_path.conf_path + "ReplyInfo.ini"
result_path = Project_path.TestResult_path + "电压力锅远程控制-自动化案例_Result.xls"
http_conf_path = Project_path.conf_path + "http.ini"
sn_path = Project_path.conf_path + "sn.ini"

host = Conf(http_conf_path).get_value("HTTP", "sit")
testmode = Conf(http_conf_path).get_value("AITEST", "mode")
# sn_yb101=Conf(sn_path).get_value("AC","yb101")
# sn_HB=Conf(sn_path).get_value("AC","HB")
sn_cooker = Conf(sn_path).get_value("pressure_cooker", "e_pressure_cooker")

r = Read_xls(test_path)
w = r.copy_book()
url = "%s/v1/auto_test/control/virtual" % host
data = {
    "version": "1.0",
    "text": "电压力锅开始煮饭 ",
    "uid": "6b07adb88106411fba94fe38c6754baa",
    "homeId": "162681",
    "device": {
        "sn": "0000EC1110002001A18C011A00620000",
        "category": "EC",
        "modelNo": "26"
    },
    "device_info": [
        {"id": 408191474334720002,
         "deviceId": "1099511825829",
         "serailNo": "0000EC1110002001A18C011A00620000",
         "enterpriseNo": "0000",
         "categoryNo": "EC",
         "modelNo": "26",
         "uid": "6b07adb88106411fba94fe38c6754baa",
         "homeId": "162681",
         "homeName": "9465的家",
         "roomId": "119961",
         "roomName": "厨房",
         "roleId": "1002",
         "deviceName": "电压力锅",
         "onlineStatus": 1,
         "version": 133}
    ],
    "query_reply": "query_reply"
}

# yb101_query=json.loads(Conf(conf_path).get_value("AC","yb101"))
# hb_query=json.loads(Conf(conf_path).get_value("AC","HB"))
rice_cooker_query = json.loads(Conf(conf_path).get_value("pressure_cooker", "e_pressure_cooker"))


def Label_Case(sheet_name=None):
    datalist = r.read_data(sheet_name, start_line=2)
    print(datalist)
    data = []
    if testmode == '0':
        for each in datalist:
            data.append(each)
    else:
        for each in datalist:
            if str(each[1]) in eval(testmode):
                data.append(each)
    return data


@allure.suite("电压力锅")
# @ddt.ddt
class TestRiceCooker():
    def setup_class(self):
        Logger().info("========%s测试开始:========" % __class__.__name__)

    def teardown_class(self):
        r.save_write(w, result_path)
        Logger().info("========%s测试结束!========" % __class__.__name__)

    @allure.feature('电压力锅')
    @pytest.mark.parametrize("tdata", Label_Case('电压力锅'))
    # @pytest.mark.flaky(reruns=3, reruns_delay=redis_case)#重试机制
    def test_pressure_cooker(self, tdata):
        test_id = tdata[0]
        test_content = tdata[2]
        data['text'] = tdata[4]
        data['device_info'][0]['serailNo'] = sn_cooker
        pre_data = tdata[3]
        Expect_nlu = tdata[5]
        Expect_lua = tdata[6]
        Expect_tts = tdata[7]

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
            pre_data = dict(rice_cooker_query, **pre_data)
            data["query_reply"] = pre_data

        Response = Request().requests(url, data, "POST").json()
        # 校验接口是的请求成功
        try:
            jsonpath.jsonpath(Response, "$..code")[0] == '200'
        except Exception as e:
            Logger().error(e)
            raise e
        nlu = jsonpath.jsonpath(Response, "$..nlu")[0]
        tts = jsonpath.jsonpath(Response, "$..text")[0].replace("，", ",")
        test_row = int(test_id.split('_')[-1])
        try:
            lua = jsonpath.jsonpath(Response, "$..luaData")[0]
        except:
            lua = ''
        finally:
            r.write_onlydata(w, test_row, 8, str(nlu), sheetname='电压力锅')
            r.write_onlydata(w, test_row, 9, str(lua), sheetname='电压力锅')
            r.write_onlydata(w, test_row, 10, str(tts), sheetname='电压力锅')

        try:
            print(str(nlu))
            assert str(nlu) == Expect_nlu, "NLU异常"
        except Exception as e:
            Logger().error(e)
            result = "NLU异常"
            raise e
        else:
            try:
                assert str(lua) == Expect_lua, "lua命令转换异常"
            except Exception as e:
                Logger().error(e)
                result = "lua命令转换异常"
                raise e
            else:
                try:
                    assert tts in eval(Expect_tts), "TTS返回异常"
                except Exception as e:
                    Logger().error(e)
                    result = "TTS返回异常"
                    raise e
                else:
                    result = "P"
                    Logger().info(u"【%s用例%s--%s】:测试通过！" % ("电压力锅", test_id, test_content))
        finally:
            r.write_onlydata(w, test_row, 11, str(result), sheetname='电压力锅')
