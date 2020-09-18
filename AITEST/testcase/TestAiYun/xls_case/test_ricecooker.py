
import unittest,allure,json,os,pytest,ddt
from common.log import Logger
Path = os.path.abspath(os.path.dirname(__file__))
path=os.path.split(Path)[0]
from common.read_xls_news import Read_xls
from common.http_request_new import Request
from common.conf import Conf
from collections import Counter
import Project_path

import jsonpath  #嵌套字典取值s = jsonpath.jsonpath(dic,'$..name')


test_path=Project_path.TestData_path+"电饭煲自动化案例.xlsx"
conf_path=Project_path.conf_path+"ReplyInfo.ini"
result_path=Project_path.TestResult_path+"电饭煲远程控制-自动化案例_Result.xls"
http_conf_path=Project_path.conf_path+"http.ini"
sn_path=Project_path.conf_path+"sn.ini"

host=Conf(http_conf_path).get_value("HTTP","sit")
testmode=Conf(http_conf_path).get_value("AITEST","mode")
#sn_yb101=Conf(sn_path).get_value("AC","yb101")
#sn_HB=Conf(sn_path).get_value("AC","HB")
sn_ricecooker=Conf(sn_path).get_value("rice_cooker","rice_cooker_4001XM")

r=Read_xls(test_path)
w=r.copy_book()
url="%s/v1/auto_test/control/virtual"%host
data = {
    "version": "1.0",
    "text": "电饭煲开始煮饭 ",
    "uid": "6b07adb88106411fba94fe38c6754baa",
    "homeId": "162681",
    "device": {
        "sn": "0000EA11100000028197271200930000",
        "category": "EA",
        "modelNo": "40"
    },
    "device_info": [
        {
            "id": 408191474334720003,
             "deviceId": "1099511825287",
             "serailNo": "0000EA11100000028197271200930000",
             "enterpriseNo": "0000",
             "categoryNo": "EA",
             "modelNo": "40",
             "uid": "e76b6954ab5d4336ac45cf30d533d308",
             "homeId": "162681",
             "homeName": "9465的家",
             "roomId": "119961",
             "roomName": "厨房",
             "roleId": "1002",
             "deviceName": "电饭煲",
             "onlineStatus": 1,
             "version": 133
        }
    ],
    "query_reply": "query_reply"
}

#yb101_query=json.loads(Conf(conf_path).get_value("AC","yb101"))
#hb_query=json.loads(Conf(conf_path).get_value("AC","HB"))
rice_cooker_query=json.loads(Conf(conf_path).get_value("rice_cooker","rice_cooker_4001XM"))

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

@allure.suite("电饭煲")
# @ddt.ddt
class TestRiceCooker():
    def setup_class(self):
        Logger().info("========%s测试开始:========" % __class__.__name__)

    def teardown_class(self):
        r.save_write(w,result_path)
        Logger().info("========%s测试结束!========" % __class__.__name__)

    @allure.feature('RiceCooker_4001XM')
    @pytest.mark.parametrize("tdata",Label_Case('中高端电饭煲'))
    # @pytest.mark.flaky(reruns=3, reruns_delay=redis_case)#重试机制
    def test_ricecooker_400XM(self,tdata):
        test_id = tdata[0]
        test_content=tdata[2]
        data['text'] = tdata[4]
        data['device_info'][0]['serailNo']=sn_ricecooker
        pre_data = tdata[3]
        Expect_nlu=tdata[5]
        Expect_lua=tdata[6]
        Expect_tts=tdata[7]

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
        print("**************")
        print(Response)
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
            r.write_onlydata(w, test_row, 8, str(nlu), sheetname='中高端电饭煲')
            r.write_onlydata(w, test_row, 9, str(lua), sheetname='中高端电饭煲')
            r.write_onlydata(w, test_row, 10, str(tts), sheetname='中高端电饭煲')

        try:
            assert str(nlu)==Expect_nlu,"NLU异常"
        except Exception as e:
            Logger().error(e)
            result="NLU异常"
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
                    result="P"
                    Logger().info(u"【%s用例%s--%s】:测试通过！" % ("中高端电饭煲", test_id, test_content))
        finally:
            r.write_onlydata(w, test_row , 11, str(result), sheetname='中高端电饭煲')



