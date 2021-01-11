# coding: utf-8
# @Time : 2020-12-29 15:14 
# @Author : xx
# @File : test_xiaomei_box.py 
# @Software: PyCharm

# 小美音箱的测试用例
from tools.get_log import GetLog
from tools.file_tool import FileTool
from scripts.common_function import Commonfunction

log = GetLog.get_logger()  # 初始化日志对象
import allure
import pytest


class Test01:
    # 1、实列化获取工具类对象
    log.info("执行小美音箱入口测试用例..............")
    device_type = "xiaomei"  # 入口类型：328 固件的空调
    tool = FileTool("data_case.csv", device_type)
    # 读取excel的内容信息
    testcaseinfo = tool.read_excel()
    import datetime
    print('开始执行。。。。。。{}'.format(datetime.datetime.now()))
    Commonfunction().runcase(testcaseinfo, device_type, tool)
    print('结束。。。。。。{}'.format(datetime.datetime.now()))

    @allure.feature("小美音箱空调入口")
    @pytest.mark.parametrize("case", testcaseinfo)
    def test01(self, case):
        log.info("执行用例{}".format(case))
        current_sheet = case.get('case_catory')
        allure.dynamic.story(current_sheet)
        allure.dynamic.title(case.get("case_name"))
        Commonfunction().run_xiaomei_step(case, Test01.tool,  log)