# coding: utf-8
# @Time : 2020-11-16 9:14 
# @Author : xx
# @File : common_function.py 
# @Software: PyCharm

import threading
import random
import queue
import allure
import jsonpath
from apscheduler.schedulers.blocking import BlockingScheduler

from api.meiju_api import Meijuapi
from scripts import common_assert
from api.webscoket_api import AiCloud
import time
from api.apis import Api
from api.orionapi import OrionApi
import datetime
import re
import os
from scripts.init_env import current_env
from tools.file_tool import FileTool
from tools.mylog import Logger
import config
from api import clock_time

log = Logger()
device_user_list = config.device_user_list
# remote_devices = config.remote_devices
all_caselist = list()
nowdate = datetime.datetime.now().strftime('%Y-%m-%d')

run_case_nums = {}
for devicetype in config.main_device_list:
    run_case_nums[devicetype] = 0
case_num = 143


def job():
    test_progress = f"================================\n********************************\n"
    for key in run_case_nums.keys():
        test_progress += f"执行进度：入口设备{key},\n已执行用例数量：【{run_case_nums[key]}】,\n剩余未执行数量：【{case_num - run_case_nums[key]}】\n"
    test_progress += f"********************************\n================================"
    print(test_progress)


# scheduler = BlockingScheduler()
# scheduler.add_job(job, 'interval', seconds=10)
# scheduler.start()


class Commonfunction():
    def runcase(self, caselist, devicetype, remote_device=None):
        global all_caselist
        case_num = len(caselist) + 1
        log.info(f"开始{devicetype}测试,线程id:{threading.currentThread().ident}")
        strt_time = time.time()
        global device_user_list, run_case_nums
        for case in caselist:
            run_case_nums[devicetype] += 1
            case_category = case.get('case_category')
            case["devicetype"] = devicetype
            case["remote_device"] = remote_device
            if case_category in config.test_category:  # 筛选用例
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
                            aicloud_ws = None
                            if devicetype not in ["yinxiang", "meiju"]:
                                aicloud_ws = AiCloud(devicetype, iswait=is_wait)
                                aicloud_ws.on_line()
                                time.sleep(0.1)
                            for i in range(0, step_len):
                                current_step = step_list[i]  # 当前测试步骤
                                if i != step_len - 1:
                                    params_value = current_step.get('params')

                                    if "clock_time" in params_value:
                                        params_value = clock_time.set_clock(params_value)
                                        print(params_value)
                                    if devicetype == "yinxiang":
                                        result = OrionApi(params_value).orion_post()
                                    elif devicetype == "meiju":
                                        result = Meijuapi().post(params_value)
                                    else:
                                        log.info(f"当前测试步骤【{current_step}】")
                                        try:
                                            result = aicloud_ws.send_data(params_value)
                                        except Exception as e:
                                            result = {"response_error": e}
                                    if result == None: result = {"error": f"{devicetype}接口超时"}
                                    current_step['response'] = result

                            log.info(f"用例【{case_name}】执行完成")
                            release_devices(devicetype, case_lock_list)
                            break
                        except Exception as e:
                            # 如果测试报错则释放设备锁
                            release_devices(devicetype, case_lock_list)
                            raise e
                    else:
                        log.info(f"当前{devicetype}入口执行用例{case_name}时，设备{case_lock_list}正在使用中")
                        time.sleep(1)
            if time.time() - strt_time > 120 or run_case_nums[devicetype] == case_num:
                job()
                strt_time = time.time()
        log.info(f"{devicetype}入口测试用例已经运行完成")
        all_caselist.append(caselist)

    def runstep(self, r, w, sheetname, case, result_file):
        if isinstance(case, str):
            case = eval(case)
        case_category = case.get('case_category')
        index = case["index"]
        step_list = case.get('steps')
        step_len = len(step_list)  # 步骤长度
        if case["devicetype"]:
            device_type = case["devicetype"]
        else:
            device_type = sheetname
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
                        yinxiang_assert = {"nlg": {
                            'nlu': '{"code":"200","data":{"nlu":{"classifier":"publicDomain"}}'}}
                        meiju_assert = {"nlg": {'code': 200, 'isMideaDomain': False, 'errorCode': "0"}}
                        if case_category in publicskill and device_type == "yinxiang":
                            current_step['params'] = yinxiang_assert
                        elif case_category in publicskill and device_type == "meiju":
                            if case_category == "音量调节":
                                current_step['params'] = {"nlg": {'text': "抱歉", 'errorCode': "0"}}
                            else:
                                current_step['params'] = meiju_assert
                        common_assert.common_assert(device_type, response, current_step.get('params'))
                    except Exception as e:
                        result = "执行失败! 原因:{}".format(e)
                        log.error("执行失败!原因:{}".format(e))
                        if "ws_error" in result:
                            error_type = "链接异常"
                        elif "asr" in result:
                            error_type = "ASR错误"
                        elif "nlg" in result:
                            error_type = "NLG错误"
                        elif "order_config" in result:
                            error_type = "本机order_config异常"
                        elif "闹钟" in result:
                            error_type = "闹钟下发异常"
                        elif "assert_media" in result:
                            error_type = "NLG错误"
                        elif "返回url为" in result:
                            error_type = "媒体技能返回异常"
                        elif "assert_url_status_code" in result:
                            error_type = "TTS或者媒体响应异常"
                        elif "assert_device_status" or "device_status错误" in result:
                            error_type = "设备状态校验错误"
                        else:
                            print(f"+++++++++++++{result}")
                            error_type = "链接异常"
                        raise e
                    else:
                        error_type = "执行通过"
                        result = "执行通过"
                    finally:
                        allure.dynamic.tag(error_type)
                        current_step["result"] = result
                        r.write_onlydata_new(w, index + i, 8, result, result_file, sheetname=sheetname)
                else:
                    response = current_step.get('response')
                    assert_step = step_list[step_len - 1]
                    assert_params = assert_step.get('params')
                    try:
                        if "device_status" in assert_params:
                            if isinstance(response, str):
                                response = eval(response)
                            mid = jsonpath.jsonpath(response, "$..mid")[-1]
                            self.search_device_status(mid, response, log)
                            current_step["response"] = response
                    except Exception as e:
                        result = "执行失败! 原因:{}".format(e)
                        log.error("执行失败!原因:{}".format(e))
                        error_type = "设备状态获取异常"
                        allure.dynamic.tag(error_type)
                        raise e
                    else:
                        result = "控制完成"
                    finally:
                        allure.attach(str(response), f"step{i + 1}_respone", allure.attachment_type.TEXT)
                        current_step["result"] = result
                        r.write_onlydata_new(w, index + i, 8, result, result_file, sheetname=sheetname)

    def search_device_status(self, mid, step_result, log):
        if isinstance(step_result, str):
            step_result = eval(step_result)
        i = 0
        apiobj = Api()
        log.info('开始获取设备状态。。。。。。{}'.format(datetime.datetime.now()))
        count = 1
        while i < count:
            time.sleep(1)
            jsonvalue = apiobj.post(mid)
            if jsonvalue.get("code") == 200:
                log.info('第{}次获取设备状态成功。。。。。。{}'.format(i, datetime.datetime.now()))
                step_result["device_status"] = jsonvalue
                break
            elif i == count - 1:
                step_result["device_status"] = jsonvalue
            i = i + 1


def cost_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        print(end_time - start_time)

    return wrapper


@cost_time
def run_main_case():
    ts = []
    main_devices = config.main_device_list
    print(main_devices)
    case_path = os.sep.join([os.path.dirname(os.path.dirname(__file__)), "data", "data_case.csv"])

    for i in range(len(main_devices)):
        device_type = main_devices[i]
        f = FileTool()
        cav_data = f.read_csv(case_path)
        testcaseinfo = f.dict_info(cav_data, isindex=True)
        # # 打乱用例顺序，减少设备锁定时设备排队等待问题
        random.shuffle(testcaseinfo)
        t0 = threading.Thread(target=Commonfunction().runcase, args=(testcaseinfo, device_type,),
                              name=f'线程{i}:{device_type}')
        ts.append(t0)

    for i in range(len(ts)):
        ts[i].setDaemon(True)  # 保证子线程在主线程退出时，无论出于什么状况都强制退出
        ts[i].start()
    for i in range(len(ts)):
        ts[i].join()
    resultfile = os.path.join(os.path.join(config.base_path, "result"),
                              f"{current_env}_MainCase_TestResult_{nowdate}.xls")
    write_result(resultfile)


def run_remote_devices(device_type, q):
    while True:
        remote_devices_list = q.get()
        q.task_done()
        if remote_devices_list:
            remote_device = remote_devices_list[0]
            print(f"{device_type}控制设备{remote_device}")
            remote_devices_list.remove(remote_device)
            q.put(remote_devices_list)
            case_path = os.sep.join(
                [os.path.dirname(os.path.dirname(__file__)), "data", "remote", f"{remote_device}.csv"])
            # 读取excel的内容信息
            f = FileTool()
            cav_data = f.read_csv(case_path)
            testcaseinfo = f.dict_info(cav_data, isindex=True)
            time.sleep(0.1)
            Commonfunction().runcase(testcaseinfo, device_type, remote_device=remote_device)
        else:
            q.put(None)  # 该步很重要，当producer()放入的None被某个consumer()抽取后，其他consumer()就没有结束标志了。缺点是最后queue中始终留有结束标志
            print("All data have been tooken out!")
            break


def run_remote_case():
    main_devices = config.main_device_list
    remote_devices = config.remote_devices.copy()
    q = queue.Queue()
    q.put(remote_devices)
    ts = []
    for i in range(len(main_devices)):
        device_type = main_devices[i]
        t0 = threading.Thread(target=run_remote_devices, args=(device_type, q), name=f'线程:{device_type}')
        ts.append(t0)
    for i in range(len(ts)):
        ts[i].setDaemon(True)  # 保证子线程在主线程退出时，无论出于什么状况都强制退出
        ts[i].start()
    for i in range(len(ts)):
        ts[i].join()
    resultfile = os.path.join(os.path.join(config.base_path, "result"),
                              f"{current_env}_RemoteCase_TestResult_{nowdate}.xls")
    write_result1(resultfile)


def write_result(path):
    f = FileTool()
    f.creat_ecxel()
    for i in range(len(all_caselist)):
        device_type = all_caselist[i][0]["devicetype"]
        device_type_data = all_caselist[i]
        device_type_data.sort(key=lambda x: x['case_id'])
        list_data = f.dict_data_to_list(device_type_data)
        f.write_data(device_type, list_data)
    f.save_excel(path)


def to_data(case_data):
    data = []
    remote_devices_list = config.remote_devices.copy()
    for remote_device in remote_devices_list:
        data0 = []
        for i in range(len(case_data)):
            for j in range(len(case_data[i])):
                if case_data[i][j]["remote_device"] == remote_device:
                    data0.append(case_data[i][j])
        data.append(data0)
    return data


def write_result1(path):
    f = FileTool()
    f.creat_ecxel()
    case_data = to_data(all_caselist)
    for i in range(len(case_data)):
        remote_device = case_data[i][0]["remote_device"]
        remote_device_data = all_caselist[i]
        # remote_device_data.sort(key=lambda x: x['case_id'])
        list_data = f.dict_data_to_list(remote_device_data, add_devicetype=True)
        f.write_data(remote_device, list_data)
    f.save_excel(path)


if __name__ == '__main__':
    # run_remote_case()
    run_main_case()
