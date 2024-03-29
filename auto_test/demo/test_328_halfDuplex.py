import allure
import pytest
import config
import os
from api import Traversing_path
from tools.file_tool_1 import MyXlrs
from tools.mylog import Logger
from scripts.common_function_1 import Commonfunction

log = Logger()
device_type = "328_halfDuplex"  # 入口类型：328 固件的空调
result_path = config.base_path + os.sep + "result"
result_file = Traversing_path.file_all_path(result_path, file_type="xlsx", filter_str=device_type)[0]
r = MyXlrs(result_file)
testcase_data = r.read_xlr()


class Test_328_HalDuplex:
    def setup_class(self):
        log.info("========%s开始执行328半双工固件空调入口测试用例:========" % __class__.__name__)

    def teardown_class(self):
        Logger().info("========%s执行328半双工固件空调入口测试用例结束!========" % __class__.__name__)

    @allure.feature(f"{device_type}")
    @pytest.mark.parametrize("case", testcase_data)
    def test01(self, case):
        log.info(case)
        log.info("执行用例{}".format(case))
        current_sheet = case.get('case_category')
        allure.dynamic.story(current_sheet)
        allure.dynamic.title(case.get("case_name"))
        Commonfunction().runstep(r, case, r.copy_sheet())
