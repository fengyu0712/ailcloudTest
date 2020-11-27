# coding: utf-8
# @Time : 2020-11-16 9:14 
# @Author : xx
# @File : common_function.py 
# @Software: PyCharm

import allure
from scripts import common_assert
from api.webscoket_api import Mywebscoket
import time
from api.api import Api
import datetime

class Commonfunction():
    def runcase(self,caselist,devicetype,tool):
        for case in caselist:
            current_sheet = case.get('case_catory')
            step_list = case.get('steps')
            step_len = len(step_list)  # 步骤长度
            for i in range(0, step_len):
                current_step = step_list[i]  # 当前测试步骤
                if i != step_len - 1:
                    params_value = current_step.get('params')
                    result = Mywebscoket(params_value, devicetype).start_websocket()
                    tool.write_excel(current_sheet, current_step.get("x_y"), "执行完成")
                    tool.write_excel(current_sheet, current_step.get("x_y_desc"), str(result))
                    current_step['step_result']=result

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

    def search_device_status(self,mid,result,log):
        i=0
        apiobj=Api()
        log.info('开始获取设备状态。。。。。。{}'.format(datetime.datetime.now()))
        count=3
        while i < count:
            time.sleep(1)
            jsonvalue=apiobj.post(mid)
            if jsonvalue.get("code")==200:
                log.info('第{}次获取设备状态成功。。。。。。{}'.format(i,datetime.datetime.now()))
                result["device_status"] =jsonvalue
                break
            elif i==count-1:
                result["device_status"] = jsonvalue

            i=i+1


