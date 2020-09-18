from common.Request import Request
from common.Assert import Assert
import pytest
from common.RW_Excel import DealExcel
from common.Parsejson import ParseJson
from conf.project_path import *

datalist=[]
datalist = DealExcel(testcase_path,"空调").read_excel()


@pytest.mark.usefixtures("init_env")
@pytest.mark.parametrize("caseid,casestauts,casetext,result_nlu,result_tts,result_lua",datalist)
def test_start_ac(caseid,casestauts,casetext,result_nlu,result_tts,result_lua,init_env):
    domain=init_env[0]
    address=domain+init_env[1]
    query_reply_info=(init_env[4])["ac"]
    update_reply_info=ParseJson().update_jsonvalue(query_reply_info,(casestauts))
    parjson={
        "version": "0",
        "text": casetext,
        "uid":init_env[2],
        "device_info":init_env[3],
        "query_reply":update_reply_info
    }

    dictinfo=Request().post_request(address,jsondata=parjson)
    assertobj=Assert()
    assertobj.containvalue(str(dictinfo['tts']),result_tts)
    assertobj.equalvalue(str(dictinfo['nlu']),result_nlu)
    assertobj.equalvalue(str(dictinfo['luaData']), result_lua)




