import unittest, allure, json, os, pytest, ddt, redis
from common.log import Logger

Path = os.path.abspath(os.path.dirname(__file__))
path = os.path.split(Path)[0]
from common.read_xls_news import Read_xls
from common.http_request_new import Request
from common.myredis import myRedis
from common.conf import Conf
from demo.demo7 import Default_data
from common.Appointment import *
import Project_path
import jsonpath  # 嵌套字典取值s = jsonpath.jsonpath(dic,'$..name')

product = "电饭煲"
product_model = ['4001XM']

test_path = Project_path.TestData_path + "%s自动化案例.xls" % product
conf_path = Project_path.conf_path + "ReplyInfo.ini"
result_path = Project_path.TestResult_path + "%s自动化案例_Result.xls" % product
http_conf_path = Project_path.conf_path + "http.ini"
db_path = Project_path.conf_path + "db.ini"

host = Conf(http_conf_path).get_value("HTTP", "sit")
testmode = Conf(http_conf_path).get_value("AITEST", "mode")
device_list = eval(Conf(db_path).get_value("Redis", "redis_db"))

url = "%s/v1/auto_test/control/virtual" % host

r = Read_xls(test_path)


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


@allure.suite(product)
class TestFC:
    def setup_class(self):
        Logger().info("========%s测试开始:========" % (__class__.__name__ + product))

    def teardown_class(self):
        Logger().info("========%s测试结束!========" % (__class__.__name__ + product))

    @allure.feature(product_model[0])
    @pytest.mark.parametrize("tdata", Label_Case(product_model[0]))
    # @pytest.mark.flaky(reruns=3, reruns_delay=redis_case)#重试机制
    def test_EA_4001XM(self, tdata):
        appoint = Appointment()
        deviceModel = product_model[0]
        Logger().debug("testdata:---" + str(tdata))
        rd = myRedis(redis_db=device_list[deviceModel])
        data = Default_data(deviceModel)
        test_id = tdata[0]
        test_content = tdata[2]
        data['text'] = tdata[4]
        pre_data = tdata[3]
        # 对预期NLU进行日期转换（如果有日期的才会用到）
        tdata[5] = appoint.run_nlu(tdata[5])

        # 查询类LUA测试时间修改
        # test_lua = eval(tdata[6])
        try:
            sign_msg = jsonpath.jsonpath(eval(tdata[6]), "$..sign_msg")[0]
        except:
            pass
        else:
            eval(tdata[6])['error']['sign_msg'] = Appointment().run_tts(sign_msg)
            # tdata[6] = str(test_lua)

        # 对TTS进行转换（预约有时间时用到）
        tts_list = eval(tdata[7])
        for i in range(len(tts_list)):
            tts_list[i] = appoint.run_tts(tts_list[i])
        tdata[7] = str(tts_list)

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
        # 校验接口是的请求成功
        try:
            jsonpath.jsonpath(Response, "$..code")[0] == '200'
        except Exception as e:
            Logger().error(e)
            raise e
        nlu = jsonpath.jsonpath(Response, "$..nlu")[0]
        tts = jsonpath.jsonpath(Response, "$..text")[0].replace("，", ",")
        mid = jsonpath.jsonpath(Response, "$..mid")[0]
        try:
            lua = jsonpath.jsonpath(Response, "$..luaData")[0]
        except:
            lua = ''
        finally:
            rd.delete(test_id)  # 清除旧缓存
            rd.push_list(tdata)
            rd.push_onlydata(test_id, str(nlu))
            rd.push_onlydata(test_id, str(lua))
            rd.push_onlydata(test_id, str(tts))
        # lua校验错误时，跳过lua校验（预约时间校验出错，处理困难）
        if lua != '':
            if lua['error'] == {}:
                if not str(lua) == str(tdata[6]): raise Exception("lua命令转换异常：%s!=%s" % (str(lua), str(tdata[6])))

        try:
            if not str(nlu) == str(tdata[5]): raise Exception("NLU异常：%s!=%s" % (str(nlu), str(tdata[5])))
            if not tts in eval(tdata[7]): raise Exception("TTS返回异常：%s not in %s" % (tts, eval(tdata[7])))
        except Exception as e:
            result = e
            Logger().error(e)
            raise e
        else:
            result = "P"
            Logger().info(u"【%s--用例%s：%s】测试通过！" % (deviceModel + product, test_id, test_content))
        finally:
            rd.push_onlydata(test_id, str(result))
            rd.push_onlydata(test_id, str(mid))
