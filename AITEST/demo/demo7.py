from common.read_xls_news import Read_xls
from common.http_request_new import Request
from common.conf import Conf
from collections import Counter
import json,Project_path
import jsonpath  #嵌套字典取值s = jsonpath.jsonpath(dic,'$..name')

device_conf = Project_path.conf_path + "device_info.ini"
http_conf_path=Project_path.conf_path+"http.ini"



def Default_data(product_model,ismeiju=None):
    deviceinfo =json.loads(Conf(device_conf).get_value("DeviceInfo", product_model))
    queryinfo = json.loads(Conf(device_conf).get_value("QueryInfo", product_model))
    data = {
        "version": "1.0",
        "text": "空调设置制冷模式",
        "uid": "auto_test0001",
        "homeId": "00001",
        "device_info": "device_info",
        "query_reply": "query_reply"
    }
    data["query_reply"] = queryinfo
    # data["device_info"] = deviceinfo  #如果传入全部设备，需要考虑多个同型号的情况
    data["device_info"] = [deviceinfo]
    if ismeiju==None:
        v_box_info = json.loads(Conf(device_conf).get_value("DeviceInfo", 'v_box'))
        data['device'] = v_box_info
    return data


def get_expectData(product_model,path,result_path,run_num=None):
    if run_num==None:
        run_num=1
    host = Conf(http_conf_path).get_value("HTTP", "sit")
    url="%s/v1/auto_test/control/virtual"%host
    data =Default_data(product_model)
    queryinfo=data['query_reply']
    r = Read_xls(path)
    data_list=r.read_data(product_model,start_line=2)
    w = r.copy_book()
    for i in range(len(data_list)):
        testid=data_list[i][0]
        tdata=data_list[i][3]
        try:
            tts_list=eval(data_list[i][7])
        except:
            tts_list=[]
        try:
            testdata=json.loads(tdata)
        except:
            testdata='{'+tdata.replace('&',',')+'}'
            try:
                testdata = json.loads(testdata)
            except Exception as e:
                print(e)
            else:
                testdata=dict(queryinfo,**testdata)
        finally:
            print(testid)
            data['text'] = data_list[i][4]
            data["query_reply"]=testdata
            n = run_num
            while n>0:
                Response=Request().requests(url,data,"POST").json()
                tts=str(Response['data']['tts']['data'][0]['text'])
                print(tts)
                tts_list.append(tts)
                nlu = Response['data']['nlu']
                try:
                    lua = jsonpath.jsonpath(Response, "$..luaData")[0]
                except Exception as e:
                    lua=''
                print(lua)
                if n==1:
                    tts_list.append(tts)
                    tts_lists = list(set(tts_list))
                    print(tts_lists)
                    r.write_onlydata(w, i + 1, 5, str(nlu), sheetname=product_model)
                    r.write_onlydata(w, i + 1, 6, str(lua), sheetname=product_model)
                    r.write_onlydata(w, i + 1, 7, str(tts_lists), sheetname=product_model)
                else:
                    tts_list.append(tts)
                n-=1
        i+=1
    r.save_write(w,result_path)


if __name__=='__main__':
    product = "电压力锅"
    product_model="POWER601"
    # path="E:\AITEST\\testdata\空调远程控制-自动化案例.xls"
    path=Project_path.TestData_path+"%s自动化案例.xls"%product
    result_path = Project_path.TestData_path+"%s自动化案例1.xls"%product
    get_expectData(product_model, path, result_path,run_num=3)