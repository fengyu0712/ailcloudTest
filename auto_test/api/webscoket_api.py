# coding: utf-8
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from jsonpath import jsonpath
from websocket import ABNF
import websocket, time, json, gc

from api.audio_generation import audio_generation
from config import base_path
from devices_info_1 import Deviceset
import os
from tools.mylog import Logger
from scripts.init_env import ws_host, current_env

log = Logger()  # 初始化日志对象

volume_conf = {
    "L1": 1,
    "L2": 25,
    "L3": 50,
    "L4": 75,
    "L5": 100,
}


# 重试装饰器
def retry(rerun_count):
    def wrapper(request):
        def inner_wrapper(*args, **kwargs):
            nonlocal rerun_count
            for i in range(rerun_count):
                try:
                    response = request(*args, **kwargs)
                except Exception as e:
                    if i == rerun_count - 1:
                        raise e
                    else:
                        log.warning(f"第{i}次请求失败")
                else:
                    return response

        return inner_wrapper

    return wrapper


class AiCloud():
    # rootpath: 音频名称
    # termianl_type : 终端类型
    # is_need_devices_status : 表示为需要获取设备信息
    def __init__(self, terminal_type, iswait=None, device_info=None):
        print("测试环境细腻系：", current_env)
        self.address = ws_host
        # self.address = "wss://link-mock.aimidea.cn:10443/cloud/connect"
        print("当前测试环境为:", ws_host)
        self.step = 3200
        self.terminal_type = terminal_type
        if not iswait:
            self.iswait = 0
        else:
            self.iswait = int(iswait)
        self.ws = self.client_ws()
        self.device_info = device_info

    def client_ws(self):
        log.info("开始ws的链接")
        # ws = websocket.create_connection(self.address, timeout=15)
        ws = websocket.create_connection(self.address, timeout=15 + self.iswait * 60)
        log.info("建立ws的链接成功")
        return ws

    def on_line(self):
        try:
            # 开始云端上线
            self.ws.send(json.dumps(Deviceset(self.terminal_type, device_info=self.device_info).online_data()),
                         ABNF.OPCODE_TEXT)
            # 开始上报设备音量信息
            self.ws.send(json.dumps(Deviceset(self.terminal_type, device_info=self.device_info).audio_staus_data()),
                         ABNF.OPCODE_TEXT)
            # # 开始上报设备OTA信息
            self.ws.send(json.dumps(Deviceset(self.terminal_type, device_info=self.device_info).ota_check()),
                         ABNF.OPCODE_TEXT)
        except Exception as e:
            self.ws.close()
            raise (f"错误信息信息为:{e}")
        # if self.terminal_type=="328_fullDuplex":
        #     # 发送头部信息
        #     self.ws.send(json.dumps(Deviceset(self.terminal_type, device_info=self.device_info).content_data()),
        #                  ABNF.OPCODE_TEXT)
        # else:
        #     return self.ws

    def send_staus(self, staus_data):
        self.ws.send(json.dumps(staus_data), ABNF.OPCODE_TEXT)

    # @retry(rerun_count=3)
    def send_data(self, audio_name):
        self.wavpath = os.path.join(base_path + os.sep + "audio_file" + os.sep, audio_name + ".wav")
        if not os.path.exists(self.wavpath):
            log.info("未找到音频文件，开始重新生成音频...")
            audio_generation(audio_name)
        try:
            # if self.terminal_type != "328_fullDuplex":
            # 发送头部信息
            self.ws.send(json.dumps(Deviceset(self.terminal_type, device_info=self.device_info).content_data()),
                         ABNF.OPCODE_TEXT)
            log.info("开始发送音频数据......................")
            with open(self.wavpath, 'rb') as f:
                while True:
                    data = f.read(self.step)
                    if data:
                        self.ws.send(data, ABNF.OPCODE_BINARY)
                    if len(data) < self.step:
                        break
                    time.sleep(0.1)
            self.ws.send('', ABNF.OPCODE_BINARY)
            result = self.get_message()
            gc.collect()
        except Exception as e:
            self.ws.close()
            result = {"ws_error": e}
            raise ("发送音频数据异常,原因:{}".format(e))
        else:
            if jsonpath(result, "$..audio"):
                volume = 50
                nlg_volume = jsonpath(result, "$..volume")[-1]
                if nlg_volume in list(volume_conf.keys()):
                    volume = volume_conf[nlg_volume]
                elif nlg_volume == "-20":
                    volume = volume - 25
                elif nlg_volume == "+20":
                    if volume == 1:
                        volume = 25
                    else:
                        volume = volume + 25
                else:
                    volume = int(nlg_volume)
                if volume < 1: volume = 1
                if volume > 100: volume = 100
                self.ws.send(json.dumps(
                    Deviceset(self.terminal_type, device_info=self.device_info).audio_staus_data(volume=volume)),
                    ABNF.OPCODE_TEXT)
                time.sleep(1)
            elif jsonpath(result, "$..skillType")[-1] == "music":
                self.ws.send(json.dumps(Deviceset(self.terminal_type, device_info=self.device_info).send_play_status()),
                             ABNF.OPCODE_TEXT)
                time.sleep(1)
            elif jsonpath(result, "$..player"):
                player_status = jsonpath(result, "$..player")[-1]
                self.ws.send(json.dumps(Deviceset(self.terminal_type, device_info=self.device_info).send_play_status(
                    status=player_status.lower())),
                    ABNF.OPCODE_TEXT)
                time.sleep(1)
            elif jsonpath(result, "$..playMode"):
                playMode = jsonpath(result, "$..mode")[-1]
                self.ws.send(json.dumps(Deviceset(self.terminal_type, device_info=self.device_info).send_play_status(
                    status=playMode.lower())),
                    ABNF.OPCODE_TEXT)
                time.sleep(1)
            # 校验url是否可以正常访问
            from scripts.common_assert import assert_url_status_code
            assert_url_status_code(result)
        finally:
            return result

    def wait_clock(self):
        log.info("等待云端下发闹钟指令中...")
        while True:
            self.ws.send("HeartBeat")
            result = self.ws.recv()
            result = result.replace("false", "False").replace("true", "True")
            if "cloud.speech.broadcast" in result:
                log.info("接收的cloud.speech.broadcast信息为:{}".format(result))
                return eval(result)

    def close(self):
        self.ws.close()
        log.info("ws链接关闭")

    def get_message(self):
        result_dict = {"login": {}, "asr": {}, "nlg": {}}
        try:
            log.info("开始接收数据......................")
            while result_dict["nlg"] == {}:
                result = self.ws.recv()
                result = result.replace("false", "False").replace("true", "True")
                if "cloud.online.reply" in result:
                    log.info("接收的online信息为:{}".format(result))
                    result_dict['login'] = eval(result)
                elif "cloud.speech.trans.ack" in result:
                    log.info("接收的cloud.speech.trans.ack信息为:{}".format(result))
                    result_dict["asr"] = eval(result)
                elif "cloud.order.config" in result:
                    log.info("接收的cloud.order.config信息为:{}".format(result))
                    result_dict["order_config"] = eval(result)
                elif "cloud.speech.reply" in result:
                    log.info("接收的cloud.speech.reply信息为:{}".format(result))
                    nlg_result = eval(result)
                    result_dict["nlg"] = nlg_result
                    if "insert" in result and self.iswait and jsonpath(nlg_result, "$..time")[0]:
                        result_dict["broadcast"] = self.wait_clock()
                    else:
                        break
                else:
                    log.info("接收到非关键信息为:{}".format(result))
                    time.sleep(0.1)
        except Exception as e:
            result_dict["error"] = e
            log.error("错误信息信息为:{}".format(e))
            raise ("错误信息信息为:{}".format(e))

        return result_dict


if __name__ == '__main__':
    info = {"sn": "00000021122251157813008987000000", "clientid": "test",
            "deviceId": "3298544982176", "module_version": "07.03.01.01.f4.20.12.05.01.07"}
    # aiyuncloud = AiCloud("328_fullDuplex")
    aiyuncloud = AiCloud("3308_halfDuplex")
    aiyuncloud.on_line()
    aiyuncloud.send_data('晾衣架上升')
    # aiyuncloud.send_data('关闭卧室空调')
    # aiyuncloud = AiCloud("328_halfDuplex")
    # aiyuncloud.on_line()
    # aiyuncloud.send_data('室内空气质量怎么样')
    # aiyuncloud.send_data('晚上八点')
    # aiyuncloud.send_data('明天呢')
    # time.sleep(5)
    # n = 1
    # while True:
    #     print(n)
    #     aiyuncloud.send_data('顺序播放')
    #     n += 1
    #     time.sleep(3)
    # def job():
    #     aiyuncloud = AiCloud("328_halfDuplex")
    #     aiyuncloud.on_line()
    #     aiyuncloud.send_data('帮我订一个零点的二十的闹钟')
    # scheduler = BlockingScheduler()
    # scheduler.add_job(job, 'date', run_date='2021-05-18 0:25:00')
    # scheduler.start()
    # while True:
    #     now = datetime.now()
    #     if now.hour == 0 and now.minute>20:
    #         aiyuncloud = AiCloud("328_halfDuplex")
    #         aiyuncloud.on_line()
    #         aiyuncloud.send_data('帮我订一个零点的二十的闹钟')
    #         break
    #     else:
    #         print(now.minute)
    #         print(now)
    #         time.sleep(300)
    # n = 1
    # while True:
    #     print(n)
    #     aiyuncloud.send_data('关闭净化器')
    #     aiyuncloud.send_data('明天的天气')
    #     n += 1
    # result = aiyuncloud.send_data('打开卧室空调')
    # # b = jsonpath(result, "$..url")[1]
    # b = jsonpath(result, "$..order")

    # result = aiyuncloud.send_data('继续播放')

    # print(result)

    # result = aiyuncloud.send_data('帮我定个一分钟以后的闹钟')

    # print(result)
    # result = aiyuncloud.send_data('当前音量是多少')
    # print(result)
    # result = aiyuncloud.send_data('音量设为百分之六十五')
    # print(result)
    # result = aiyuncloud.send_data('来一首歌')
    # # print(result)
    #
    # # print(result)
    # result = aiyuncloud.send_data('继续播放')
    # # print(result)
    # # print(result)
    # result = aiyuncloud.send_data('暂停播放', )
    # # # print(result)
    # result = aiyuncloud.send_data('停止播放')
    # # # print(result)
    # result = aiyuncloud.send_data('继续播放')
