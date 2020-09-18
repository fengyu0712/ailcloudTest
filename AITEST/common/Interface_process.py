from common.http_request_new import Request
from common.read_xls_news import Read_xls
from common.list_dict import Conversion
from common.log import Logger
import re, json

filepath = 'E:\AITEST\\testdata\\testdata1.xls'


def DataConversion(filepath, n=None, l=None):
    if n == None:
        n = 2
    if l == None:
        l = 8
    testdata = Read_xls(filepath).read_data(start_line=2)
    # testdata1=testdata[redis_case]
    key_list = testdata[0][n:(n + l)]
    data_list = testdata[1:]
    list_datas = []
    for each in data_list:
        data = {}
        data['id'] = each[0]
        data["场景描述"] = each[1]
        # data["校验"]=each[-redis_case]
        m = len(each) // l
        for i in range(0, m):
            if i == 0:
                list0 = each[n:(n + l)]
            else:
                list0 = each[i * l + n:(i + 1) * l + n]
            onedata_dict = Conversion().list_dict(list0, key_list)
            if onedata_dict["url"]!="":
                data["接口%s" % (i + 1)] = onedata_dict
        data["期望值"] = each[-1]
        # list_datas.append(str(data))
        list_datas.append(data)
        i += 1
    # Logger().log("测试数据读取完毕！")
    return list_datas


if __name__ == "__main__":
    data = DataConversion(filepath)
    print(data)

data11 = {
    'url': 'http://bkt.jeagine.com/api/user/signin',
    'type': 'get',
    'header': '',
    '参数': "{'account': '13017600000', 'appKey': 'all', 'category_id': 80, 'password': '123456', 'terminal': 2}",
    '继承参数': '',
    '调用参数': '',
    '下传参数': '{"uid":"user=>id"}',
    '校验': ''
}


def OnlyInterface(**data):
    url = data['url']
    type = data['type']
    header = data['header']
    testdata = data['参数']
    check = data['校验']
    if isinstance(testdata, dict):
        pass
    else:
        try:
            testdata = eval(testdata)
        except Exception as e:
            Logger().error(e)
            testdata = {}

    up_data = data['继承参数']
    if up_data == '':
        up_data = {}
    else:
        try:
            up_data = eval(up_data)
        except Exception as e:
            Logger().error(e)
            up_data = {}

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
    if parameter == '':
        testdata = testdata
    else:
        try:
            parameter = eval(parameter)
        except Exception as e:
            Logger().error(e)
            # parameter = ''
        else:
            for each in parameter:
                testdata[each] = up_data[each]
    respone = Request().requests(url, testdata, type, headers=header)
    respone = respone.json()

    try:
        if check != '':
            check = eval(check)
            for each in check.keys():
                assert respone[each] == check[each], "接口【%s】响应校验失败" % url
        else:
            Logger().info("跳过接口响应校验，测试继续")
    except Exception as e:
        Logger().error(e)
    else:
        if downdata != '':
            try:
                downdata = eval(downdata)
            except Exception as e:
                # downdata={}
                Logger().error(e)
            else:
                for key in downdata.keys():
                    down_value = downdata[key].split("=>")
                    s = respone
                    for i in range(0, len(down_value)):
                        s = s[down_value[i]]
                        i += 1
                    downdata[key] = s
                    up_data.update(downdata)
        result0 = [respone, up_data]
    return result0


if __name__ == "__main__":
    a = OnlyInterface(**data11)
    print(a)
    print("OnlyInterface==end!")

data2 = {'接口1': {
    'url': 'http://bkt.jeagine.com/api/user/signin',
    'type': 'get',
    'header': '',
    '参数': "{'account': '13017600000', 'appKey': 'all', 'category_id': 80, 'password': '123456', 'terminal': 2}",
    '继承参数': '',
    '调用参数': '',
    '下传参数': '{"uid":"user=>id"}',
    '校验': ''
},
    '接口2': {
        'url': 'http://bkt.jeagine.com/api/user/mission/list',
        'type': 'get',
        'header': '',
        '参数': '{"uid": ""}',
        '继承参数': '',
        '调用参数': '["uid"]',
        '下传参数': '',
        '校验': '{"code":redis_case}'
    }
}


def InterfaceProcess(**data2):
    global up_data
    d_list = []
    for each in data2.values():
        d_list.append(each)
    for i in range(0, len(d_list)):
        # print("======%s"%i)
        if i == 0:
            result = OnlyInterface(**d_list[i])
            up_data = result[1]
        else:
            url = d_list[i]['url']
            if url != "":
                try:
                    parameter = eval(d_list[i]['调用参数'])
                except Exception as e:
                    Logger().error(e)
                    parameter = {}
                # data=eval(d_list[i]['参数'])
                up_data1 = d_list[i]['继承参数']
                if up_data1 == '':
                    up_data1 = up_data
                else:
                    try:
                        up_data1 = eval(up_data1)
                    except Exception as e:
                        Logger().error(e)
                        up_data1 = {}
                    finally:
                        up_data1.update(up_data)
                # for each in parameter:
                #     data[each]=up_data1[each]
                # d_list[i]['参数']=str(data)
                d_list[i]['继承参数'] = str(up_data1)
                up_data = str(up_data1)
                result = OnlyInterface(**d_list[i])
        i += 1
    return result


if __name__ == "__main__":
    data = DataConversion(filepath)
    print(data)
    # tdata={'id': 2, '场景描述': '场景2', '接口1': {'url': 'http://bkt.jeagine.com/api/user/signin', 'type': 'get', 'header': '', '参数': "{'account': '13017600000', 'appKey': 'all', 'category_id': 80, 'password': '123456', 'terminal': 3}", '继承参数': '', '调用参数': '', '下传参数': '{"uid":"user=>id"}', '校验': ''}, '接口2': {'url': '', 'type': '', 'header': '', '参数': '', '继承参数': '', '调用参数': '', '下传参数': '', '校验': ''}, '期望值': ''}
    tdata=data[1]
    print(tdata)
    case_describe = tdata.pop('场景描述')
    id = tdata.pop('id')
    qiwang = tdata.pop('期望值')
    a = InterfaceProcess(**tdata)
    print(a)
