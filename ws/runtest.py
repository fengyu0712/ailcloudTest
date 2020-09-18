import time,sys,os,platform
# 获取绝对路径，以便shell脚本跑
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import pytest
from Common.send_mail import Mail




# test_path="E:\ws\TestCase\\full_duplex\"
test_path="E:\ws\TestCase\\full_duplex\\testASR002.py"
now = time.strftime("%Y-%m-%d %H_%M_%S", time.localtime())
result_file= "E:\\ws\\test_result\\" + "allure_result\\"
report_file= "E:\\ws\\test_result\\" + "allure_report\\"




def run():
    # pytest.main()
    # pytest.main(["-s",'-n=1',test_path,'--alluredir',result_file])
    pytest.main(["-s",  test_path, '--alluredir', result_file])
    #'-s' 展示日志
    #'-p' 隐藏pytest打印日志
    #'-n=2'  分布式运行，n后面为CPU数量      多进程数据写入存在问题
    #'--alluredir'  执行文件夹下的所有
    #'--allure_features=PYTEST'  运行选定的标签或者场景

shell1 = "allure generate %s -o %s --clean"%(result_file,report_file)
shell2 = "allure open  %s"%report_file
def PC_run():
    os.system(shell1)
    os.system(shell2)
if __name__=="__main__":
    nowdate = time.strftime('%Y-%m-%d')
    result_path = "E:/ws/test_result/result%s.xls" % nowdate
    log_path="E:\\ws\\log\\"+nowdate+".log"
    run()
    m = Mail()
    m.creat_mail("全双工链路识别率测试结果",text="全双工链路识别率测试已经完成，测试结果见附件")
    m.add_attach(result_path)
    m.add_attach(log_path)
    m.sent_mail()
    PC_run()



