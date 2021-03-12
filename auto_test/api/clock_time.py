# @Time : 2021/2/24 10:22 
# @Author : lijq36
# @File : clock_time.py 
# @Software: PyCharm
import datetime
import re

now = datetime.datetime.now()

now_hour = datetime.datetime.now().hour
houe_to_chinese = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二']
# now_hour = 0


def set_hour(now_hour):
    if 13 >= now_hour > 0:
        hour = now_hour - 1
    elif 13 < now_hour < 24:
        hour = now_hour - 13
    else:
        hour = 0  # 零点的时候设定零点的闹钟
    return hour


def set_clock(utterance):
    hour = set_hour(now_hour)
    result = re.sub("{clock_time}", houe_to_chinese[hour] + "点", utterance)
    return result


def clock_respone(hour=None):
    if hour == None: hour = set_hour(now_hour)

    def get_periodoftime(sethour):
        period_of_time = ["深夜", "凌晨", "早上", "上午", "中午", "下午", "傍晚", "晚上"]
        time_slot = [3, 6, 8, 11, 13, 17, 19, 23]
        for i in range(len(time_slot)):
            if sethour < time_slot[i]:
                return (period_of_time[i])

    date = "今天"

    if 0 < hour < now_hour < 12:
        hour = hour + 12
    elif hour <= 12 <= now_hour < 24:
        date = "明天"
        if hour == 12: hour = 0
    elif 12 < hour < now_hour < 24:
        date = "明天"

    period_of_time = get_periodoftime(hour)
    return (date + period_of_time + str(hour) + "点")


if __name__ == '__main__':
    print(set_clock("帮我定个{clock_time}的闹钟"))
    print(clock_respone())
