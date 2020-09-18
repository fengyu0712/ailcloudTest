import time,re
import datetime

class Appointment:
    def __init__(self):
        self.now_time=datetime.datetime.now()
        self.now_date=self.now_time.date()
        self.now_hour=self.now_time.hour

    def run_nlu(self,nlu):

        today = datetime.date.today()  # 获得今天的日期
        a = re.compile("{'parameter': 'date', 'value': '(.*)'}, {'parameter': 'deviceMode',")
        b = "{'parameter': 'date', 'value': '%s'}, {'parameter': 'deviceMode',"
        if "明天" in nlu:
            data = today + datetime.timedelta(days=1)
            try:
                nlu = re.sub(a, b % data.isoformat(), nlu)  # 正则替换日期，匹配不到就返回原NLU
            except:
                nlu = nlu
        elif "今天" in nlu:
            data = today
            try:
                nlu = re.sub(a, b % data.isoformat(), nlu)
            except:
                nlu = nlu
        elif "昨天" in nlu:  # 定时应该不会有时间
            data = today - datetime.timedelta(days=1)
            try:
                nlu = re.sub(a, b % data.isoformat(), nlu)
            except:
                nlu = nlu
        else:
            nlu = nlu
        return nlu

    #时区定位
    def DateP(self,hour):
        if 6 > hour >= 0:
            P = "凌晨"
        elif 12 > hour >= 6:
            P = "上午"
        elif hour == 12:
            P = "中午"
        elif 18 > hour > 12:
            P = "下午"
        elif 24 > hour >= 18:
            P = "晚上"
        else:
            P = "时间错误"
        return P

    def DiffTime(self,date1, date2):
        # %Y-%m-%d为日期格式，其中的-可以用其他代替或者不写，但是要统一，同理后面的时分秒也一样；可以只计算日期，不计算时间。
        date1 = datetime.datetime.strptime(date1, "%Y-%m-%d %H:%M:%S")
        date2 = datetime.datetime.strptime(date2, "%Y-%m-%d %H:%M:%S")
        # 根据上面需要计算日期还是日期时间，来确定需要几个数组段。下标0表示年，小标1表示月，依次类推...
        # date1 = datetime.datetime(date1[0], date1[1], date1[2], date1[3], date1[4], date1[5])
        # date2 = datetime.datetime(date2[0], date2[1], date2[2], date2[3], date2[4], date2[5])

        # 返回两个变量相差的值，就是相差时间,最后转换为分钟返回
        return (date2 - date1).total_seconds()/60

    def CalDate(self):
        if  '明天' in self.tts:
            date_str="明天"
            self.test_date=self.now_date+datetime.timedelta(days=1)
            if "下午" in self.tts or "晚上" in self.tts and self.test_hour<12:
                self.test_hour = self.test_hour+12

        elif '今天' in self.tts:
            date_str = "今天"
            if "下午" in self.tts or "晚上" in self.tts and self.test_hour<12:
                self.test_hour = self.test_hour+12
        else:
            date_str = ""
            if self.now_hour < 12:
                if self.test_hour < self.now_hour:
                    self.test_hour = self.test_hour + 12
            else:
                if "早上" in self.tts or "上午" in self.tts or "凌晨" in self.tts:
                    self.test_date = self.now_date + datetime.timedelta(days=1)
                    date_str = "明天"
                elif  "下午" in self.tts or "晚上" in self.tts :
                    if self.test_hour<self.now_hour-12:
                        self.test_date = self.now_date + datetime.timedelta(days=1)
                        date_str = "明天"
                        self.test_hour = self.test_hour + 12
                    if self.now_hour > self.test_hour > 12:
                        self.test_date = self.now_date + datetime.timedelta(days=1)
                        date_str = "明天"
                else:
                    if  12>=self.test_hour>self.now_hour-12:
                        self.test_hour = self.test_hour + 12
                    if  self.test_hour<self.now_hour-12:
                        self.test_date = self.now_date + datetime.timedelta(days=1)
                        date_str = "明天"
                    if self.now_hour>self.test_hour>12 :
                        self.test_date = self.now_date + datetime.timedelta(days=1)
                        date_str = "明天"
        return date_str
    def AppointTTS(self):
        test_time_o = re.findall("{(.*?)}", self.tts)[0]
        self.test_hour = int(re.split(':', test_time_o)[0])
        self.test_min = int(re.split(':', test_time_o)[1])
        # 默认测试日期和当前日期一致
        self.test_date = self.now_time.date()
        date_str=self.CalDate()
        dateP=self.DateP(self.test_hour)
        test_time = self.test_date.strftime('%Y-%m-%d ') + "%s:%s:00"%(str(self.test_hour),self.test_min)
        now_time=self.now_time.strftime('%Y-%m-%d %H:%M:%S')
        diff_time=self.DiffTime(now_time,test_time)
        if diff_time<72:
            tts="该模式预约时间不允许小于72分钟"
        else:
            while self.test_hour > 12:
                self.test_hour = self.test_hour-12
            a = re.compile("TTSDate.*点")
            b = "%s点"
            tts = re.sub(a, b % (date_str +dateP+ str(self.test_hour)), self.tts)  # 利用正则替换
        return tts

    def CookingTTS(self):
        value_list=re.findall(r"\d+\.?\d*", self.tts)
        addHour=int(value_list[0])
        addMin=int(value_list[1])
        test_time = self.now_time + datetime.timedelta(hours=addHour,minutes=addMin)
        test_hour = test_time.hour
        test_mins = test_time.minute
        a = re.compile("CookTime--.*完成")
        b = "%s点%s分完成"
        tts = re.sub(a, b % (str(test_hour), str(test_mins)), self.tts)  # 利用正则替换
        return tts

    def run_tts(self,TTS):
        self.tts=TTS
        if "TTSDate" in self.tts:
            tts = self.AppointTTS()
        elif "CookTime" in self.tts:
            tts=self.CookingTTS()
        else:
            tts=self.tts

        return tts



if __name__=="__main__":
    #TTS调用格式
    # 1.NLU包含明天时，自动调用
    # 2.预约TTS，包含标识TTSDATE 和{时间}
    # 3.烹饪时间TTS，包含标识设备将在CookTime和菜谱剩余时间（剩余时间为参数传入）
    m="好的，电饭煲将会在TTSDate--{8:00}点完成烹饪"
    n = "设备将在CookTime--1:50完成"
    a=Appointment().run_tts(m)
    b=Appointment().run_tts(n)
    print(a,b)
