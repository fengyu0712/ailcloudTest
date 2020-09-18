import unittest, allure, json, os, pytest, ddt, redis, re
from common.log import Logger

Path = os.path.abspath(os.path.dirname(__file__))
path = os.path.split(Path)[0]
from common.read_xls_news import Read_xls
from common.http_request_new import Request
from common.myredis import myRedis
from common.conf import Conf
from demo.demo7 import Default_data
from collections import Counter
import Project_path
import jsonpath  # 嵌套字典取值s = jsonpath.jsonpath(dic,'$..name')
import lockfile

test_path = Project_path.TestData_path + "净化器自动化案例.xls"
conf_path = Project_path.conf_path + "ReplyInfo.ini"
result_path = Project_path.TestResult_path + "净化器自动化案例_Result.xls"
http_conf_path = Project_path.conf_path + "http.ini"

host = Conf(http_conf_path).get_value("HTTP", "sit")
testmode = Conf(http_conf_path).get_value("AITEST", "mode")

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


w = r.copy_book()


@allure.suite("净化器")
class TestFC:
    def setup_class(self):
        Logger().info("========%s净化器测试开始:========" % __class__.__name__)

    def teardown_class(self):
        r.save_write(w, result_path)
        # file_lock.release()
        Logger().info("========%s净化器测试结束!========" % __class__.__name__)

    @allure.feature('KJ400G')
    @pytest.mark.parametrize("tdata", Label_Case('KJ400G'))
    # @pytest.mark.flaky(reruns=3, reruns_delay=redis_case)#重试机制
    def test_FC_KJ400G(self, tdata):
        deviceModel = "KJ400G"
        Logger().debug("testdata:---" + str(tdata))
        data = Default_data(deviceModel)
        test_id = tdata[0]
        test_content = tdata[2]
        data['text'] = tdata[4]
        pre_data = tdata[3]
        test_row = int(re.split('_', test_id)[-1])
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
            # file_lock.acquire()
            r.write_onlydata(w, test_row, 8, str(nlu), sheetname=deviceModel)
            r.write_onlydata(w, test_row, 9, str(lua), sheetname=deviceModel)
            r.write_onlydata(w, test_row, 10, str(tts), sheetname=deviceModel)
        try:
            if not str(nlu) == str(tdata[5]): raise Exception("NLU异常：%s!=%s" % (str(nlu), str(tdata[5])))
            if not str(lua) == str(tdata[6]): raise Exception("lua命令转换异常：%s!=%s" % (str(lua), str(tdata[6])))
            if not tts in eval(tdata[7]): raise Exception("TTS返回异常：%s not in %s" % (tts, eval(tdata[7])))
        except Exception as e:
            result = e
            Logger().error(e)
            raise e
        else:
            result = "P"
            Logger().info(u"【%s用例%s--%s】:测试通过！" % ("净化器-%s" % deviceModel, test_id, test_content))
        finally:
            r.write_onlydata(w, test_row, 11, result, sheetname=deviceModel)
            r.write_onlydata(w, test_row, 12, mid, sheetname=deviceModel)
