# coding: utf-8
# 配置文件
'''
便于后期维护，增强灵活性
内容：文件的基路径
主机地址
excel数据对于的列信息
'''
import os

#1、 基路径
base_path=os.path.dirname(__file__)

# 2、websocket的主机地址
#host="ws://linksit.aimidea.cn:10000/cloud/connect"  # sit环境webscoket地址
host="ws://link.uat.aimidea.cn:10000/cloud/connect"  # uat环境websocket地址
#host="wss://link.aimidea.cn:10443/cloud/connect"   # pro环境websocket地址

# 3、http请求的主机地址,获取设备的状态
#http_host="http://sit.aimidea.cn:11003/v1/common/device/getDeviceStatus"  # sit环境查询设备状态接口
http_host="https://uat.aimidea.cn:11003/v1/common/device/getDeviceStatus"

# uat环境查询设备状态接口
#http_host="https://api.aimidea.cn:11003/v1/common/device/getDeviceStatus"  # 正式环境查询设备状态接口

# 3、 excel数据对应的列
cell_config={
    "case_id":1,
    "case_name":2,
    "step":3,
    "params":4,
    "result":5,
    "desc":6
}

# 4、终端入口设备信息
sit_deviceid="3298544982176"
pro_deviceid="166026256064412"

terminal_devices={"328":{"sn":"00000031122251059042507F12340000","clientid":"cf6411ef-976d-4292-a92a-1f0a765615b2","deviceId":"%s" % pro_deviceid},
                  "328_fullDuplex":{"sn":"00000031122251059042507F12340000","clientid":"cf6411ef-976d-4292-a92a-1f0a765615b2","deviceId":"%s" % pro_deviceid},
                  "yuyintie_1":{"sn":"000008311000VA022091500000289FGR","clientid":"yuyintie_test","deviceId":"9895604650248"},
                 }