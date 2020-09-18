from AITEST.Common.read_xls_news import Read_xls
from AITEST.Common.write_xls import WriteExcel
from AITEST.Common.T_websocket import WsSingle
from Common.conf import Read_conf
from Common.log import Logger
from Conf import Project_path
import sys,time,unittest,pytest,allure
from ddt import ddt,data


conf_path=Project_path.Conf_file_path
url=Read_conf(conf_path+"/ws.conf").get_value("WS","url")
print(url)
audio_path=Read_conf(conf_path+"/ws.conf").get_value("WS","audio_path")
test_data_path=Project_path.TestData_path+"/case.xlsx"
r=Read_xls(test_data_path)
w=r.copy_book()

sheet_names=r.get_sheet_names()
print(sheet_names)
# writedata = WriteExcel()
testdatas = r.read_data("002M30_36", start_line=3)
print(testdatas)