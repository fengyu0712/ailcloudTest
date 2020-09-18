import datetime
import re
import time
import xlsxwriter


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
    # # 根据上面需要计算日期还是日期时间，来确定需要几个数组段。下标0表示年，小标1表示月，依次类推...
    # date1 = datetime.datetime(date1[0], date1[1], date1[2], date1[3], date1[4], date1[5])
    # date2 = datetime.datetime(date2[0], date2[1], date2[2], date2[3], date2[4], date2[5])

    # 返回两个变量相差的值，就是相差时间,最后转换为分钟返回
    return (date2 - date1).total_seconds()


path1 = "E:\\log\\20200320\\multi_wake_log_032110_1"
path2 = "E:\\log\\20200320\\multi_wake_log_032110_2"
path3 = "E:\\log\\20200320\\multi_wake_log_032110_3"
path4 = "E:\\log\\demolog\\wakeup_2020-03-21-1127.log"
nowdate = time.strftime('%Y%m%d-%H')
result_path = 'E:\AITEST\TestResult\weiyihuanxing_result%s_test.xls' % nowdate

a1 = r"\[(.*)\](.*)get wakeup_flag:(.+?)"
a2 = r"\[(.+?)\] - (.*) - 第\[(.*)\]次播放：(.*)\\(.+?).wav"

with open(path1, "r", encoding='utf-8') as r1, open(path2, "r", encoding='utf-8') as r2, open(path3, "r",
                                                                                              encoding='utf-8') as r3, open(
    path4, "r", encoding='utf-8') as r4:
    log1 = r1.read()
    log2 = r2.read()
    log3 = r3.read()
    log4 = r4.read()
result1 = re.findall(a1, log1)
result2 = re.findall(a1, log2)
result3 = re.findall(a1, log3)
result0 = re.findall(a2, log4)
#
# result0 = [('2020-03-10 09:34:45,059', '[Line:32] - [INFO]-[thread:13976]-[process:6464]', '1','test', '001M26_01_40_0001'),
#            ('2020-03-10 09:34:58,734', '[Line:32] - [INFO]-[thread:13976]-[process:6464]', '2','test', '001M28_01_42_0001'),
#            ('2020-03-10 09:35:12,040', '[Line:32] - [INFO]-[thread:13976]-[process:6464]', '3','test', '001M33_08_42_0001'),
#            ('2020-03-10 09:35:26,694', '[Line:32] - [INFO]-[thread:13976]-[process:6464]', '4','test', '003M29_01_40_0001')]
# result1 = [('2020-03-10 09:34:47.779', '486', '0'), ('2020-03-10 09:35:01.822', '486', '1'),
#            ('2020-03-10 09:35:14.922', '486', '0')]
# result2 = [('2020-03-10 09:34:47.854', '486', '1'), ('2020-03-10 09:35:01.868', '486', '0'),
#            ('2020-03-10 09:35:14.953', '486', '1')]
# result3 = [('2020-03-10 09:34:47.892', '486', '0'), ('2020-03-10 09:35:01.953', '486', '1'),
#            ('2020-03-10 09:35:15.016', '486', '0')]

w = WriteExcel(result_path)
w.creattable("唯一唤醒")
now1 = datetime.datetime.now()
total_num = len(result0)
# total_num = 100
wakeup_num = total_num
print(total_num)
total_sum0 = 0
total_sum1 = 0
total_sum2 = 0
total_sum3 = 0

device1_wakeup_num = 0
device2_wakeup_num = 0
device3_wakeup_num = 0

for i in range(0, total_num):
    time0 = result0[i][0].replace(',', '.')
    num = result0[i][2]
    wakeup_file = result0[i][4]
    result_list0 = [num, time0, wakeup_file]


    def t_log(result):
        # print(result)
        result_new = list(result)
        test_result = '未检测'
        for j in range(len(result_new)):
            time1 = result_new[j][0]
            if 0 < DiffTime(time0, time1) < 5:
                test_result = result_new[j][2]
                result.remove(result_new[j])  # 删除已经匹配过的参数，提升后续的速度
                break
            else:
                continue
        result_list0.append(test_result)
        # print(result)
        return result


    t_log(result1)
    t_log(result2)
    t_log(result3)
    result_sum = 0
    for m in range(3, len(result_list0)):
        try:
            s = int(result_list0[m])
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
    if result_list0[4] == '1':
        device2_wakeup_num += 1
    if result_list0[5] == '1':
        device3_wakeup_num += 1
    if result_list0[3:6] == ['未检测', '未检测', '未检测']:
        wakeup_num -= 1
    print(result_list0)
    w.write_linedata(i, result_list0)
now2 = datetime.datetime.now()
t_time = now2 - now1
print(t_time, device1_wakeup_num, device2_wakeup_num, device3_wakeup_num, wakeup_num)
print("设备一唤醒次数为：%s。" % device1_wakeup_num)
print("设备二唤醒次数为：%s。" % device2_wakeup_num)
print("设备三唤醒次数为：%s。" % device3_wakeup_num)

print("测试唤醒次数为：%s。" % total_num)
print("唤醒成功次数为：%s。" % wakeup_num)

print("未唤醒次数为：%s，百分比：%s" % (total_sum0, "%.2f%%" % (total_sum0 / total_num * 100)))
print("唯一唤醒次数为：%s，百分比：%s【%s】" % (
    total_sum1, "%.2f%%" % (total_sum1 / total_num * 100), ("%.2f%%" % (total_sum1 / wakeup_num * 100))))
print("多设备唤醒次数为：%s，百分比：%s" % (total_sum2 + total_sum3, "%.2f%%" % ((total_sum2 + total_sum3) / total_num * 100)))

w.write_linedata(0, ["测试唤醒次数为", total_num, "测试唤醒次数为", wakeup_num], start_col=9)
w.write_linedata(1, ["未唤醒次数为", total_sum0, "%.2f%%" % (total_sum0 / total_num * 100)], start_col=9)
w.write_linedata(2, ["唯一唤醒次数为", total_sum1, ("%.2f%%" % (total_sum1 / total_num * 100)),
                     ("%.2f%%" % (total_sum1 / wakeup_num * 100))], start_col=9)
w.write_linedata(3, ["多设备唤醒次数为", total_sum2 + total_sum3, "%.2f%%" % ((total_sum2 + total_sum3) / total_num * 100)],
                 start_col=9)
w.write_linedata(5, ["设备一唤醒次数为", device1_wakeup_num], start_col=9)
w.write_linedata(6, ["设备二唤醒次数为", device2_wakeup_num], start_col=9)
w.write_linedata(7, ["设备三唤醒次数为", device3_wakeup_num], start_col=9)

w.close()
print("==========end")
