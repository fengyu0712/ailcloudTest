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

# 2、主机地址
device_status_list = {"dit": "http://sit.aimidea.cn:11003",
                      "sit": "http://sit.aimidea.cn:11003",
                      'uat': "https://uat.aimidea.cn",
                       "pro": "https://openapi-prod-tmp.aimidea.cn",
                      #"pro": "https://api.aimidea.cn"
                      }

# 3、 excel数据对应的列
cell_config = {
    "case_catory": 1,
    "case_id": 2,
    "case_name": 3,
    "step": 4,
    "params": 5,
    "result": 6,
    "desc": 7
}

# 4、终端入口设备信息
dit_terminal_devices = {
    "328": {"sn": "00000031122251059042507F12340000", "clientid": "a53e691f-cc5d-4a56-abed-e318c4afc478",
            "deviceId": "10995116462812"},
    "328_fullDuplex": {"sn": "00000031122251059042507F12340000", "clientid": "cf6411ef-976d-4292-a92a-1f0a765615b2",
                       "deviceId": "10995116462812"},
    "xf": {"sn": "00000031122251059042507F12340000", "clientid": "77ecd71d690e897b795c773d85f76802",
           "deviceId": "10995116462812"},
    "yuyintie_1": {"sn": "000008311000VA022091500000289FGR", "clientid": "yuyintie_test", "deviceId": "9895604650248"},
    }

uat_terminal_devices = {
    "328": {"sn": "00000031122251059042507F12340000", "clientid": "b039414f-999c-46f4-ac89-22b8ef07fbb1",
            "deviceId": "166026256064412"},
    "328_fullDuplex": {"sn": "00000031122251059042507F12340000", "clientid": "b039414f-999c-46f4-ac89-22b8ef07fbb1",
                       "deviceId": "166026256064412"},
    "xf": {"sn": "00000031122251059042507F12340000", "clientid": "c3ddaeb1-a19b-45ac-b06e-256fd0384bf2",
           "deviceId": "166026256064412"},
    "yuyintie_1": {"sn": "000008311000VA022091500000289FGR", "clientid": "yuyintie_test", "deviceId": "9895604650248"},
    }

alltotal_devices = {"dit": dit_terminal_devices, "sit": dit_terminal_devices, "uat": uat_terminal_devices,
                    "pro": uat_terminal_devices}
