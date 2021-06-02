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

# 2、websocket的主机地址
ws_host_list = {"dit": "ws://linkdit.aimidea.cn:10000/cloud/connect",
                "sit": "ws://linksit.aimidea.cn:10000/cloud/connect",
                "uat": "ws://linkuat.aimidea.cn:10000/cloud/connect",
                "pro": "wss://link.aimidea.cn:10443/cloud/connect",
                "test": "ws://link-mock.aimidea.cn:10443/cloud/connect"
                }
# 2、meiju接口地址
meiju_host_list = {"dit": "http://sit.aimidea.cn:11003",
                   "sit": "http://sit.aimidea.cn:11003",
                   "uat": "https://iot-devicemanager-uat.aimidea.cn",
                   "pro": "https://iot-datatransmit.aimidea.cn",
                   # "test": "https://openapi-prod-tmp.aimidea.cn/"
                   }

# 4、小美音箱地址
yinxiang_host_list = {"dit": "http://sit.aimidea.cn:11003",
                      "sit": "http://sit.aimidea.cn:11003",
                      'uat': "https://uat.aimidea.cn:21023",
                      "pro": "https://api.aimidea.cn:11003",
                      "test": "http://sit.aimidea.cn:11003",
                      }
# 5、open_api地址
api_host_list = {"dit": "http://sit.aimidea.cn:11003",
                 "sit": "http://sit.aimidea.cn:11003",
                 "uat": "http://sit.aimidea.cn:11003",
                 # 'uat': "https://uat.aimidea.cn:21023",
                 "pro": "https://api.aimidea.cn:11003",
                 "test": "https://openapi-prod-tmp.aimidea.cn/"
                 }

# 6、设备状态查询地址
device_status_host_list = {"dit": "http://sit.aimidea.cn:11003",
                           "sit": "http://sit.aimidea.cn:11003",
                           "uat": "http://sit.aimidea.cn:11003",
                           # 'uat': "https://uat.aimidea.cn:21023",
                           "pro": "https://api.aimidea.cn:11003",
                           "test": "https://openapi-prod-tmp.aimidea.cn/"
                           }

#  excel数据对应的列
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

sit_terminal_devices = {
    # qq音乐链接
    "328_fullDuplex": {"sn": "00000021122251157813008987000000", "clientid": "test0001",
                       "deviceId": "3298544982176", "module_version": "07.03.01.01.f4.20.12.05.01.07"},
    # 酷狗音乐
    "328_halfDuplex": {"sn": "00000021122251157813008987010000", "clientid": "6fed03d8-37d3-4fd0-afd6-1204ae10b380",
                       "deviceId": "3298544982176", "module_version": "07.03.01.01.f4.20.12.05.01.07"},

    # 思必驰音乐
    "xf__halfDuplex": {"sn": "00000021122251157813008987000000", "clientid": "test0003",
                       "deviceId": "3298544982176", "module_version": "07.03.01.01.f4.20.12.05.01.07"},
    # 思必驰音乐
    # "yuyintie_1": {"sn": "000008311000VA022091500000289FGR", "clientid": "test0004", "deviceId": "9895604650248",
    #                "module_version": "07.03.01.01.f4.20.12.05.01.07"},
    # qq音乐转码
    "3308_halfDuplex": {"sn": "00000021122251157813008987000000", "clientid": "test0005", "deviceId": "3298544982176",
                        "module_version": "05.03.00.01.06.19.09.01.01.08"},

    "yinxiang": {"deviceid": "111000010213019416Z068", "uid": "80920524eedef3574e64c3dab72dd0bd",
                 "clientid": "0e215b2bc3f6cfa41cc3bfdc845b890c", "clientKey": "2cddc204b428ef114e29664704698dcd"},
    "meiju": {"uid": "80920524eedef3574e64c3dab72dd0bd", "homeId": "1018545"}
}

# pro_terminal_devices = {
#     "328_halfDuplex": {"sn": "00000021122251157813008987000000", "clientid": "test00011",
#                        "deviceId": "160528698598412",
#                        "module_version": "07.03.01.01.f4.20.12.05.01.07"},
#     "328_fullDuplex": {"sn": "00000021122251157813008987000000", "clientid": "d26004b02546667444e22400cdbd0762",
#                        "deviceId": "160528698598412",
#                        "module_version": "07.03.01.01.f4.20.12.05.01.07"},
#     "xf__halfDuplex": {"sn": "00000021122251157813008987000000", "clientid": "test00013",
#                        "deviceId": "160528698598412",
#                        "module_version": "07.03.01.01.f5.20.12.02.00.02"},
#     # "yuyintie_1": {"sn": "000008311000VA022091500000289FGR", "clientid": "test0014", "deviceId": "9895604650248",
#     #               "module_version": "07.03.01.01.f4.20.12.05.01.07"},
#     "3308_halfDuplex": {"sn": "00000021122251157813008988650000", "clientid": "test0015",
#                         "deviceId": "160528700040836",
#                         "module_version": "05.03.00.01.06.19.09.01.01.08"},
#     "yinxiang": {"deviceid": "111000010213019416Z031", "uid": "5668a004b73f4aa89ec5c3a19dc5defd",
#                  "clientid": "e256482c-2b93-4f79-bda5-c76da8de2129",
#                  "clientKey": "76f01e24-afc1-4a9c-879b-3d3e5941bda4", },
#     "meiju": {"uid": "5668a004b73f4aa89ec5c3a19dc5defd", "homeId": "11207290"}
#     # "meiju": {"uid": "a7da5f1093a94d40b45bb0ccf6fa21fc", "homeId": "19776793"}
# }


pro_terminal_devices = {
    # qq音乐链接
    "328_fullDuplex": {"sn": "00000021122251157813008988650000", "clientid": "test0001",
                       "deviceId": "160528700040836",
                       "module_version": "07.03.01.01.f4.20.12.05.01.07"},
    # 酷狗音乐
    "328_halfDuplex": {"sn": "00000021122251157813008988650000", "clientid": "fa4ddd66-1fb6-4e47-b17b-f10ba9602338",
                       "deviceId": "160528700040836",
                       "module_version": "07.03.01.01.f4.20.12.05.01.07"},
    # 思必驰音乐
    "xf__halfDuplex": {"sn": "00000021122251157813008988650000", "clientid": "test0003",
                       "deviceId": "160528700040836",
                       "module_version": "07.03.01.01.f5.20.12.02.00.02"},
    # "yuyintie_1": {"sn": "000008311000VA022091500000289FGR", "clientid": "test0004", "deviceId": "9895604650248",
    #               "module_version": "07.03.01.01.f4.20.12.05.01.07"},
    "3308_halfDuplex": {"sn": "00000021122251157813008988650000", "clientid": "test0005",
                        "deviceId": "160528700040836",
                        "module_version": "05.03.00.01.06.19.09.01.01.08"},
    "yinxiang": {"deviceid": "111000010213019416Z031", "uid": "5668a004b73f4aa89ec5c3a19dc5defd",
                 "clientid": "e256482c-2b93-4f79-bda5-c76da8de2129",
                 "clientKey": "76f01e24-afc1-4a9c-879b-3d3e5941bda4", },
    "meiju": {"uid": "5668a004b73f4aa89ec5c3a19dc5defd", "homeId": "11207290"}
}

alltotal_devices = {"dit": sit_terminal_devices, "sit": sit_terminal_devices, "uat": pro_terminal_devices,
                    "pro": pro_terminal_devices, "test": sit_terminal_devices}

device_user_list = {"AC1": 0, "AC2": 0, "FC1": 0, "DB1": 0, "CA": 0}

# "yuyintie_1,xf__halfDuplex,
# main_device_list = ["328_halfDuplex", "328_fullDuplex", "3308_halfDuplex", "meiju", "yinxiang"]
# main_device_list = ["328_fullDuplex"]
main_device_list = [ "meiju"]
test_env = "pro"

# test_category = ["多设备控制", "设备继承", "免设备名", "场景控制", "跨机控制", "查询类", "通用技能", "Public", "rasa", "故障码问询", "冰箱食材", "播放控制",
#                  "音量调节", "闹钟技能", "自定义设备名"]

# test_category = ["多设备控制", "设备继承", "免设备名", "跨机控制", "查询类"]
test_category = ["闹钟技能"]

# remote_devices = ["空调", "烤箱", "电压力锅", "智能灯", "加湿器", "电饭煲", "净水器", "蒸箱", "扫地机", "洗衣机", "烟机", "破壁机", "电热水器", "燃气热水器",
#                   "净化器", "微蒸烤一体机", "微波炉"]

remote_devices = ["灯", "灯1", "灯2", "灯3", "灯4"]
