# @Time : 2021/2/24 10:22 
# @Author : lijq36
# @File : clock_time.py 
# @Software: PyCharm
import datetime
import re

now = datetime.datetime.now()

now_hour = datetime.datetime.now().hour
houe_to_chinese = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二']
# now_hour = 1


def set_clock(utterance):
    if 13 >= now_hour > 0:
        set_hour = now_hour - 1
    elif 13 < now_hour < 24:
        set_hour = now_hour - 13
    else:
        set_hour = 0  # 零点的时候设定零点的闹钟
    result = re.sub("{clock_time}", houe_to_chinese[set_hour] + "点", utterance)
    return result


def clock_respone():
    def get_periodoftime(sethour):
        period_of_time = ["深夜", "凌晨", "早上", "上午", "中午", "下午", "傍晚", "晚上"]
        time_slot = [3, 6, 8, 11, 13, 17, 19, 23]
        for i in range(len(time_slot)):
            if sethour < time_slot[i]:
                return (period_of_time[i])

    if 12 >= now_hour >= 0:
        date = "今天"

        if now_hour == 0 or 1:
            set_hour = 0
            date = "明天"
        else:
            set_hour = now_hour + 11  # 转到PM的闹钟
        # if now_hour==13:
        #     set_hour = 12
        #     date = "明天"
        period_of_time = get_periodoftime(set_hour)
        return (date + period_of_time + str(set_hour) + "点")
    else:

        if now_hour == 13:
            set_hour = 12
        else:
            set_hour = now_hour - 13  # 进入多轮询问定几点的闹钟
        return f"是明天上午{set_hour}点还是下午{set_hour}点？"


if __name__ == '__main__':
    print(set_clock("帮我定个{clock_time}的闹钟"))
    print(clock_respone())
