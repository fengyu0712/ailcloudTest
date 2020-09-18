result = [2, 3, 4, 2, 2, 1, 2]
import datetime
import re
import time
import xlsxwriter


def DiffTime(date1, date2):
    # %Y-%m-%d为日期格式，其中的-可以用其他代替或者不写，但是要统一，同理后面的时分秒也一样；可以只计算日期，不计算时间。
    date1 = time.strptime(date1, "%Y-%m-%d %H:%M:%S.%f")
    date2 = time.strptime(date2, "%Y-%m-%d %H:%M:%S.%f")
    # 根据上面需要计算日期还是日期时间，来确定需要几个数组段。下标0表示年，小标1表示月，依次类推...
    date1 = datetime.datetime(date1[0], date1[1], date1[2], date1[3], date1[4], date1[5])
    date2 = datetime.datetime(date2[0], date2[1], date2[2], date2[3], date2[4], date2[5])

    # 返回两个变量相差的值，就是相差时间,最后转换为分钟返回
    return (date2 - date1).total_seconds()


result0 = [('2020-03-10 09:34:45,059', '[Line:32] - [INFO]-[thread:13976]-[process:6464]', '1', '001M26_01_40_0001'),
           ('2020-03-10 09:34:58,734', '[Line:32] - [INFO]-[thread:13976]-[process:6464]', '2', '001M28_01_42_0001'),
           ('2020-03-10 09:35:12,040', '[Line:32] - [INFO]-[thread:13976]-[process:6464]', '3', '001M33_08_42_0001'),
           ('2020-03-10 09:35:26,694', '[Line:32] - [INFO]-[thread:13976]-[process:6464]', '4', '003M29_01_40_0001')]
result1 = [('2020-03-10 09:34:47.779', '486', '0'), ('2020-03-10 09:35:01.822', '486', '1'),
           ('2020-03-10 09:35:14.922', '486', '0')]
result2 = [('2020-03-10 09:34:47.854', '486', '1'), ('2020-03-10 09:35:01.868', '486', '0'),
           ('2020-03-10 09:35:14.953', '486', '1')]
result3 = [('2020-03-10 09:34:47.892', '486', '0'), ('2020-03-10 09:35:01.953', '486', '1'),
           ('2020-03-10 09:35:15.016', '486', '0')]
now1 = datetime.datetime.now()
for i in range(0, len(result0)):
    time0 = result0[i][0].replace(',', '.')
    num = result0[i][2]
    wakeup_file = result0[i][3]
    result_list0 = [num, time0, wakeup_file]


    def t_log(result):
        # print(result)
        result_new = list(result)
        test_result = '未检测'
        for j in range(len(result_new)):
            # time.sleep(1)
            time1 = result_new[j][0]
            if 0 < DiffTime(time0, time1) < 10:
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
now2 = datetime.datetime.now()
t_time = now2 - now1
print(t_time)


