# -*-coding:utf-8 -*-
# @Time : 2021/2/4 9:45 
# @Author : xx
# @File : test_open_api.py 
# @Software: PyCharm
# -*-coding:utf-8 -*-
import json
import time

import allure
import pytest
from jsonpath import jsonpath

import config
import os
from api import Traversing_path
from api.apis import Api
from tools.file_tool_1 import MyXlrs, FileTool
from tools.mylog import Logger
from scripts import common_function_1
from scripts.init_env import host, current_env, terminal_devices

log = Logger()
test_type = "openapi"

sheet = FileTool("open_api_case.csv", test_type)
testcaseinfo = sheet.read_excel_openapi()


def get_sheet(device_type):
    result_path = config.base_path + os.sep + "result"
    result_file = Traversing_path.file_all_path(result_path, file_type="xlsx", filter_str="openapi")[-1]
    print(result_file)
    sheet = MyXlrs(result_file)
    return sheet


class Test_OpenApi:
    def setup_class(self):
        log.info("========%s开始执行用例测试用例:========" % __class__.__name__)

    def teardown_class(cls):
        Logger().info("========%s执行OPENAPI用例测试用例结束!========" % __class__.__name__)

    @allure.feature("OPENAPI")
    @pytest.mark.parametrize("case", testcaseinfo)
    def test_openapi(self, case):
        case["data"]["data"]["deviceId"] = terminal_devices["328_halfDuplex"]["deviceId"] #修改deviceID
        log.info("执行用例{}".format(case))
        current_sheet = case.get('Interface_name')
        expect = case["expect"]
        allure.dynamic.story(current_sheet)
        response=""
        result=""
        try:
            response = Api().open_api(case['data'])
            for key in (list(expect.keys())):
                log.info(key)
                #部分接口返回的是str，jsonpath取不到值，需要转换
                if not jsonpath(response, f"$..{key}") and isinstance(jsonpath(response, f"$..data")[-1],str):
                    response["data"]=eval(jsonpath(response, "$..data")[-1])
                assert (expect[key] == jsonpath(response, f"$..{key}")[0]), f"{key}值校验失败"
        except Exception as e:
            result = e
            raise e
        else:
            result = "测试通过"
        finally:
            sheet.write_excel("OPENAPI", case.get("response"), str(response))
            sheet.write_excel("OPENAPI", case.get("result"), str(result))
        if current_sheet == "方言":
            time.sleep(5)
        else:
            time.sleep(1)
