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
                     "pro": "wss://linkprod.aimidea.cn:10443/cloud/connect"}

# 2、设备状态的主机地址
device_status_list = {"dit": "http://sit.aimidea.cn:11003/v1/common/device/getDeviceStatus",
                      "sit": "http://sit.aimidea.cn:11003/v1/common/device/getDeviceStatus",
                      'uat':"https://uat.aimidea.cn/v1/common/device/getDeviceStatus",
                      "pro": "https://openapi-prod-tmp.aimidea.cn/v1/common/device/getDeviceStatus"}

# 3、 excel数据对应的列
cell_config = {
    "case_id": 1,
    "case_name": 2,
    "step": 3,
    "params": 4,
    "result": 5,
    "desc": 6
}

# 4、终端入口设备信息
dit_terminal_devices = {
    "328": {"sn": "00000031122251059042507F12340000", "clientid": "a53e691f-cc5d-4a56-abed-e318c4afc478",
            "deviceId": "10995116462812"},
    "328_fullDuplex": {"sn": "00000031122251059042507F12340000", "clientid": "cf6411ef-976d-4292-a92a-1f0a765615b2",
                       "deviceId": "10995116462812"},
    "yuyintie_1": {"sn": "000008311000VA022091500000289FGR", "clientid": "yuyintie_test", "deviceId": "9895604650248"},
    }

uat_terminal_devices = {
    "328": {"sn": "00000031122251059042507F12340000", "clientid": "b039414f-999c-46f4-ac89-22b8ef07fbb1",
            "deviceId": "166026256064412"},
    "328_fullDuplex": {"sn": "00000031122251059042507F12340000", "clientid": "b039414f-999c-46f4-ac89-22b8ef07fbb1",
                       "deviceId": "166026256064412"},
    "yuyintie_1": {"sn": "000008311000VA022091500000289FGR", "clientid": "yuyintie_test", "deviceId": "9895604650248"},
    }

alltotal_devices = {"dit": dit_terminal_devices, "sit": dit_terminal_devices, "uat": uat_terminal_devices,
                    "pro": uat_terminal_devices}
