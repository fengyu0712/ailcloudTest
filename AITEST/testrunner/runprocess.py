import pytest,time,os,platform,Project_path
from common.Traversing_path import file_all_path
from common.m_process import mprocess

result_file = Project_path.TestResult_path + "allure_result\\"
report_file = Project_path.TestReport_path + "allure_report\\"
def runpy(test_path):
    print('Parent process %s.' % os.getpid())
    pytest.main(["-s", test_path, '--alluredir', result_file])
def PC_run():
    shell1 = "allure generate %s -o %s --clean" % (result_file, report_file)
    shell2 = "allure open  %s" % report_file
    os.system(shell1)
    os.system(shell2)


if __name__=='__main__':
    start_time = time.time()
    case_path="E:\\AITEST\\testcase\\WS_Test\\"
    case_path1 = case_path+"\\test_all_ws_new.py"
    # case_path2 = case_path+"\\test_websocket1.py"
    path = file_all_path(case_path, filter_str="test")
    print(path)
    mprocess(runpy,path)
    endtime = time.time()
    print("this run take %s seconds" % format(endtime - start_time))
    if platform.system()=="Windows":
        PC_run()


