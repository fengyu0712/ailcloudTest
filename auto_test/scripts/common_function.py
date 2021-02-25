# coding: utf-8
# @Time : 2020-11-16 9:14 
# @Author : xx
# @File : common_function.py 
# @Software: PyCharm
import threading

import allure
from scripts import common_assert
from api.webscoket_api import Mywebscoket
import time
from api.apis import Api
from api.orionapi import OrionApi
import datetime
import re
from tools.file_tool import FileTool

device_locks = {"AC1": 0, "AC2": 0, "FC1": 0, "D1": 0, "DB1": 0}
class Commonfunction():
    def runcase(self, caselist, devicetype, tool):
        print(f"开始{devicetype}测试")
        global device_locks
        for case in caselist:
            device_lock=case.get('lock_device')
            device_lock_list=[]
            while True:
                is_lock = 0
                if device_lock:
                    device_lock_list=re.split(",",device_lock)
                    print(device_lock_list)
                    for i in range(0,len(device_lock_list)):
                        is_lock=device_locks[device_lock_list[i]]+is_lock
                if not is_lock:
                    for i in range(0,len(device_lock_list)):
                        device_locks[device_lock_list[i]]=1
                    current_sheet = case.get('case_catory')
                    case_name=case.get('case_name')
                    print(f"当前执行用例{case_name}")
                    step_list = case.get('steps')
                    step_len = len(step_list)  # 步骤长度
                    for i in range(0, step_len):
                        current_step = step_list[i]  # 当前测试步骤
                        if i != step_len - 1:
                            params_value = current_step.get('params')
                            if devicetype=="xiaomei":
                                result=OrionApi(params_value).orion_post()
                            else:
                                result = Mywebscoket(params_value, devicetype).start_websocket()
                            tool.write_excel(current_sheet, current_step.get("x_y"), "执行完成")
                            tool.write_excel(current_sheet, current_step.get("x_y_desc"), str(result))
                            current_step['step_result'] = result
                    for i in range(0, len(device_lock_list)):
                        device_locks[device_lock_list[i]]=0
                    break
                else:
                    print(f"设备{device_lock_list}正在使用中")
                    time.sleep(1)

    def run_xiaomei_step(self,case,tool,log):
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


    def runstep(self, case, tool, devicetype, log):
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
                        common_assert.common_assert(resultdir, current_step.get('params'))
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
                        mid = result.get("nlg").get("mid")
                        self.search_device_status(mid, result, log)
                        tool.write_excel(current_sheet, current_step.get("x_y_desc"), str(result))

                    resultdir = result

    '''
    def runstep(self,case,tool,devicetype,log):
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
                        common_assert.common_assert(resultdir, current_step.get('params'))
                        tool.write_excel(current_sheet, current_step.get("x_y"), "执行通过")
                    except Exception as e:
                        tool.write_excel(current_sheet, current_step.get("x_y"), "执行失败! 原因:{}".format(e))
                        log.error("执行失败!原因:{}".format(e))
                        raise
                else:
                    params_value = current_step.get('params')
                    result = Mywebscoket(params_value, devicetype).start_websocket()
                    if i == step_len - 2:
                        assert_step = step_list[step_len - 1]
                        assert_params = assert_step.get('params')
                        if "device_status" in assert_params:
                            mid = result.get("nlg").get("mid")
                            self.search_device_status(mid,result,log)

                    tool.write_excel(current_sheet, current_step.get("x_y"), "执行完成")
                    tool.write_excel(current_sheet, current_step.get("x_y_desc"), str(result))
                    resultdir = result
    '''

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
    process_count = 8  # 进程数
    device_type_list=["328_halfDuplex","328_fullDuplex"]
    for i in range(0,len(device_type_list)):
        device_type=device_type_list[i]
        tool = FileTool("data_case.csv", device_type)
        # 读取excel的内容信息
        testcaseinfo = tool.read_excel()
        t0 = threading.Thread(target=Commonfunction().runcase, args=(testcaseinfo, device_type, tool,), name=f'线程{i}')
        # t2 = threading.Thread(target=demo2, kwargs={case_list}, name='线程2')
        ts.append(t0)
    for i in range(len(ts)):
        ts[i].start()
    for i in range(len(ts)):
        ts[i].join()


if __name__ == '__main__':
    run()
