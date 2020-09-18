import datetime
import re
import time
import xlsxwriter

#唯一唤醒日志计算统计脚本

class WriteExcel:
    def __init__(self, path):
        self.wb = xlsxwriter.Workbook(path)

    def creattable(self, sheet_name):
        # self.wb.
        self.sheet = self.wb.add_worksheet(sheet_name)

    def write_onlydata(self, row, col, vale):
        self.sheet.write(row, col, vale)

    def write_linedata(self, row, list_data, start_col=None):
        if start_col == None:
            start_col = 0
        for i in range(len(list_data)):
            self.write_onlydata(row, i + start_col, list_data[i])

    def close(self, ):
        self.wb.close()


def DiffTime(date1, date2):
    # %Y-%m-%d为日期格式，其中的-可以用其他代替或者不写，但是要统一，同理后面的时分秒也一样；可以只计算日期，不计算时间。
    date1 = datetime.datetime.strptime(date1, "%Y-%m-%d %H:%M:%S.%f")
    date2 = datetime.datetime.strptime(date2, "%Y-%m-%d %H:%M:%S.%f")

    # 返回两个变量相差的值，就是相差时间,最后转换为分钟返回
    return (date2 - date1)


log_path = "E:\\log\\20200731\\"
path1 = log_path + "multi_wake_log_073109_1"
path2 = log_path + "multi_wake_log_073109_2"
path3 = log_path + "multi_wake_log_073109_3"
path4 = log_path + "2020-07-31.log"
nowdate = time.strftime('%Y%m%d-%H')


a1 = r"\[(.+?)\](.*)current:(.+?)\n((?:.|\n)*?)\[(.+?)\](.*)get wakeup_flag:(.+?)"
a11 = "\[(.+?)\].*current:(.+?),signal:(.+?),noisy:(.+?)\n(?:.|\n)*?\[(.+?)\].*get wakeup_flag:(.+?)"
a2 = r"\[(.+?)\] - .* - 第(.*)次播放：.*\\(.+?).wav"
# a3 = r"\[(.+?)\] - .*"

with open(path1, "r", encoding='utf-8') as r1, open(path2, "r", encoding='utf-8') as r2, open(path3, "r",
                                                                                              encoding='utf-8') as r3, open(
    path4, "r", encoding='utf-8') as r4:
    log1 = r1.read()
    log2 = r2.read()
    log3 = r3.read()
    log4 = r4.read()
result1 = re.findall(a11, log1)
result2 = re.findall(a11, log2)
result3 = re.findall(a11, log3)
result0 = re.findall(a2, log4)


Round = 0  #统计轮次
result_path = 'G:\python\AITEST\TestResult\Result\weiyihuanxing_result%s_%s.xls' % (nowdate,Round)
w = WriteExcel(result_path)
w.creattable("唯一唤醒")
excel_header = ["序号", "唤醒时间","测试音频", "设备1结果", "能量值1", "signal1", "时差1", "设备2结果", "能量值2", "signal1", "时差2", "设备3结果", "能量值3",
                "signal1", "时差3", "唤醒设备个数"]

w.write_linedata(0, excel_header)
now1 = datetime.datetime.now()
# total_num = len(result0)
total_num = 200
wakeup_num = total_num
print(total_num)
total_sum0 = 0
total_sum1 = 0
total_sum2 = 0
total_sum3 = 0



device1_wakeup_num = 0
device2_wakeup_num = 0
device3_wakeup_num = 0


for i in range(Round * total_num, (Round + 1) * total_num):
# for i in range(Round * total_num, total_num):
    # time0 = result0[i].replace(',', '.')
    time0 = result0[i][0].replace(',', '.')
    num = i - Round * total_num + 1
    wakeup_file = result0[i][2]
    result_list0 = [num, time0, wakeup_file]


    def t_log(result):
        result_new = list(result)
        test_result = '未检测'
        current = ""
        signal = ""
        add_time = ""
        for j in range(len(result_new)):
            l_time1 = result_new[j][0]
            l_time2 = result_new[j][4]
            if -2 < DiffTime(time0, l_time2).total_seconds() < 5:
                current = result_new[j][1]
                signal = result_new[j][2]
                noisy = result_new[j][3]
                add_time = DiffTime(l_time1, l_time2).microseconds / 1000
                result.remove(result_new[j])  # 删除已经匹配过的参数，提升后续的速度
                break
            else:
                continue
        result_list0.append(test_result)
        result_list0.append(current)
        result_list0.append(signal)
        result_list0.append(add_time)
        # print(result)
        return result


    t_log(result1)
    t_log(result2)
    t_log(result3)
    result_sum = 0
    r_list = [result_list0[3], result_list0[7], result_list0[11]]
    for m in range(len(r_list)):
        try:
            s = int(r_list[m])
        except:
            s = 0
        result_sum += s
    result_list0.append(result_sum)
    if result_sum == 0:
        total_sum0 += 1
    elif result_sum == 1:
        total_sum1 += 1
    elif result_sum == 2:
        total_sum2 += 1
    elif result_sum == 3:
        total_sum3 += 1
    else:
        print("error")
    if result_list0[3] == '1':
        device1_wakeup_num += 1
    if result_list0[7] == '1':
        device2_wakeup_num += 1
    if result_list0[11] == '1':
        device3_wakeup_num += 1
    if result_list0[3] == '未检测' and result_list0[7] == '未检测' and result_list0[11] == '未检测':
        wakeup_num -= 1
    print(result_list0)
    w.write_linedata(num, result_list0)
now2 = datetime.datetime.now()
t_time = now2 - now1
print(t_time, device1_wakeup_num, device2_wakeup_num, device3_wakeup_num, wakeup_num)
print("设备一唤醒次数为：%s。" % device1_wakeup_num)
print("设备二唤醒次数为：%s。" % device2_wakeup_num)
print("设备三唤醒次数为：%s。" % device3_wakeup_num)

print("测试唤醒次数为：%s。" % total_num)
print("唤醒成功次数为：%s。" % wakeup_num)
print("唤醒率为：%s。" % ("%.2f%%" % (wakeup_num / total_num * 100)))
print("未唤醒次数为：%s，百分比：%s" % (total_sum0, "%.2f%%" % (total_sum0 / total_num * 100)))
print("唯一唤醒次数为：%s，百分比：%s【%s】" % (
    total_sum1, "%.2f%%" % (total_sum1 / total_num * 100), ("%.2f%%" % (total_sum1 / wakeup_num * 100))))
print("多设备唤醒次数为：%s，百分比：%s" % (total_sum2 + total_sum3, "%.2f%%" % ((total_sum2 + total_sum3) / total_num * 100)))

w.write_linedata(0, ["测试唤醒次数为", total_num, "唤醒次数为", wakeup_num, "唤醒率为", ("%.2f%%" % (wakeup_num / total_num * 100))],
                 start_col=17)
w.write_linedata(1, ["未唤醒次数为", total_sum0, "%.2f%%" % (total_sum0 / total_num * 100)], start_col=17)
w.write_linedata(2, ["唯一唤醒次数为", total_sum1, ("%.2f%%" % (total_sum1 / total_num * 100)),
                     ("%.2f%%" % (total_sum1 / wakeup_num * 100))], start_col=17)
w.write_linedata(3, ["多设备唤醒次数为", total_sum2 + total_sum3, "%.2f%%" % ((total_sum2 + total_sum3) / total_num * 100)],
                 start_col=17)
w.write_linedata(5, ["设备一唤醒次数为", device1_wakeup_num], start_col=17)
w.write_linedata(6, ["设备二唤醒次数为", device2_wakeup_num], start_col=17)
w.write_linedata(7, ["设备三唤醒次数为", device3_wakeup_num], start_col=17)

w.close()
print("==========end")
