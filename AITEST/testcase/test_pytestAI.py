from common.Interface_process import OnlyInterface, DataConversion, InterfaceProcess
import unittest, allure, json, os, pytest
from common.log import Logger

Path = os.path.abspath(os.path.dirname(__file__))
path = os.path.split(Path)[0]
filepath = path + '\\testdata\\testdata1.xls'
dd = DataConversion(filepath)


# @pytest.fixture(scope='module')
@allure.suite("接口自动化")
@allure.feature('PYTEST')
class TestPYJJ:
    # @classmethod
    # def setUpClass(cls):
    #     Logger().info("========%s测试开始:========" % __class__.__name__)
    # @classmethod
    # def tearDownClass(cls):
    #     Logger().info("========%s测试结束!========" % __class__.__name__)
    @pytest.mark.parametrize("tdata", dd)
    @pytest.mark.flaky(reruns=3, reruns_delay=1)  # 重试机制
    def test_run(self, tdata):
        Logger().info("tdata:%s"%tdata)
        id = tdata.pop('id')
        case_describe = tdata.pop('场景描述')
        qiwang =eval( tdata.pop('期望值'))
        Logger().info("1")
        result = InterfaceProcess(**tdata)
        Logger().info("2")
        s = result[0]
        for each in qiwang.keys():
            qiwang_value = each.split("=>")
            for i in range(0, len(qiwang_value)):
                s = s[qiwang_value[i]]
                i += 1
            try:
                assert s == qiwang[each], "与期望值不符"
            except Exception as e:
                raise e
            else:
                Logger().info(u"【用例%s--%s】:测试通过！" % (id, case_describe))
