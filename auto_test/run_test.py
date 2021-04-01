import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import pytest
import time
import config
from scripts import common_function_1

now = time.strftime("%Y-%m-%d %H_%M_%S", time.localtime())
result_path = os.path.join(config.base_path, "result")
# allure_report_path = os.path.join(config.base_path, "report")

allure_result_path = os.path.join(result_path, "allure_result")

test_env = config.test_env
test_path = config.base_path + os.sep + "scripts" + os.sep + "test_case" + os.sep + "test_main_case.py"


def run_deviceControl():
    # 运行设备控制阶段
    common_function_1.run()


def run_testcase():
    pytest.main(["-s", f"--env={test_env}", test_path, f'--alluredir={allure_result_path}'])
    # pytest.main(["-s",  test_path, '--alluredir', result_file])
    # '-s' 展示日志
    # '-p' 隐藏pytest打印日志
    # '-n=2'  分布式运行，n后面为CPU数量      分布式数据写入存在问题
    # https://www.cnblogs.com/Maruying/p/13683305.html
    # -worker = auto  分布式 获取cpu数量，起进程  windows下不生效
    # "--tests-per-worker=4"  分布式四个线程
    # '--alluredir'  执行文件夹下的所有
    # '--allure-features=PYTEST'  运行选定的标签或者场景


if __name__ == '__main__':
    # run_deviceControl()
    run_testcase()
    print("allure generate %s -o %s --clean" % (allure_result_path, allure_result_path))
    print("allure open  %s" % allure_result_path)
    os.system("allure generate %s -o %s --clean" % (allure_result_path, allure_result_path))
    os.system("allure open  %s" % allure_result_path)
