import xlwt
from config import base_path
import os
from tools.mylog import Logger
import datetime
from scripts.init_env import current_env
import csv
import config

log = Logger()  # 初始化日志对象


class FileTool():

    def read_csv(self, file_path):
        data = []
        with open(file_path, encoding='gbk') as f:
            reader = csv.reader(f)
            header = next(reader)
            # print(header)
            for row in reader:
                data.append(row)
        return data

    def dict_info(self, data, devicetype=None, isindex=False, remote_device=None):
        # 不穿devicetype 时，取最后一个值，方便归类
        data_list = list()
        dictinfo = []
        allsteps = list()
        line = 0
        for i in range(len(data)):
            caseid = data[i][1]
            if caseid:
                if devicetype == None: devicetype = data[i][-2]
                dictinfo = {"case_category": data[i][0], "case_id": caseid, "case_name": data[i][2],
                            "lock_device": data[i][3], "steps": [], "devicetype": devicetype,
                            "remote_device": remote_device}
                dictinfo["devicetype"] = devicetype
                if data[i][0] in config.test_category:  # 筛选用例
                    data_list.append(dictinfo)
                    line += len(allsteps)
                    if isindex == True:
                        dictinfo["index"] = line + 1
                allsteps = list()
            step_dict = dict()
            if data[i][6] == None:
                continue
            step_dict["is_wait"] = data[i][4]
            step_dict["step"] = data[i][5]
            step_dict["params"] = data[i][6]
            step_dict["response"] = data[i][7]
            step_dict["result"] = data[i][8]
            allsteps.append(step_dict)
            if "steps" in dictinfo:
                dictinfo["steps"] = allsteps
        return data_list

    def dict_data_to_list(self, datainfo, add_devicetype=None):
        data_list = list()
        for case in datainfo:
            for i in range(len(case["steps"])):
                if i == 0:
                    one_data = [case["case_category"], case["case_id"], case["case_name"], case["lock_device"], ]
                else:
                    one_data = ["", "", "", ""]
                for value in list(case["steps"][i].values()):
                    one_data.append(value)
                if add_devicetype: one_data.append(case["devicetype"])
                data_list.append(one_data)
        return data_list

    def creat_ecxel(self):
        self.wb = xlwt.Workbook()

    def write_data(self, sheet_name, list_data):
        sheet = self.wb.add_sheet(sheet_name)
        header = ['用例分类', '用例编号', '用例名称', '锁定设备', 'is_wait', '测试步骤', '参数', '执行状态', '实际结果']
        for i in range(len(header)):
            sheet.write(0, i, header[i])
        for i in range(len(list_data)):
            for j in range(len(list_data[i])):
                sheet.write(i + 1, j, str(list_data[i][j]))

    def save_excel(self, path=None):
        nowdate = datetime.datetime.now().strftime('%Y-%m-%d-%H-%H-%S')
        if path == None:
            path = os.path.join(os.path.join(base_path, "result"), f"{current_env}_TestResult_{nowdate}.xls")
        self.wb.save(path)


def devicetype_info(data):
    # 按照devicetype 分割数据，方便写入不同表单
    test_info = {}
    for key in config.main_device_list:
        test_info[key] = []

    # for case in data:
    #     devicetype = case["devicetype"]
    #     test_info[devicetype].append(case)

    return test_info


if __name__ == '__main__':
    a = r"F:\git\Midea\auto_test\data\data_case.csv"
    b = r"F:\git\Midea\auto_test\data\open_api_case.csv"
    f = FileTool()
    data = f.read_csv(b)
    print(data)
    # data_list = f.dict_info(data, devicetype="3308", isindex=True)
    # print(data_list)
