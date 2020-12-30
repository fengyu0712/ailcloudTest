# coding: utf-8
# @Time : 2020-11-30 18:10 
# @Author : xx
# @File : conftest.py.py 
# @Software: PyCharm

import pytest
import sys
import os

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="ws://linksit.aimidea.cn:10000",
                     help="one of: deeptables, gbm")

# 从配置对象中读取自定义参数的值
@pytest.fixture(scope="session")
def cmdopt(request):
    return request.config.getoption("--env")

    # 将自定义参数的值打印出来


@pytest.fixture(autouse=True)
def fix_1( cmdopt):
    print('\n --cmdopt的值：', cmdopt)
    a = cmdopt




