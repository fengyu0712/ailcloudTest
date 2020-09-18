import time,sys,os,platform
# 获取绝对路径，以便shell脚本跑
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import Project_path,pytest
from common.myredis import myRedis
from common.write_xls import WriteExcel
from common.conf import Conf

db_path = Project_path.conf_path + "db.ini"
device_list=eval(Conf(db_path).get_value("Redis", "redis_db"))


# test_path = rootPath+"\\testcase\\WS_Test\\"
# test_path="E:\AITEST\\testcase\TestAiYun"
test_path="E:\AITEST\\testcase\TestAiYun\\redis_case"
# test_path="E:\AITEST\\testcase\TestAiYun\\redis_case\\test_StrideAcRredis02.py"
now = time.strftime("%Y-%m-%d %H_%M_%S", time.localtime())
result_file= Project_path.TestResult_path + "allure_result\\"
report_file= Project_path.TestReport_path + "allure_report\\"




def run():
    # pytest.main()
    pytest.main(["-s",'-n=2',test_path,'--alluredir',result_file])
    # pytest.main(["-s",  test_path, '--alluredir', result_file])
    #'-s' 展示日志
    #'-p' 隐藏pytest打印日志
    #'-n=2'  分布式运行，n后面为CPU数量      多进程数据写入存在问题
    #'--alluredir'  执行文件夹下的所有
    #'--allure_features=PYTEST'  运行选定的标签或者场景


header=['用例ID', '测试标签', '用例描述', '前置状态', '命令', '预期结果-nlu', '预期结果-luaResponse', '预期结果-tts','测试结果-nlu', '测试结果-luaResponse', '测试结果-tts','测试结果','mid']
testDevice=list(device_list.keys())
def redisToxls(devicelist,result_path):
    w = WriteExcel()
    for i in range(len(testDevice)):
        sheet=w.creattable(testDevice[i])
        w.write_linedata(0,header,sheet)
        r=myRedis(device_list[testDevice[i]])
        key_list=r.get_keys()
        for i in range(len(key_list)):
            key_value=r.read_list(key_list[i])
            w.write_linedata(i+1,key_value,sheet)
    w.save_excel(result_path)

shell1 = "allure generate %s -o %s --clean"%(result_file,report_file)
shell2 = "allure open  %s"%report_file
def PC_run():
    os.system(shell1)
    os.system(shell2)
if __name__=="__main__":
    nowtime = time.strftime('%Y-%m-%d-%H-%M-%S')
    result_path = Project_path.TestResult_path + "空调远程控制-自动化案例_Result%s.xls" % nowtime
    run()
    if 'redis' in test_path:
        redisToxls(testDevice,result_path)
    if platform.system()=="Windows":
       PC_run()
    else:
       print("End!")



