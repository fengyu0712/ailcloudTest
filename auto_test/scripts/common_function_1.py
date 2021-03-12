# coding: utf-8
# @Time : 2020-11-16 9:14 
# @Author : xx
# @File : common_function.py 
# @Software: PyCharm
import threading
import random

import allure
import jsonpath
from api.meiju_api import Meijuapi
from scripts import common_assert
from api.webscoket_api_1 import AiCloud
import time
from api.apis import Api
from api.orionapi import OrionApi
import datetime
import re

from scripts.common_assert import assert_url_status_code
from tools.file_tool_1 import FileTool
from tools.mylog import Logger
import config
from api import clock_time

log = Logger()
device_user_list = config.device_user_list


class Commonfunction():
    def runcase(self, caselist, devicetype, tool):
        log.info(f"开始{devicetype}测试,线程id:{threading.currentThread().ident}")
        global device_user_list
        for case in caselist:
            case_category = case.get('case_category')
            if case_category in config.test_category:  # 筛选用例
                case_id = case.get('case_id')
                case_name = case.get('case_name')
                case_lock = case.get('lock_device')
                log.info(f"当前{devicetype}开始执行用例【{case_id}-{case_name}】")
                case_lock_list = []
                if case_lock:
                    if case_lock == "all":
                        case_lock_list = list(device_user_list.keys())
                    else:
                        case_lock_list = re.split(",", case_lock)
                while True:
                    is_lock = 0
                    for i in range(0, len(case_lock_list)):
                        if device_user_list[case_lock_list[i]] == 1:
                            is_lock = 1
                            break
                    if not is_lock:
                        for i in range(0, len(case_lock_list)):
                            device_user_list[case_lock_list[i]] = 1
                        if case_lock_list:
                            log.info(f"{devicetype}入口使用设备{case_lock_list}")

                        # 释放设备
                        def release_devices(devicetype, case_lock_list):
                            if case_lock_list:
                                log.info(f"{devicetype}入口开始释放设备{case_lock_list}")
                                for i in range(0, len(case_lock_list)):
                                    device_user_list[case_lock_list[i]] = 0

                        step_list = case.get('steps')
                        step_len = len(step_list)  # 步骤长度
                        try:
                            aicloud_ws = None
                            if devicetype not in ["yinxiang", "meiju"]:
                                aicloud_ws = AiCloud(devicetype)
                                aicloud_ws.on_line()
                            for i in range(0, step_len):
                                current_step = step_list[i]  # 当前测试步骤
                                if i != step_len - 1:
                                    params_value = current_step.get('params')
                                    is_wait = current_step.get('is_wait')
                                    if "clock_time" in params_value:
                                        params_value = clock_time.set_clock(params_value)
                                    if devicetype == "yinxiang":
                                        result = OrionApi(params_value).orion_post()
                                    elif devicetype == "meiju":
                                        result = Meijuapi().post(params_value)
                                    else:
                                        log.info(f"当前测试步骤【{current_step}】")
                                        try:
                                            result = aicloud_ws.send_data(params_value, iswait=is_wait)
                                            assert_url_status_code(result)
                                        except Exception as e:
                                            result = {"response_error": e}
                                    if result == None: result = {"error": f"{devicetype}接口超时"}
                                    tool.write_excel(case_category, current_step.get("x_y"), "执行完成")
                                    tool.write_excel(case_category, current_step.get("x_y_desc"), str(result))
                                    current_step['step_result'] = result

                            log.info(f"用例【{case_name}】执行完成")
                            release_devices(devicetype, case_lock_list)
                            break
                        except Exception as e:
                            # 如果测试报错则释放设备锁
                            release_devices(devicetype, case_lock_list)
                            raise e
                    else:
                        log.info(f"当前{devicetype}入口执行时，设备{case_lock_list}正在使用中")
                        time.sleep(1)

        log.info(f"{devicetype}入口测试用例已经运行完成")

    # def run_xiaomei_step(self, case, tool):
    #     current_sheet = case.get('case_category')
    #     step_list = case.get('steps')
    #     step_len = len(step_list)  # 步骤长度
    #     resultdir = {}
    #     for i in range(0, step_len):
    #         current_step = step_list[i]  # 当前测试步骤
    #         step_desc = current_step.get('step')  # 测试步骤的描述信息
    #         with allure.step(step_desc):
    #             if i == step_len - 1:
    #                 # 进行校验信息
    #                 try:
    #                     common_assert.assert_response(resultdir, current_step.get('params'))
    #                     tool.write_excel(current_sheet, current_step.get("x_y"), "执行通过")
    #                 except Exception as e:
    #                     tool.write_excel(current_sheet, current_step.get("x_y"), "执行失败! 原因:{}".format(e))
    #                     log.error("执行失败!原因:{}".format(e))
    #                     raise
    #             elif i == step_len - 2:
    #                 result = current_step.get('step_result')
    #                 assert_step = step_list[step_len - 1]
    #                 assert_params = assert_step.get('params')
    #                 if "device_status" in assert_params:
    #                     mid = jsonpath.jsonpath(result,"$..mid")[-1]
    #                     self.search_device_status(mid, result, log)
    #                     tool.write_excel(current_sheet, current_step.get("x_y_desc"), str(result))
    #
    #                 resultdir = result

    def runstep(self, device_type, r, case, w_tool):
        case_category = case.get('case_category')
        step_list = case.get('steps')
        step_len = len(step_list)  # 步骤长度
        # resultdir = {}
        for i in range(0, step_len):
            current_step = step_list[i]  # 当前测试步骤
            step_desc = current_step.get('step')  # 测试步骤的描述信息
            with allure.step(step_desc):
                if i == step_len - 1:
                    # 进行校验信息
                    try:
                        # 如果是小美音箱，对public技能进行特殊校验
                        publicskill = ["Public", "播放控制", "音量调节", "闹钟技能"]
                        yinxiang_assert = {"nlg": {'status': 500,
                                                   'nlu': '{"code":"200","data":{"nlu":{"classifier":"publicDomain"}},"message":"success"}'}}
                        meiju_assert = {"nlg": {'isMideaDomain': False, 'errorCode': "0"}}
                        if case_category in publicskill and device_type == "yinxiang":
                            current_step['params'] = yinxiang_assert
                        if case_category in publicskill and device_type == "meiju":
                            if case_category == "音量调节":
                                current_step['params'] = {"nlg": {'text': "抱歉", 'errorCode': "0"}}
                            else:
                                current_step['params'] = meiju_assert
                        common_assert.common_assert(device_type, resultdir, current_step.get('params'))
                        r.write_onedata(w_tool, current_step.get("x_y"), "执行通过")
                    except Exception as e:
                        r.write_onedata(w_tool, current_step.get("x_y"), "执行失败! 原因:{}".format(e))
                        log.error("执行失败!原因:{}".format(e))
                        raise
                elif i == step_len - 2:
                    result = current_step.get('step_result')
                    assert_step = step_list[step_len - 1]
                    assert_params = assert_step.get('params')
                    if "device_status" in assert_params:
                        if isinstance(result, str):
                            result = eval(result)
                        mid = jsonpath.jsonpath(result, "$..mid")[-1]
                        self.search_device_status(mid, result, log)
                        r.write_onedata(w_tool, current_step.get("x_y_desc"), str(result))
                    resultdir = result

    def search_device_status(self, mid, result, log):
        if isinstance(result, str):
            result = eval(result)
        i = 0
        apiobj = Api()
        log.info('开始获取设备状态。。。。。。{}'.format(datetime.datetime.now()))
        count = 3
        while i < count:
            time.sleep(1)
            jsonvalue = apiobj.post(mid)
            if jsonvalue.get("code") == 200:
                log.info('第{}次获取设备状态成功。。。。。。{}'.format(i, datetime.datetime.now()))
                result["device_status"] = jsonvalue
                break
            elif i == count - 1:
                result["device_status"] = jsonvalue
            i = i + 1


def cost_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        print(end_time - start_time)

    return wrapper


@cost_time
def run():
    ts = []
    device_type_list = config.main_device_list
    for i in range(0, len(device_type_list)):
        device_type = device_type_list[i]
        tool = FileTool("data_case.csv", device_type)
        tool.load_excel()
        # 读取excel的内容信息
        testcaseinfo = tool.read_excel()
        #打乱用例顺序，减少设备锁定时设备排队等待问题
        random.shuffle(testcaseinfo)
        t0 = threading.Thread(target=Commonfunction().runcase, args=(testcaseinfo, device_type, tool,),
                              name=f'线程{i}:{device_type}')
        # t2 = threading.Thread(target=demo2, kwargs={case_list}, name='线程2')
        ts.append(t0)
    for i in range(len(ts)):
        ts[i].start()
    for i in range(len(ts)):
        ts[i].join()


if __name__ == '__main__':
    run()
