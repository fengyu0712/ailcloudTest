# import pytest
# import sys
# import os
#
#
#
# def pytest_addoption(parser):
#     parser.addoption("--env", action="store", default="ws://linksit.aimidea.cn:10000",
#                      help="one of: deeptables, gbm")
#
# # 从配置对象中读取自定义参数的值
# @pytest.fixture(scope="session")
# def cmdopt(request):
#     return request.config.getoption("--env")

import sys
import os

from scripts import init_env

curPath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(curPath)
import pytest
import config

base_path = config.base_path
# from scripts.init_env import host, current_env

allure_result = os.path.join(os.path.join(base_path, "result"), "allure_result")
allure_conf_path = os.path.join(allure_result, "environment.properties")


# 添加命令行参数
def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        # default: 默认值，命令行没有指定host时，默认用该参数值
        default=init_env.current_env,
        help="test case project host address"
    )


@pytest.fixture(scope="session", autouse=True)
def host(request):
    '''获取命令行参数'''
    # 获取命令行参数给到环境变量
    env = request.config.getoption("--env").upper()
    test_host = init_env.host
    print(f"当前用例运行测试环境:{test_host}")
    os.environ["host"] = test_host
    updata_allure_env(env, test_host)


def updata_allure_env(env, testhost):
    '''
    同步环境信息到allure报告上
    :param env: 当前环境
    :param testhost: 当前测试HOST
    :return:
    '''
    if os.path.isfile(allure_conf_path):
        os.remove(allure_conf_path)
    with open(allure_conf_path, "a") as f:
        f.write(f"ENVIRONMENT={env}\n")
        f.write(f"HOST={testhost}\n")

