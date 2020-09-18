from common.http_request_new import Request
from common.read_xls_news import Read_xls
from common.list_dict import Conversion
from common.log import Logger
import re,json

filepath='E:\python_space\AITEST\\testdata\\testdata.xls'
def DataConversion(filepath):
    testdata=Read_xls(filepath).read_data(start_line=2)
    # testdata1=testdata[redis_case]
    key_list=testdata[0][2:9]
    data_list=testdata[1:]
    list_datas = []
    for each in data_list:
        data = {}
        data['id']=each[0]
        data["场景描述"]=each[1]
        # data["校验"]=each[-redis_case]
        m = len(each) // 7
        for i in range(0, m):
            if i == 0:
                list0 = each[2:9]
            else:
                list0 = each[(i-1) * 7+9:7* i+9]
            onedata_dict=Conversion().list_dict(list0,key_list)
            data["接口%s"%(i+1)]=onedata_dict
            i+=1
        data["期望值"] = each[-1]
        # list_datas.append(str(data))
        list_datas.append(data)
    # Logger().log("测试数据读取完毕！")
    return list_datas

if __name__=="__main__":
    data=DataConversion(filepath)
    print(data)

data11={
		'url': 'http://bkt.jeagine.com/api/user/signin',
		'type': 'get',
		'header': '',
		'参数': "{'account': '13017600000', 'appKey': 'all', 'category_id': 80, 'password': '123456', 'terminal': 2}",
		'继承参数': '',
		'调用参数': '',
		'下传参数': '{"uid":"user=>id"}',
        '校验': '{"code":redis_case}'
	}

def OnlyInterface(**data):
    url = data['url']
    type = data['type']
    header = data['header']
    testdata = data['参数']
    check=data['校验']
    if isinstance(testdata,dict):
        pass
    else:
        try:
            testdata = eval(testdata)
        except Exception as e:
            Logger().error(e)
            testdata={}
    try:
        up_data = data['继承参数']
    except Exception as e:
        data['继承参数']={}
        Logger().error(e)
    else:
        try:
            up_data = eval(up_data)
        except Exception as e:
            Logger().error(e)
            up_data={}
    finally:
        up_data=data['继承参数']={}
    print(up_data)
            # raise e
    parameter = data['调用参数']
    downdata = data['下传参数']
    if header == '':
        header = {}
    else:
        try:
            header = eval(header)
        except Exception as e:
            Logger().error(e)
            header = {}
    if parameter=='':
        testdata = testdata
    else:
        try:
            parameter = eval(parameter)
        except Exception as e:
            Logger().error(e)
            parameter = ''
        else:
            for each in parameter:
                testdata[each] = up_data[each]
    respone = Request().requests(url, testdata, type,headers=header)
    if check=='':
        check = {}
    else:
        try:
            check = eval(check)
        except Exception as e:
            Logger().error(e)
            check = {}
    for each in check.keys():
        try :
            assert respone[each]==check[each],"接口【%s】响应校验失败"%url
        except Exception as e:
            raise e
        else:
            if downdata != '':
                try:
                    downdata=eval(downdata)
                except Exception as e:
                    downdata={}
                    Logger.error(e)
                else:
                    for key in downdata.keys():
                        down_value = downdata[key].split("=>")
                        s=respone
                        for i in range(0,len(down_value)):
                            s=s[down_value[i]]
                            i+=1
                        downdata[key] = s
                        up_data.update(downdata)
            result = [respone,up_data]
        return result
# if __name__=="__main__":
#     a=OnlyInterface(**data11)
#     print(a)


data2=	{
    "接口1": {
        "url": "http://bkt.jeagine.com/api/user/signin",
        "type": "get",
        "header": "",
        "参数": "{'account': '13017600000', 'appKey': 'all', 'category_id': 80, 'password': '123456', 'terminal': 2}",
        "调用参数": "",
        "下传参数": "{\"uid\":\"user=>id\"}",
        "校验": "{\"code\":redis_case}"
    },
    "接口2": {
        "url": "http://bkt.jeagine.com/api/user/mission/list",
        "type": "get",
        "header": "",
        "参数": "{\"uid\": \"\"}",
        "调用参数": "[\"uid\"]",
        "下传参数": "",
        "校验": "{\"code\":redis_case}"
    }
}

def InterfaceProcess(**data2):
    global up_data
    d_list=[]
    for each in data2.values():
        d_list.append(each)
    for i in range(0,len(d_list)):
        # print("======%s"%i)
        if i==0:
            result=OnlyInterface(**d_list[i])
            up_data=result[1]
        else:
            url=d_list[i]['url']
            if url!="":
                try:
                    parameter=eval(d_list[i]['调用参数'])
                except Exception as e:
                    Logger().error(e)
                    parameter={}
                # data=eval(d_list[i]['参数'])
                d_list[i]['继承参数']=up_data
                # if up_data1 == '':
                #     up_data1 = up_data
                # else:
                try:
                    up_data1=eval(up_data1)
                except Exception as e:
                    Logger().error(e)
                    up_data1={}
                finally:
                    up_data1.update(up_data)
                # for each in parameter:
                #     data[each]=up_data1[each]
                # d_list[i]['参数']=str(data)
                d_list[i]['继承参数']=str(up_data1)
                up_data = str(up_data1)
                result = OnlyInterface(**d_list[i])
            # else
        i += 1
    return  result
if __name__=="__main__":
    a=InterfaceProcess(**data2)
    print(a)

