# coding: utf-8
from urllib import request
import jsonpath
from api import clock_time


def common_assert(device_type, response, excepect_dict):
    assert response != None, "response为空"
    print(response)
    print(excepect_dict)
    if isinstance(response, str):
        response = eval(response)
    if isinstance(excepect_dict, str):
        excepect_dict = eval(excepect_dict)
    # 设置家电入口，音箱入口和美居入口无闹钟和音乐等校验
    midea_entrances = ["328_halfDuplex", "328_fullDuplex", "3308_halfDuplex"]

    # 闹钟时间转换
    if "clock_respone" in str(excepect_dict):
        excepect_dict["nlg"]["text"] = clock_time.clock_respone()
        excepect_dict["asr"]["text"] = clock_time.set_clock(excepect_dict["asr"]["text"])

    if device_type not in ["yinxiang", "meiju"]:
        # 断言：asr的text信息
        excepect_asr = excepect_dict.get('asr').get('text')
        result_asr = jsonpath.jsonpath(response, "$..asr")[-1]
        assert result_asr == excepect_asr, f'asr错误！ 响应asr：{result_asr}，预期asr：{excepect_asr}'

    if device_type in list(excepect_dict.keys()):
        excepect_dict = excepect_dict[device_type]

    # 断言：nlg 的text信息
    excepect_nlg = excepect_dict.get('nlg')
    for key in list(excepect_nlg.keys()):
        print(key)
        nlg_value = jsonpath.jsonpath(response, f"$..{key}")[-1]
        if isinstance(excepect_nlg[key], str):
            assert excepect_nlg[key] in nlg_value, f'nlg：{key}错误！ 响应nlg：{nlg_value}，预期nlg：{excepect_nlg[key]}'
        else:
            assert excepect_nlg[key] == nlg_value, f'nlg：{key}错误！ 响应nlg：{nlg_value}，预期nlg：{excepect_nlg[key]}'

    assert response.get("response_error") == None, f"返回结果有错误：响应值：{str(response)}，期望值：{str(excepect_dict)}"
    # 校验设备状态
    assert_device_status(response, excepect_dict)
    if device_type not in ["yinxiang", "meiju"]:
        # 断言 order_config
        if excepect_dict.get('order_config'):
            result_order = jsonpath.jsonpath(response, "$..order")[-1]
            assert excepect_dict.get('order_config')['order'] == result_order, \
                f"下发order_config错误！下发order为{result_order},预期order{excepect_dict.get('order_config')['order']}"

        # 断言闹钟信息
        if excepect_dict.get('clock'):
            assert excepect_dict.get('clock').get('url') == jsonpath.jsonpath(response, '$..url')[-1], "闹钟接收异常"

        # 媒体技能校验
        assert_media(response, device_type)


def assert_media(response, device_type):
    # 校验媒体技能
    if jsonpath.jsonpath(response, "$..skillType")[-1] == "music" and \
            response.get("broadcast") == None:  # 音乐,且返回不属于推送(排除闹钟)
        if device_type == "328_halfDuplex":
            assert "isure6.stream.qqmusic.qq.com" in jsonpath.jsonpath(response, "$..url")[1], \
                "返回qq音乐资源异常，返回url为：%s" % {
                    jsonpath.jsonpath(response, "$..url")[1]}
        elif device_type == "328_fullDuplex":
            assert "fs.liebao.kugou.com" in jsonpath.jsonpath(response, "$..url")[1], \
                "返回酷狗音乐资源异常，返回url为：%s" % {
                    jsonpath.jsonpath(response, "$..url")[1]}
        elif device_type == "3308_halfDuplex":
            assert "audio-convert" in jsonpath.jsonpath(response, "$..url")[1], \
                "返回qq转码音乐资源异常，返回url为：%s" % {
                    jsonpath.jsonpath(response, "$..url")[1]}
        else:
            assert "mp3cdn.hifiok.com" in jsonpath.jsonpath(response, "$..url")[1], \
                "返回思必驰音乐链接异常，返回url为：%s" % {
                    jsonpath.jsonpath(response, "$..url")[1]}
    elif jsonpath.jsonpath(response, "$..skillType")[-1] == "story":  # 故事
        assert "aod.cos.tx.xmcdn.com" in jsonpath.jsonpath(response, "$..url")[1], "返回喜马拉雅儿故事资源异常，返回url为：%s" % {
            jsonpath.jsonpath(response, "$..url")[1]}
    elif jsonpath.jsonpath(response, "$..skillType")[-1] == "joke":  # 笑话
        assert "aod.cos.tx.xmcdn.com" in jsonpath.jsonpath(response, "$..url")[1], "返回喜马拉雅笑话资源异常，返回url为：%s" % {
            jsonpath.jsonpath(response, "$..url")[1]}
    elif jsonpath.jsonpath(response, "$..skillType")[-1] == "opera":  # 戏曲
        assert "aod.cos.tx.xmcdn.com" in jsonpath.jsonpath(response, "$..url")[1], "返回喜马拉雅戏曲资源异常，返回url为：%s" % {
            jsonpath.jsonpath(response, "$..url")[1]}
    elif jsonpath.jsonpath(response, "$..skillType")[-1] == "crosstalk":  # 相声
        assert "aod.cos.tx.xmcdn.com" in jsonpath.jsonpath(response, "$..url")[1], "返回喜马拉雅相声资源异常，返回url为：%s" % {
            jsonpath.jsonpath(response, "$..url")[1]}
    elif jsonpath.jsonpath(response, "$..skillType")[-1] == "otherAudio":  # 儿歌
        assert "aod.cos.tx.xmcdn.com" in jsonpath.jsonpath(response, "$..url")[1], "返回喜马拉雅儿歌资源异常，返回url为：%s" % {
            jsonpath.jsonpath(response, "$..url")[1]}


def assert_url_status_code(response):
    urls = jsonpath.jsonpath(response, "$..url")
    if urls:
        for url in urls:
            url_status_code = request.urlopen(url).status
            assert url_status_code == 200, f"返回链接:{url},无法正常打开，status_code={url_status_code}"


def assert_device_status(response, excepect_dict):
    # 断言：设备状态信息
    if "device_status" in excepect_dict:
        excepect_status = excepect_dict['device_status']
        device_status = response['device_status']
        for key in excepect_status:
            assert excepect_status[key] == jsonpath.jsonpath(device_status, f"$..{key}")[-1] \
                , f'device_status错误！ 响应code：{device_status}，预期code：{excepect_status}'
            # if key == "code":
            #     assert response.get('device_status').get('code') == excepect_dict.get('device_status').get(
            #         'code'), 'device_status错误！ 响应code：{}，预期code：{}'.format(response.get('device_status').get('code'),
            #                                                                excepect_dict.get('device_status').get(
            #                                                                    'code'))
            # else:
            #     print(response)
            #     status_value = jsonpath.jsonpath(response, f"$..{key}")[0]
            #     assert str(status_value) == str(excepect_dict.get('device_status').get(
            #         key)), 'device_status错误！ 响应device_status：{}，预期device_status：{}'.format(status_value,
            #                                                                                excepect_dict.get(
            #                                                                                    'device_status').get(
            #                                                                                    key))


def getvalue(response, root_mark, node_mark):
    try:
        valuelist = jsonpath.jsonpath(response.get(root_mark), node_mark)
        value = ""
        if len(valuelist) > 0:
            value = valuelist[0]
        return value
    except Exception as e:
        raise e
