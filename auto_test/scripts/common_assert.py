# coding: utf-8
import jsonpath
def common_assert(response,excepect):
    excepect_dict=eval(excepect)

    # 断言：login 信息的响应码
    assert response.get('login').get('code') == excepect_dict.get('login').get('code'),'login错误！ 响应code：{}，预期code：{}'.format(response.get('login').get('code'),excepect_dict.get('login').get('code'))

    # 断言：lgoin 的message 信息
    assert response.get('login').get('message') == excepect_dict.get('login').get('message'),'login错误！ 响应message：{}，预期message：{}'.format(response.get('login').get('message'),excepect_dict.get('login').get('message'))

    # 断言: asr 信息的响应码
    assert response.get('asr').get('code') == excepect_dict.get('asr').get('code'),'asr错误！ 响应code：{}，预期code：{}'.format(response.get('asr').get('code'),excepect_dict.get('asr').get('code'))
    # 断言：asr的text信息
    asr_value=getvalue(response,'asr','$.data.asr')
    assert asr_value == excepect_dict.get('asr').get('text'),'asr错误！ 响应asr：{}，预期asr：{}'.format(asr_value,excepect_dict.get('asr').get('text'))

    # 断言: nlg 信息的响应码
    assert response.get('nlg').get('code') == excepect_dict.get('nlg').get('code'),'nlg错误！ 响应code：{}，预期code：{}'.format(response.get('nlg').get('code'),excepect_dict.get('nlg').get('code'))
    # 断言：nlg 的text信息
    nlg_value=getvalue(response,'nlg','$.data.tts.data[0].text')
    assert excepect_dict.get('nlg').get('text') in nlg_value,'nlg错误！ 响应nlg：{}，预期nlg：{}'.format(nlg_value,excepect_dict.get('nlg').get('text'))

    # 断言：设备状态信息
    if "device_status" in excepect_dict:
        device_dict=excepect_dict['device_status']
        for key in device_dict:
            if key=="code":
                assert response.get('device_status').get('code') == excepect_dict.get('device_status').get(
                    'code'), 'device_status错误！ 响应code：{}，预期code：{}'.format(response.get('device_status').get('code'),
                                                                 excepect_dict.get('device_status').get('code'))
            else:
                status_value = getvalue(response, 'device_status', '$.data.status.{}'.format(key))
                assert str(status_value)==str(excepect_dict.get('device_status').get(
                    key)), 'device_status错误！ 响应device_status：{}，预期device_status：{}'.format(status_value,
                                                                                                            excepect_dict.get(
                                                                                                                'device_status').get(
                                                                                                                key))

def getvalue(response,root_mark,node_mark):
    try:
        valuelist = jsonpath.jsonpath(response.get(root_mark),node_mark)
        value=""
        if len(valuelist) > 0:
            value = valuelist[0]
        return value
    except Exception as e:
        print("获取值，一次信息如下：%s"%e)
        return ""

