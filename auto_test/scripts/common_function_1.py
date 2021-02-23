# coding: utf-8
# @Time : 2020-11-16 9:14 
# @Author : xx
# @File : common_function.py 
# @Software: PyCharm
import threading

import allure
from scripts import common_assert
from api.webscoket_api_1 import AiCloud
import time
from api.api import Api
from api.orionapi import OrionApi
import datetime
import re
from tools.file_tool_1 import FileTool
from tools.mylog import Logger
import config

log = Logger()
device_user_list = config.device_user_list


class Commonfunction():
    def runcase(self, caselist, devicetype, tool):
        log.info(f"开始{devicetype}测试,线程id:{threading.currentThread().ident}")
        global device_user_list
        for case in caselist:
            current_sheet = case.get('case_catory')
            case_id = case.get('case_id')
            case_name = case.get('case_name')
            case_lock = case.get('lock_device')
            is_wait = case.get('is_wait')
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
                        aicloud_ws = AiCloud(devicetype)
                        aicloud_ws.on_line()
                        for i in range(0, step_len):
                            current_step = step_list[i]  # 当前测试步骤
                            if i != step_len - 1:
                                params_value = current_step.get('params')
                                if devicetype == "xiaomei":
                                    result = OrionApi(params_value).orion_post()
                                else:
                                    log.info(f"当前测试步骤【{current_step}】")

                                    result = aicloud_ws.send_data(params_value,iswait=is_wait)
                                tool.write_excel(current_sheet, current_step.get("x_y"), "执行完成")
                                tool.write_excel(current_sheet, current_step.get("x_y_desc"), str(result))
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

    def run_xiaomei_step(self, case, tool, log):
        current_sheet = case.get('case_catory')
        step_list = case.get('steps')
        step_len = len(step_list)  # 步骤长度
        resultdir = {}
        for i in range(0, step_len):
            current_step = step_list[i]  # 当前测试步骤
            step_desc = current_step.get('step')  # 测试步骤的描述信息
            with allure.step(step_desc):
                if i == step_len - 1:
                    # 进行校验信息
                    try:
                        common_assert.assert_response(resultdir, current_step.get('params'))
                        tool.write_excel(current_sheet, current_step.get("x_y"), "执行通过")
                    except Exception as e:
                        tool.write_excel(current_sheet, current_step.get("x_y"), "执行失败! 原因:{}".format(e))
                        log.error("执行失败!原因:{}".format(e))
                        raise
                elif i == step_len - 2:
                    result = current_step.get('step_result')
                    assert_step = step_list[step_len - 1]
                    assert_params = assert_step.get('params')
                    if "device_status" in assert_params:
                        mid = result.get("mid")
                        self.search_device_status(mid, result, log)
                        tool.write_excel(current_sheet, current_step.get("x_y_desc"), str(result))

                    resultdir = result

    def runstep(self, r, case, w_tool):
        # current_sheet = case.get('case_catory')
        step_list = case.get('steps')
        step_len = len(step_list)  # 步骤长度
        resultdir = {}
        for i in range(0, step_len):
            current_step = step_list[i]  # 当前测试步骤
            step_desc = current_step.get('step')  # 测试步骤的描述信息
            with allure.step(step_desc):
                if i == step_len - 1:
                    # 进行校验信息
                    try:
                        common_assert.common_assert(resultdir, current_step.get('params'))

                        r.write_onedata(w_tool, current_step.get("x_y"), "执行通过")
                    except Exception as e:
                        r.write_onedata(w_tool, current_step.get("x_y"), "执行失败! 原因:{}".format(e))
                        log.error("执行失败!原因:{}".format(e))
                        raise
                elif i == step_len - 2:
                    result = eval(current_step.get('step_result'))
                    assert_step = step_list[step_len - 1]
                    assert_params = assert_step.get('params')
                    if "device_status" in assert_params:
                        mid = result.get("nlg").get("mid")
                        self.search_device_status(mid, result, log)
                        r.write_onedata(w_tool, current_step.get("x_y_desc"), str(result))

                    resultdir = result

    def search_device_status(self, mid, result, log):
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
        t0 = threading.Thread(target=Commonfunction().runcase, args=(testcaseinfo, device_type, tool,), name=f'线程{i}:{device_type}')
        # t2 = threading.Thread(target=demo2, kwargs={case_list}, name='线程2')
        ts.append(t0)
    for i in range(len(ts)):
        ts[i].start()
    for i in range(len(ts)):
        ts[i].join()


if __name__ == '__main__':
    run()
