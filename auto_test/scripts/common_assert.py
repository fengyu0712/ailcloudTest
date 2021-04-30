# coding: utf-8
from urllib import request
import jsonpath
from api import clock_time
from tools.mylog import Logger

log = Logger()


def common_assert(device_type, response, excepect_dict):
    assert response != None, "response为空"
    print(response)
    print(excepect_dict)
    if isinstance(response, str):
        response = eval(response)
    if isinstance(excepect_dict, str):
        excepect_dict = eval(excepect_dict)

    # 闹钟时间转换
    if "clock_respone" in str(excepect_dict):
        excepect_dict["nlg"]["text"] = clock_time.clock_respone()
        excepect_dict["asr"]["text"] = clock_time.set_clock(excepect_dict["asr"]["text"])

    if device_type not in ["yinxiang", "meiju"]:
        # 断言：asr的text信息
        excepect_asr = excepect_dict.get('asr').get('text')
        try:
            result_asr = jsonpath.jsonpath(response, "$..asr")[-1]
        except:
            log.error(f"进行【断言 asr】时,response为：{response}，没有查找到asr信息")
            raise ValueError(f"进行【断言 asr】时,response为：{response}，没有查找到asr信息")
        else:
            assert result_asr == excepect_asr, f'asr错误！ 响应asr：{result_asr}，预期asr：{excepect_asr}'

    if device_type in list(excepect_dict.keys()):
        excepect_dict = excepect_dict[device_type]

    # 断言：nlg 的信息
    excepect_nlg = excepect_dict.get('nlg')
    for key in list(excepect_nlg.keys()):
        print(key)
        try:
            nlg_value = jsonpath.jsonpath(response, f"$..{key}")[-1]
        except:
            log.error(f"进行【断言 nlg】时，response为：{response}，没有查找到nlg相关键值信息")
            raise ValueError(f"进行【断言 nlg】时，response为：{response}，没有查找到nlg相关键值信息")
        else:

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
            try:
                result_order = jsonpath.jsonpath(response, "$..order")[-1]
            except:
                log.error(f"进行【断言 order_config】时，response为：{response}，没有查找到order信息")
                raise ValueError(f"进行【断言 order_config】时，response为：{response}，没有查找到order信息")
            else:
                assert excepect_dict.get('order_config')['order'] == result_order, \
                    f"下发order_config错误！下发order为{result_order},预期order{excepect_dict.get('order_config')['order']}"

        # 断言闹钟信息
        if excepect_dict.get('clock'):
            try:
                clock_url = jsonpath.jsonpath(response, '$..url')[-1]
            except:
                log.error(f"进行【断言闹钟信息】时，response为：{response}，没有查找到闹钟url信息")
                raise ValueError(f"进行【断言闹钟信息】时，response为：{response}，没有查找到闹钟url信息")
            else:
                assert excepect_dict.get('clock').get('url') == clock_url, "闹钟接收异常"

        # 媒体技能校验
        assert_media(response, device_type)


def assert_media(response, device_type):
    try:
        skillType = jsonpath.jsonpath(response, "$..skillType")[-1]
        skill_url = jsonpath.jsonpath(response, "$..url")[-1]
    except:
        log.error(f"进行【assert_media】时，response为：{response}，没有查找到skillType或者媒体链接信息")
        raise ValueError(f"进行【assert_media】时，response为：{response}，没有查找到skillType或者媒体链接信息")
    else:
        # 校验媒体技能
        if skillType == "music" and response.get("broadcast") == None:  # 音乐,且返回不属于推送(排除闹钟)
            if device_type == "328_halfDuplex":
                assert "isure6.stream.qqmusic.qq.com" in skill_url, "返回qq音乐资源异常，返回url为：%s" % {
                    jsonpath.jsonpath(response, "$..url")[1]}
            elif device_type == "328_fullDuplex":
                assert "fs.liebao.kugou.com" in skill_url, "返回酷狗音乐资源异常，返回url为：%s" % {
                    jsonpath.jsonpath(response, "$..url")[1]}
            elif device_type == "3308_halfDuplex":
                assert "audio-convert" in skill_url, "返回qq转码音乐资源异常，返回url为：%s" % {
                    jsonpath.jsonpath(response, "$..url")[1]}
            else:
                assert "mp3cdn.hifiok.com" in skill_url, "返回思必驰音乐链接异常，返回url为：%s" % {
                    jsonpath.jsonpath(response, "$..url")[1]}
        elif skillType == "story":  # 故事
            assert "aod.cos.tx.xmcdn.com" in skill_url, "返回喜马拉雅儿故事资源异常，返回url为：%s" % {
                jsonpath.jsonpath(response, "$..url")[1]}
        elif skillType == "joke":  # 笑话
            assert "aod.cos.tx.xmcdn.com" in skill_url, "返回喜马拉雅笑话资源异常，返回url为：%s" % {
                jsonpath.jsonpath(response, "$..url")[1]}
        elif skillType == "opera":  # 戏曲
            assert "aod.cos.tx.xmcdn.com" in skill_url, "返回喜马拉雅戏曲资源异常，返回url为：%s" % {
                jsonpath.jsonpath(response, "$..url")[1]}
        elif skillType == "crosstalk":  # 相声
            assert "aod.cos.tx.xmcdn.com" in skill_url, "返回喜马拉雅相声资源异常，返回url为：%s" % {
                jsonpath.jsonpath(response, "$..url")[1]}
        elif skillType == "otherAudio":  # 儿歌
            assert "aod.cos.tx.xmcdn.com" in skill_url, "返回喜马拉雅儿歌资源异常，返回url为：%s" % {
                jsonpath.jsonpath(response, "$..url")[1]}


def assert_url_status_code(response):
    try:
        urls = jsonpath.jsonpath(response, "$..url")
    except:
        log.error(f"进行【assert_url_status_code】时，response为：{response}，没有查找到url信息")
        raise ValueError(f"进行【assert_url_status_code】时，response为：{response}，没有查找到url信息")
    else:
        if urls:
            for url in urls:
                url_status_code = request.urlopen(url).status
                assert url_status_code == 200, f"返回链接:{url},无法正常打开，status_code={url_status_code}"


def assert_device_status(response, excepect_dict):
    # 断言：设备状态信息
    if "device_status" in excepect_dict:
        excepect_status = excepect_dict['device_status']
        try:
            device_status = response['device_status']
        except:
            log.error(f"进行【assert_device_status】时，response为：{response}，没有查找到device_status信息")
            raise ValueError(f"进行【assert_device_status】时，response为：{response}，没有查找到device_status信息")
        else:
            for key in excepect_status:
                try:
                    status_key_value = jsonpath.jsonpath(device_status, f"$..{key}")[-1]
                except:
                    log.error(f"进行【assert_device_status】时，response为：{response}，没有查找到{key}信息")
                    raise ValueError(f"进行【assert_device_status】时，response为：{response}，没有查找到{key}信息")
                else:
                    assert excepect_status[key] == status_key_value, f'device_status错误！ 响应code：' \
                                                                     f'{device_status}，预期code：{excepect_status}'


def getvalue(response, root_mark, node_mark):
    try:
        valuelist = jsonpath.jsonpath(response.get(root_mark), node_mark)
        value = ""
        if valuelist:
            value = valuelist[0]
    except Exception as e:
        raise e
    else:
        return value
