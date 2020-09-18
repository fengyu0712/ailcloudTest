
from common.Interface_process import OnlyInterface,DataConversion,InterfaceProcess
import unittest,allure,json,os,pytest
from ddt import ddt,data
from common.log import Logger
Path = os.path.abspath(os.path.dirname(__file__))
path=os.path.split(Path)[0]
filepath=path+'\\testdata\\testdata1.xls'
dd=DataConversion(filepath)
# @pytest.fixture(scope='module')
@ddt
@allure.feature('UNITTEST+PYTEST')
class TestJJ(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Logger().info(u"========%s测试开始:========" % __class__.__name__)
    @classmethod
    def tearDownClass(cls):
        Logger().info(u"========%s测试结束!========" % __class__.__name__)
    def setUp(self):
        pass
    def tearDown(self):
        pass
    @data(*dd)
    @allure.story("开始运行")
    @pytest.mark.flaky(reruns=3, reruns_delay=1)#重试机制
    def test_run(self,tdata):
        try:
            case_describe = tdata.pop('场景描述')
            id = tdata.pop('id')
            qiwang = tdata.pop('期望值')
            qiwang=eval(qiwang)
        except Exception as e:
            raise e
        result=InterfaceProcess(**tdata)
        s=result[0]
        for each in qiwang.keys():
            qiwang_value=each.split("=>")
            for i in range(0, len(qiwang_value)):
                s = s[qiwang_value[i]]
                i += 1
            try:
                self.assertEqual(s, qiwang[each], "与期望值不符")
            except Exception as e:
                print(e)
                raise e
            else:
                Logger().info(u"【用例%s】--%s:测试通过！"%(id,case_describe))