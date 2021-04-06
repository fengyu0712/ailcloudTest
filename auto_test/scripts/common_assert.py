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
            assert excepect_status[key] == jsonpath.jsonpath(device_status,
                                                             f"$..{key}"), f'device_status错误！ 响应code：{device_status}，预期code：{excepect_status}'
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


if __name__ == '__main__':
    resp = {"code": 200, "data": {"volume": 5, "asr": "来一首歌", "tts": {"startSeq": 0, "data": [
        {"urlType": "tts", "skillType": "", "autoResume": False, "text": "好听的音乐，马上就来，为您播放:林俊杰的原来",
         "url1": "http://tts.dui.ai/runtime/v1/longtext/123f93df-b862-4480-a28c-8bec427d1167?productId=278575322",
         "seq": 0}, {"urlType": "media", "skillType": "", "autoResume": True, "text": "原来",
                     "url": "http://mp3cdn.hifiok.com/06/80/wKgBeVGQ58-AAomyAIE8iWsnkxY186.mp3?sign=8736e40c1474e1f8f631027e6e02d853&t=1614562518",
                     "seq": 1}, {"urlType": "media", "skillType": "", "autoResume": True, "text": "水手",
                                 "url": "http://mp3cdn.hifiok.com/09/7E/wKgB4VHHM0KAZHQvAKe9AcZinvs176.mp3?sign=16f7e479a8c72412da40edf682e4e29b&t=1614563123",
                                 "seq": 2}, {"urlType": "media", "skillType": "", "autoResume": True, "text": "美了美了",
                                             "url": "http://mp3cdn.hifiok.com/06/13/A2C5F4BA65aF2edA5459513B5Ae6cBC8.mp3?sign=b7d8e59410f028cd2a0d0484b526d237&t=1614559243",
                                             "seq": 3},
        {"urlType": "media", "skillType": "", "autoResume": True, "text": "没那么简单",
         "url": "http://mp3cdn.hifiok.com/00/07/453ea8A63CbfE99aeD62AbDCFBf7B084.mp3?sign=7f1b426c21a819ca18ae0c8c53b9f1e6&t=1614555023",
         "seq": 4}, {"urlType": "media", "skillType": "", "autoResume": True, "text": "送亲",
                     "url": "http://mp3cdn.hifiok.com/02/15/fcb5beeb609111e7911528cfe92119eb.mp3?sign=edbf8664a3cac76e83329452ba7568f6&t=1614564910",
                     "seq": 5}, {"urlType": "media", "skillType": "", "autoResume": True, "text": "亲亲",
                                 "url": "http://mp3cdn.hifiok.com/00/17/286FebF4FB1bd1A6fdEB0fB14c3DBBd5.mp3?sign=6db72a5319c3a15d00aef133cacada28&t=1614569029",
                                 "seq": 6}, {"urlType": "media", "skillType": "", "autoResume": True, "text": "夜猫",
                                             "url": "http://mp3cdn.hifiok.com/07/01/3bbDDEfE77887e9dd8FA0f5EfBC04ecc.mp3?sign=dea043bc26264995847449ec1dbb5dcc&t=1614555464",
                                             "seq": 7},
        {"urlType": "media", "skillType": "", "autoResume": True, "text": "从前",
         "url": "http://mp3cdn.hifiok.com/09/01/1cFdc4A4f6aacf3d1eEA1Bb58AFEa29B.mp3?sign=ac569e0fcc6f440b0d66e249f69fe616&t=1614564714",
         "seq": 8}, {"urlType": "media", "skillType": "", "autoResume": True, "text": "不同",
                     "url": "http://mp3cdn.hifiok.com/03/04/5D5AEEDdA1eA1de8176E80F8aAefa1AA.mp3?sign=ab6080bcd17d6112de101096f42af0fe&t=1614568611",
                     "seq": 9}, {"urlType": "media", "skillType": "", "autoResume": True, "text": "曾经心痛",
                                 "url": "http://mp3cdn.hifiok.com/07/48/wKgB4VGpVduADgIYAM_Q4MxLGZk948.mp3?sign=f07ee4ab0c180e48271608471659e54d&t=1614568042",
                                 "seq": 10}, {"urlType": "media", "skillType": "", "autoResume": True, "text": "执迷不悟",
                                              "url": "http://mp3cdn.hifiok.com/0A/3A/wKgB4VHgQE2AMrGUAJ0DiSzSGUI706.mp3?sign=790cf77cc3db4a2e28492848ede42527&t=1614555434",
                                              "seq": 11},
        {"urlType": "media", "skillType": "", "autoResume": True, "text": "忘情",
         "url": "http://mp3cdn.hifiok.com/15/07/148Fb8EA1Ea7356cdEb2ED96De9FEce0.mp3?sign=fe8b91ae8674ccf1a5018d473708dddc&t=1614566866",
         "seq": 12}, {"urlType": "media", "skillType": "", "autoResume": True, "text": "医生",
                      "url": "http://mp3cdn.hifiok.com/06/04/B1AD2f5d87FfEE6fB1DA363c92BCe0fc.mp3?sign=3e79292af294053d1575bc678f49e813&t=1614569343",
                      "seq": 13}, {"urlType": "media", "skillType": "", "autoResume": True, "text": "伤心城市",
                                   "url": "http://mp3cdn.hifiok.com/06/A9/wKgB4VGn95mATX8WAKQlIRXObDI520.mp3?sign=e3ab1f2c2b15e913de9ae8c342a5c43a&t=1614576057",
                                   "seq": 14}, {"urlType": "media", "skillType": "", "autoResume": True, "text": "十送红军",
                                                "url": "http://mp3cdn.hifiok.com/07/14/48FE24048f0b1Ff4Bd888baa8C2Cd0CF.mp3?sign=9bc726d93209f148b3ab1538d225cbfa&t=1614566269",
                                                "seq": 15}], "type": "Sort"}, "endSession": True,
                                  "skill": {"data": {}, "skillType": "music", "vendor": "dui"},
                                  "sessionId": "8bacbb777a5311eb936998e7f4f1e716", "version": "0.0.1", "class": "tts",
                                  "languageClass": ""}, "topic": "cloud.speech.reply",
            "mid": "8bacbb767a5311eb8e5798e7f4f1e716"}

    assert_url_status_code(resp)
