import allure
import pytest
import config
import os
from api import Traversing_path
from tools.file_tool_1 import MyXlrs
from tools.mylog import Logger
from scripts import common_function_1




log = Logger()

main_device_list=config.main_device_list

# 运行设备控制阶段
common_function_1.run()

def get_sheet(device_type):
    result_path = config.base_path + os.sep + "result"
    result_file = Traversing_path.file_all_path(result_path, file_type="xlsx", filter_str=device_type)[-1]
    print(result_file)
    sheet = MyXlrs(result_file)
    return sheet


class TestMain:
    def setup_class(self):
        log.info("========%s开始执行主场景用例测试用例:========" % __class__.__name__)


    def teardown_class(cls):
        Logger().info("========%s执行主场景用例测试用例结束!========" % __class__.__name__)

    @allure.feature(f"{main_device_list[0]}")
    @pytest.mark.parametrize("case", get_sheet(main_device_list[0]).read_xlr())
    def test01(self, case):
        log.info("执行用例{}".format(case))
        current_sheet = case.get('case_catory')
        allure.dynamic.story(current_sheet)
        allure.dynamic.title(case.get("case_name"))
        common_function_1.Commonfunction().runstep(get_sheet(main_device_list[0]), case, get_sheet(main_device_list[0]).copy_sheet())

    @allure.feature(f"{main_device_list[1]}")
    @pytest.mark.parametrize("case", get_sheet(main_device_list[1]).read_xlr())
    def test02(self, case):
        log.info("执行用例{}".format(case))
        current_sheet = case.get('case_catory')
        allure.dynamic.story(current_sheet)
        allure.dynamic.title(case.get("case_name"))
        common_function_1.Commonfunction().runstep(get_sheet(main_device_list[1]), case, get_sheet(main_device_list[1]).copy_sheet())
