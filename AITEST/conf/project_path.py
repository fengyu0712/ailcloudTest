import os
rootpath=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
"根据配置文件读取当前项目所在的绝对路径"
conf_path=os.path.join(rootpath,"conf/")
testcase_runpath=os.path.join(rootpath,"testcase/")
testdata_path=os.path.join(rootpath,"testdata/")
testcase_path=os.path.join(testdata_path,"测试案例.xlsx")

