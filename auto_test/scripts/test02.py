# coding: utf-8
# @Time : 2020-11-16 9:13
# @Author : xx
# @File : test02.py
# @Software: PyCharm
from tools.file_tool import FileTool
from tools.get_log import GetLog
from tools.file_tool import FileTool
from api.api import Api
import pytest
from api.webscoket_api import Mywebscoket
from scripts import common_assert,common_function
from scripts.common_function import Commonfunction

log=GetLog.get_logger()  # 初始化日志对象
import allure
import pytest

class Test01:
    #1、实列化获取工具类对象
    log.info("执行328全双工固件空调入口测试用例..............")
    device_type="328_fullDuplex"  # 入口类型：328 固件的空调
    tool=FileTool("data_case.xlsx",device_type)
    # 读取excel的内容信息
    testcaseinfo=tool.read_excel()
    import datetime
    print('开始执行。。。。。。{}'.format(datetime.datetime.now()))
    Commonfunction().runcase(testcaseinfo,device_type,tool)
    print('结束。。。。。。{}'.format(datetime.datetime.now()))

    @allure.feature("328全双工固件空调入口")
    @pytest.mark.parametrize("case",testcaseinfo)
    def test02(self,case):
        log.info("执行用例{}".format(case))
        current_sheet = case.get('case_catory')
        allure.dynamic.story(current_sheet)
        allure.dynamic.title(case.get("case_name"))
        Commonfunction().runstep(case, Test01.tool, Test01.device_type, log)
