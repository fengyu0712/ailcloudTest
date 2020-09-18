# -*-coding:utf-8 -*-
import threading
# 多线程执行多个唤醒-稳定性测试
import serial
import time
import datetime
import winsound
import os
import openpyxl
import xlsxwriter

# 日志目录
LOG_OUTPUT_DIRECTORY="D:/log2/"

# pull的音频目录
pull_output_dir="D:/pulldir/"

# 命令词目录
#WAKEUP_DIR="E:/唯一唤醒/7条唤醒音频/"
#WAKEUP_DIR="E:/7686/普通话/"
WAKEUP_DIR="D:/audio_file/唤醒词/青年/"

#exeute_time=604800  # 执行时间  7天
exeute_time=120



class WAKEUP():
    def __init__(self,recordpath,serial_port,wakeup_word_value,log_path,comname,deviceid):
        self.total = 0  # 唤醒次数
        self.sucess = 0  # 成功次数
        self.fail_count = 0  # 连续三次唤醒失败的次数
        self.five_fail_count = 0  # 连续五次唤醒失败的次数
        self.seven_fail_count = 0  # 连续7次唤醒失败的次数
        self.lianxu_fail = 0  # 连续三次唤醒失败
        self.everyfail_count = 0  # 每次唤醒失败的次数
        self.result_path=recordpath   # 记录保存路径信息
        self.create_txt_head()  # 创建头部信息
        self.s_port=serial_port  # 串口信息
        self.wakemark=wakeup_word_value   # 唤醒词标志
        self.logpath=log_path  # 日志路径
        self.comvalue=comname  # 自定义的打印名称
        self.current_deviceid=deviceid  # 设备的id

    def create_txt_head(self):
        linlist=["总唤醒次数:0","唤醒成功次数:0","唤醒失败次数:0","连续三次唤醒失败次数:0","连续五次唤醒失败次数:0","连续七次以上唤醒失败次数:0","成功率:0","序号 播放音频时间 wav 唤醒是否成功"]
        for i in linlist:
            self.write_file(self.result_path,i+"\n")

    # 写入日志信息
    def write_file(self,fp, lines, mode='a+'):
        with open(fp, mode,encoding="utf-8") as f:
            f.writelines(lines)
            f.close()

    def read_fileinfo(self):
        alllines=[]
        with open(self.result_path, encoding="utf-8") as fr:
            for line in fr.readlines()[7:]:
                alllines.append(line)
        return alllines

    # 唤醒小美,获取唤醒
    def recvWakeup(self,serial, logfd):
        try:
            i = 0
            # 3秒内收到数据
            iswakeup = False
            while i < 30:
                data = serial.read_all()
                if len(data) == 0:
                    time.sleep(0.1)
                    i += 1
                elif isinstance(data, bytes):
                    new_data = data.decode(encoding='utf-8', errors='ignore')
                    log_ts_str = "[" + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S.%f') + "] " + new_data
                    self.write_file(logfd, log_ts_str)
                    if new_data.find(self.wakemark) != -1:
                        iswakeup = True
                        break

            return iswakeup
        except Exception as e:
            print("异常信息如下: " + str(e))
            return False

    def pull_dir(self,wavname):
        push_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        dirvalue =pull_output_dir +self.comvalue +"/" + wavname + push_time + "/"
        if not os.path.exists(dirvalue):
            os.makedirs(dirvalue)
        os.system("adb -s %s pull /mnt/UDISK/rec/ %s" % (self.current_deviceid,dirvalue))


    def run(self,palyaudiotime,wav_value):
        self.total=self.total+1
        iswake=self.recvWakeup(self.s_port,self.logpath)   # 是否唤醒成功
        if iswake:
            if self.lianxu_fail >= 3 and self.lianxu_fail < 5:
                self.fail_count = self.fail_count + 1
                #self.pull_dir(wav_value)
            elif self.lianxu_fail >= 5 and self.lianxu_fail < 7:
                self.five_fail_count = self.five_fail_count + 1
                #self.pull_dir(wav_value)
            elif self.lianxu_fail >= 7:
                self.seven_fail_count = self.seven_fail_count + 1
                #self.pull_dir(wav_value)

            self.sucess = self.sucess + 1
            self.lianxu_fail = 0
        else:
            self.everyfail_count = self.everyfail_count + 1
            self.lianxu_fail = self.lianxu_fail + 1


        print("%s总唤醒次数:%s"%(self.comvalue,str(self.total)))
        print("%s唤醒成功次数:%s"%(self.comvalue,str(self.sucess)))
        print("%s唤醒失败次数:%s"%(self.comvalue,str(self.everyfail_count)))
        print("%s连续三次唤醒失败次数:%s"%(self.comvalue, str(self.fail_count)))
        print("%s连续五次唤醒失败次数:%s"%(self.comvalue,str(self.five_fail_count)))
        print("%s连续七次以上唤醒失败次数:%s"%(self.comvalue,str(self.seven_fail_count)))
        ratioCmd = (self.sucess / self.total) * 100
        ratioCmd_value = "{:.2f}%".format(ratioCmd)
        print("%s唤醒成功率: %s" %(self.comvalue,ratioCmd_value))
        print("****************************************************")
        allline_info=self.read_fileinfo() # 读取文件获取原有的信息
        rowinfo = "%s %s %s %s \n" % (self.total, palyaudiotime, wav_value, iswake)
        allline_info.append(rowinfo)  # 添加新增加的信息
        first_headinfo=[]  # 头部信息
        first_headinfo.append("总唤醒次数:%s \n"%(str(self.total)))
        first_headinfo.append("唤醒成功次数:%s \n" % (str(self.sucess)))
        first_headinfo.append("唤醒失败次数:%s \n" % (str(self.everyfail_count)))
        first_headinfo.append("连续三次唤醒失败次数:%s \n" % (str(self.fail_count)))
        first_headinfo.append("连续五次唤醒失败次数:%s \n" % (str(self.five_fail_count)))
        first_headinfo.append("连续七次以上唤醒失败次数:%s \n" % (str(self.seven_fail_count)))
        first_headinfo.append("唤醒成功率:%s \n" % ratioCmd_value)
        self.write_file(self.result_path, first_headinfo,"w+")  # 写入头部信息
        self.write_file(self.result_path,allline_info)  # 写入行信息



def initcominfo(serialFD,wakeup_word,define_printname,deviceid):
    # com3的结果信息和日志信息
    nowtimeinfo = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    result_path = LOG_OUTPUT_DIRECTORY + define_printname+"唤醒率%s.txt" % nowtimeinfo
    log_filename = LOG_OUTPUT_DIRECTORY + define_printname + nowtimeinfo + '.log'
    # 初始化对象
    wakeobj=WAKEUP(result_path,serialFD,wakeup_word,log_filename,define_printname,deviceid)
    return wakeobj


def read_uart():
    serialFd = serial.Serial('COM5', 921600, timeout=60)
    com3_obj=initcominfo(serialFd,"\"ev\":	\"wake up\"","语音贴1.0_COM5","3153074508")

    serialFd1 = serial.Serial('COM11', 1500000, timeout=60)
    com5obj = initcominfo(serialFd1, "\"ev\":	\"wake up\"", "语音贴2.0_", "3153074508")

    # 播放音频文件.
    audiofile_list=os.listdir(WAKEUP_DIR)
    start_time=datetime.datetime.now()  # 开始执行时间
    print(start_time)  # 开始执行时间
    isend=False  # 是否结束
    while True:
        if isend:
            break
        for i in range(0,len(audiofile_list)):
            endTime = datetime.datetime.now()
            reponse_time = (endTime - start_time).total_seconds()
            if reponse_time >= exeute_time:
                print( "共执行时间：" + str(reponse_time))
                print("结束时间："+str(endTime))
                isend = True
                break

            wav_value=audiofile_list[i]
            now_time=datetime.datetime.now()   # 播放音频的时间
            wakeup_path=WAKEUP_DIR+wav_value  # 音频文件路径
            winsound.PlaySound(wakeup_path, winsound.SND_FILENAME)  # 播放唤醒词
            # 对象列表库
            thread_obj = []
            thread_obj.append(com3_obj.run)
            thread_obj.append(com5obj.run)

            thread_list=[]
            for t_obj in thread_obj:
                t1 = threading.Thread(target=t_obj, args=(now_time, wav_value))
                thread_list.append(t1)

            for t in thread_list:
                t.start()
                time.sleep(0.5)

            for t in thread_list:
                t.join()

    serialFd.close()
    serialFd1.close()

if  __name__ == '__main__':
    read_uart()
