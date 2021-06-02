# -*-coding:utf-8 -*-
# @Time : 2021/2/4 9:45 
# @Author : xx
# @File : test_open_api.py 
# @Software: PyCharm
# -*-coding:utf-8 -*-
import datetime
import re
import time
import allure
import pytest
from jsonpath import jsonpath

import config
import os
from api.apis import Api
from tools.file_tool import FileTool
from tools.mylog import Logger
from scripts.init_env import current_env, terminal_devices
from tools.myxls import Write_xls

log = Logger()
test_type = "openapi"

nowdate = datetime.datetime.now().strftime('%Y-%m-%d')
case_path = os.path.join(os.path.join(config.base_path, "data"), "open_api_case.csv")
result_file = os.path.join(os.path.join(config.base_path, "result"), f"{current_env}_OpenApi_TestResult_{nowdate}.xls")
testcaseinfo = FileTool().read_csv(case_path)

header = ["用例编号", "测试接口", "用例名称", "serviceUrl", "参数", "校验参数", "实际结果", "测试结果"]


class Test_OpenApi:
    def setup_class(cls):
        log.info("========%s开始执行OPENAPI测试用例:========" % __class__.__name__)
        cls.w = Write_xls()
        cls.w.creattable("openapi")
        cls.w.write_linedata(0, header)

    def teardown_class(cls):
        Logger().info("========%s执行OPENAPI用例测试用例结束!========" % __class__.__name__)
        cls.w.save_excel(result_file)

    @allure.feature("OPENAPI")
    @pytest.mark.parametrize("case", testcaseinfo)
    def test_openapi(self, case):
        case_id = case[0]
        row = int(re.split("_", case_id)[-1])
        serviceUrl = case[3]
        params = eval(case[4])
        expect = eval(case[5])
        if params.get("deviceId"):
            # params["deviceId"]="160528698598412"
            params["deviceId"] = terminal_devices["328_halfDuplex"]["deviceId"]  # 修改deviceID
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        if case[1] == "沉浸式烹饪":
            headers = {"Content-Type": "application/x-www-form-urlencoded", "uid": "a7da5f1093a94d40b45bb0ccf6fa21fc"}
        log.info("执行用例{}".format(case))
        current_sheet = case[1]
        allure.dynamic.story(current_sheet)
        data = {"serviceUrl": serviceUrl, "data": params}
        response = ""
        result = ""
        try:
            response = Api().open_api(data, headers)
            for key in (list(expect.keys())):
                log.info(key)
                # 部分接口返回的是str，jsonpath取不到值，需要转换
                if not jsonpath(response, f"$..{key}") and isinstance(jsonpath(response, f"$..data")[-1], str):
                    response["fullDuplex"] = eval(jsonpath(response, "$..data")[-1])
                assert (str(expect[key]) in str(jsonpath(response, f"$..{key}")[0])), f"{key}值校验失败"
        except Exception as e:
            result = e
            raise e
        else:
            result = "测试通过"
        finally:
            case[6] = response
            case[7] = result
            self.w.write_linedata(row, case)
        if current_sheet == "方言":
            time.sleep(5)
        else:
            time.sleep(1)
