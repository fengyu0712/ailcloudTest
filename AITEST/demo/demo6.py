from common.read_xls_news import Read_xls
from common.http_request_new import Request
from common.conf import Conf
from collections import Counter
import json,Project_path
http_conf_path=Project_path.conf_path+"http.ini"
host=Conf(http_conf_path).get_value("HTTP","sit")
path="E:\AITEST\\testdata\yb101远程控制-自动化案例_new3.xls"
conf_path="E:\AITEST\conf\defaultQueryReply.ini"
r=Read_xls(path)
w=r.copy_book()
url="%s/v1/auto_test/control/virtual"%host
result_path="E:\AITEST\\testdata\yb101远程控制-自动化案例_new4.xls"
data_yb101_0=json.loads(Conf(conf_path).get_value("AC","yb101"))
data_ac=r.read_data('yb101',start_line=2)
for i in range(0,len(data_ac)):
    text=data_ac[i][4]
    if "空调" not in text:
        text="空调"+text
        r.write_onlydata(w, i + 1, 4,text , sheetname='yb101')
r.save_write(w,result_path)


