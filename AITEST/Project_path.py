import os
# from common.conf import Conf
projectfail=os.path.split(os.path.realpath(__file__))[0]
# print(projectfail)
"根据配置文件读取当前项目所在的绝对路径"
common_path=os.path.join(projectfail,"common\\")
conf_path=os.path.join(projectfail,"conf\\")
InterfaceTest_path=os.path.join(projectfail,"InterfaceTest\\")
Log_path=os.path.join(projectfail,"Log\\")
TestData_path=os.path.join(projectfail,"testdata\\")
# TestAudioData_path=os.path.join(TestData_path,"test_audio\\")
TestResult_path=os.path.join(projectfail,"TestResult\\Result\\")
TestReport_path=os.path.join(projectfail,"TestResult\\Report\\")
Source_path=os.path.join(projectfail,"Source\\")
Image_path=os.path.join(projectfail,"Image\\")
PO_path=os.path.join(projectfail,"Page_Object\\")
TestCase_path=os.path.join(projectfail,"testcase\\")

