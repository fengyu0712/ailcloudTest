# coding: utf-8
# 配置文件
'''
内容：文件的基路径
主机地址
excel数据对于的列信息
'''
import os

# 1、 基路径
base_path = os.path.dirname(__file__)

# 生成环境：wss://link.aimidea.cn:10443/cloud/connect
# 2、websocket的主机地址
host_address_list = {"dit": "ws://linkdit.aimidea.cn:10000/cloud/connect",
                     "sit": "ws://linksit.aimidea.cn:10000/cloud/connect",
                     "uat": "ws://linkuat.aimidea.cn:10000/cloud/connect",
                     # "pro": "wss://linkprod.aimidea.cn:10443/cloud/connect",
                     "pro": "wss://link.aimidea.cn:10443/cloud/connect",
                     "test": "wss://linkprod.aimidea.cn:10443/cloud/connect"
                     }

# 2、主机地址
device_status_list = {"dit": "http://sit.aimidea.cn:11003",
                      "sit": "http://sit.aimidea.cn:11003",
                      'uat': "https://uat.aimidea.cn:21023",
                      # "pro": "https://openapi-prod-tmp.aimidea.cn",
                      "pro": "https://api.aimidea.cn:11003",
                      "test": "https://openapi-prod-tmp.aimidea.cn/"
                      }

# 3、小美音箱地址
yinxiang_host_list = {
    "sit": "http://sit.aimidea.cn:11003",
    'uat': "https://uat.aimidea.cn:21023",
    "pro": "https://api.aimidea.cn:11003"
}

# 3、 excel数据对应的列
cell_config = {
    "case_category": 1,
    "case_id": 2,
    "case_name": 3,
    "lock_device": 4,
    "is_wait": 5,
    "step": 6,
    "params": 7,
    "result": 8,
    "desc": 9,
    "step_result": 9
}

open_api = {
    "case_id": 1,
    "Interface_name": 2,
    "case_name": 3,
    "serviceUrl": 4,
    "data": 5,
    "expect": 6,
    "response": 7,
    "result": 8
}

# 4、终端入口设备信息
# dit_terminal_devices = {
#     "328_halfDuplex": {"sn": "00000031122251059042507F12340000", "clientid": "a53e691f-cc5d-4a56-abed-e318c4afc478",
#             "deviceId": "10995116462812"},
#     "328_fullDuplex": {"sn": "00000031122251059042507F12340000", "clientid": "cf6411ef-976d-4292-a92a-1f0a765615b2",
#                        "deviceId": "10995116462812"},
#     "xf": {"sn": "00000031122251059042507F12340000", "clientid": "77ecd71d690e897b795c773d85f76802",
#            "deviceId": "10995116462812"},
#     "yuyintie_1": {"sn": "000008311000VA022091500000289FGR", "clientid": "yuyintie_test", "deviceId": "9895604650248"},
#     }

sit_terminal_devices = {
    # qq音乐链接
    "328_halfDuplex": {"sn": "00000021122251157813008987000000", "clientid": "test0001",
                       "deviceId": "3298544982176", "module_version": "07.03.01.01.f4.20.12.05.01.07"},
    # 酷狗音乐
    "328_fullDuplex": {"sn": "00000021122251157813008987000000", "clientid": "ed091219-a1c0-4993-9076-099641c34c6a",
                       "deviceId": "3298544982176", "module_version": "07.03.01.01.f4.20.12.05.01.07"},
    # 思必驰音乐
    "xf__halfDuplex": {"sn": "00000021122251157813008987000000", "clientid": "test0003",
                       "deviceId": "3298544982176", "module_version": "07.03.01.01.f4.20.12.05.01.07"},
    # 思必驰音乐
    "yuyintie_1": {"sn": "000008311000VA022091500000289FGR", "clientid": "test0004", "deviceId": "9895604650248",
                   "module_version": "07.03.01.01.f4.20.12.05.01.07"},
    # qq音乐转码
    "3308_halfDuplex": {"sn": "00000021122251157813008987000000", "clientid": "test0005", "deviceId": "3298544982176",
                        "module_version": "05.03.00.01.06.19.09.01.01.08"},

    "yinxiang": {"deviceid": "111000010213019416Z068", "uid": "80920524eedef3574e64c3dab72dd0bd"},
    "meiju": {"uid": "80920524eedef3574e64c3dab72dd0bd", "homeId": "1018545"}

}

# uat_terminal_devices = {
#     "328_halfDuplex": {"sn": "00000031122251059042507F12340000", "clientid": "b039414f-999c-46f4-ac89-22b8ef07fbb1",
#                        "deviceId": "166026256064412"},
#     "328_fullDuplex": {"sn": "00000031122251059042507F12340000", "clientid": "b039414f-999c-46f4-ac89-22b8ef07fbb1",
#                        "deviceId": "166026256064412"},
#     "xf": {"sn": "00000031122251059042507F12340000", "clientid": "c3ddaeb1-a19b-45ac-b06e-256fd0384bf2",
#            "deviceId": "166026256064412"},
#     "yuyintie_1": {"sn": "000008311000VA022091500000289FGR", "clientid": "yuyintie_test", "deviceId": "9895604650248"},
# }


pro_terminal_devices = {
    # qq音乐链接
    "328_halfDuplex": {"sn": "00000021122251157813008988650000", "clientid": "test0001",
                       "deviceId": "160528700040836", "module_version": "07.03.01.01.f4.20.12.05.01.07"},
    # 酷狗音乐
    "328_fullDuplex": {"sn": "00000021122251157813008988650000", "clientid": "test0002",
                       "deviceId": "160528700040836", "module_version": "07.03.01.01.f4.20.12.05.01.07"},
    # 思必驰音乐
    "xf__halfDuplex": {"sn": "00000021122251157813008988650000", "clientid": "test0003",
                       "deviceId": "160528700040836", "module_version": "07.03.01.01.f4.20.12.05.01.07"},
    # 思必驰音乐
    "yuyintie_1": {"sn": "000008311000VA022091500000289FGR", "clientid": "test0004", "deviceId": "9895604650248",
                   "module_version": "07.03.01.01.f4.20.12.05.01.07"},
    # qq音乐转码
    "3308_halfDuplex": {"sn": "00000021122251157813008988650000", "clientid": "test0005", "deviceId": "160528700040836",
                        "module_version": "05.03.00.01.06.19.09.01.01.08"},
    "yinxiang": {"deviceid": "111000010213019416Z031", "uid": "5668a004b73f4aa89ec5c3a19dc5defd"},
    "meiju": {"uid": "5668a004b73f4aa89ec5c3a19dc5defd", "homeId": "11207290"}

}

alltotal_devices = {"dit": sit_terminal_devices, "sit": sit_terminal_devices, "uat": pro_terminal_devices,
                    "pro": pro_terminal_devices, "test": pro_terminal_devices}

device_user_list = {"AC1": 0, "AC2": 0, "FC1": 0, "D1": 0, "DB1": 0}

# "yuyintie_1,xf__halfDuplex,,"328_fullDuplex"
main_device_list = ["328_halfDuplex", "328_fullDuplex", "3308_halfDuplex", "yinxiang", "meiju"]
# main_device_list = ["meiju", "328_fullDuplex"]
test_env = "uat"

test_category = ["多设备控制", "设备继承", "免设备名", "场景控制", "跨机控制", "查询类", "通用技能", "Public", "rasa", "故障码问询", "冰箱食材", "播放控制",
                 "音量调节", "闹钟技能", "自定义设备名"]

# test_category = ["通用技能", "Public", "rasa", "故障码问询", "冰箱食材", "播放控制", "音量调节", "闹钟技能", "跨机控制"]
# test_category = ["播放控制", "故障码问询", "跨机控制"]

# remote_devices = ["空调", "烤箱", "电压力锅", "智能灯", "加湿器", "电饭煲", "净水器", "蒸箱", "扫地机", "洗衣机", "烟机", "破壁机", "电热水器", "燃气热水器",
#                   "净化器", "微蒸烤一体机", "微波炉"]
remote_devices = ["灯", "灯1", "灯2", "灯3", "灯4"]
