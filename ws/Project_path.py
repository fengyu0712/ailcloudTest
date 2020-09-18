import os
# from common.conf import Conf
projectfail=os.path.split(os.path.realpath(__file__))[0]
# print(projectfail)
"根据配置文件读取当前项目所在的绝对路径"
Common_path=os.path.join(projectfail,"Common\\")
conf_path=os.path.join(projectfail,"conf\\")
test_audio_path=os.path.join(projectfail,"test_audio\\")
log_path=os.path.join(projectfail,"log\\")
test_date_path=os.path.join(projectfail,"test_date\\")
# TestAudioData_path=os.path.join(TestData_path,"test_audio\\")
test_result_path=os.path.join(projectfail,"test_result\\")
TestReport_path=os.path.join(projectfail,"test_result\\Report\\")
Image_path=os.path.join(projectfail,"Image\\")
TestCase_path=os.path.join(projectfail,"TestCase\\")

