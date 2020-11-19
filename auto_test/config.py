# coding: utf-8
# 配置文件
'''
便于后期维护，增强灵活性
内容：文件的基路径
主机地址
excel数据对于的列信息
'''
import  os
#1、 基路径
base_path=os.path.dirname(__file__)
# 2、websocket的主机地址
host="ws://linksit.aimidea.cn:10000/cloud/connect"
# 3、http请求的主机地址,获取设备的状态
#http_host="http://sit.aimidea.cn:11003/v1/common/device/getDeviceStatus"
http_host="https://apis-uat.aimidea.cn:11003/v1/common/device/getDeviceStatus"

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
terminal_devices={"328":"00000031122251059042507F12340000",
                  "328_fullDuplex":"00000031122251059042507F12340000",
                  }