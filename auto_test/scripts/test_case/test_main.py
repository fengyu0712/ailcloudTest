import allure
import pytest
import config
import os
from api import Traversing_path
from tools.file_tool_1 import MyXlrs
from tools.mylog import Logger
from scripts import common_function_1

log = Logger()
main_device_list = config.main_device_list

# 运行设备控制阶段
# common_function_1.run()


def get_sheet(device_type):
    result_path = config.base_path + os.sep + "result"
    result_file_list = Traversing_path.file_all_path(result_path, file_type="xlsx", filter_str=device_type)
    result_file = sorted(result_file_list, key=lambda x: os.path.getctime(os.path.join(result_path, x)))  # 按照文件创建时间排序
    sheet = MyXlrs(result_file[-1])
    return sheet


class TestMain:
    def setup_class(self):
        log.info("========%s开始执行主场景用例测试用例:========" % __class__.__name__)

    def teardown_class(cls):
        Logger().info("========%s执行主场景用例测试用例结束!========" % __class__.__name__)

    @allure.feature("328_halfDuplex")
    @pytest.mark.parametrize("case", get_sheet("328_halfDuplex").read_xlr())
    def test_328_halfDuplex(self, case):
        log.info("执行用例{}".format(case))
        device_type = "328_halfDuplex"
        current_sheet = case.get('case_category')
        allure.dynamic.story(current_sheet)
        allure.dynamic.title(case.get("case_name"))
        common_function_1.Commonfunction().runstep(device_type, get_sheet(device_type), case,
                                                   get_sheet(device_type).copy_sheet())

    @allure.feature("328_fullDuplex")
    @pytest.mark.parametrize("case", get_sheet("328_fullDuplex").read_xlr())
    def test_328_fullDuplex(self, case):
        log.info("执行用例{}".format(case))
        device_type = "328_fullDuplex"
        current_sheet = case.get('case_category')
        allure.dynamic.story(current_sheet)
        allure.dynamic.title(case.get("case_name"))
        common_function_1.Commonfunction().runstep(device_type, get_sheet(device_type), case,
                                                   get_sheet(device_type).copy_sheet())

    @allure.feature("3308_halfDuplex")
    @pytest.mark.parametrize("case", get_sheet("3308_halfDuplex").read_xlr())
    def test_3308(self, case):
        device_type = "3308_halfDuplex"
        log.info("执行用例{}".format(case))
        current_sheet = case.get('case_category')
        allure.dynamic.story(current_sheet)
        allure.dynamic.title(case.get("case_name"))
        common_function_1.Commonfunction().runstep(device_type, get_sheet(device_type), case,
                                                   get_sheet(device_type).copy_sheet())

    @allure.feature("yinxiang")
    @pytest.mark.parametrize("case", get_sheet("yinxiang").read_xlr())
    def test_yinxiang(self, case):
        device_type = "yinxiang"
        log.info("执行用例{}".format(case))
        current_sheet = case.get('case_category')
        allure.dynamic.story(current_sheet)
        allure.dynamic.title(case.get("case_name"))
        common_function_1.Commonfunction().runstep(device_type, get_sheet(device_type), case,
                                                   get_sheet(device_type).copy_sheet())

    @allure.feature("meiju")
    @pytest.mark.parametrize("case", get_sheet("meiju").read_xlr())
    def test_meiju(self, case):
        device_type = "meiju"
        log.info("执行用例{}".format(case))
        current_sheet = case.get('case_category')
        allure.dynamic.story(current_sheet)
        allure.dynamic.title(case.get("case_name"))
        common_function_1.Commonfunction().runstep(device_type, get_sheet(device_type), case,
                                                   get_sheet(device_type).copy_sheet())