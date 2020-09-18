import pytest
from conf.Config import ReadConfigFile


testresult={}
@pytest.fixture(scope="module")
def init_env():
    print("前置信息-----------获取环境信息.....")
    rfobj=ReadConfigFile()
    domainvalue,url=rfobj.get_env()   # 获取域名和url信息
    print(domainvalue,url)
    uid,devicesinfo,query_replyinfo=rfobj.get_devicesinfo()   #获取uid和devices的信息

    # 测试结果信息
    yield (domainvalue,url,uid,devicesinfo,eval(query_replyinfo),testresult)
    print("后置信息-----------写入excel的测试结果")
    print(testresult)
