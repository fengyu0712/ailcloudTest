# -*-coding:utf-8 -*-
import threading
# 多线程执行多个唤醒
import serial
import time
import datetime
import winsound
import os
import re
# 日志目录
LOG_OUTPUT_DIRECTORY="D:/log/在线识别率-202012-16/"

# 命令词目录
#WAKEUP_DIR="E:/唯一唤醒/7条唤醒音频/"
#WAKEUP_DIR="E:/7686/普通话/"
WAKEUP_DIR="E:/audio/唤醒小美音频-8009唤醒词/"
file_path=r"E:\script\script\data\DF100_offline.txt"

#exeute_time=604800  # 执行时间  7天
exeute_time=259200

class WAKEUP():
    def __init__(self,recordpath,serial_port,wakeup_word_value,log_path,comname,state,lixian_hash):
        self.total = 0  # 唤醒次数
        self.sucess = 0  # 成功次数
        self.fail=0  # 失败次数
        self.result_path=recordpath   # 记录保存路径信息
        self.create_txt_head()  # 创建头部信息
        self.s_port=serial_port  # 串口信息
        self.wakemark=wakeup_word_value   # 唤醒词标志
        self.logpath=log_path  # 日志路径
        self.comvalue=comname  # 自定义的打印名称
        self.firmstate=state  # 固件状态
        self.hashtable=lixian_hash  # 离线hash映射表

    def create_txt_head(self):
        linlist=["总唤醒次数:0","唤醒成功次数:0","唤醒失败次数:0","成功率:0","序号 播放音频时间 wav 唤醒是否成功 asr 是否命中离线指令此 是否命中开关机命令"]
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
            for line in fr.readlines()[4:]:
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
    
    def is_mingzhong_offline(self,newdata):
        ismingzhong = False
        try:
            #print(newdata)
            commond = re.compile("operation\":\"(.*)\",\"domain\"")
            c = commond.findall(newdata)
            #print(c)

            if len(c) > 0:
                local_asr = str(c[0]).replace(" ", "")
                if local_asr in ['close','open']:
                    ismingzhong=True

        except Exception as e:
            print("解析异常了：", e)
        finally:
            return ismingzhong

    def run(self,palyaudiotime,wav_value):
        self.total=self.total+1
        iswake=self.recvWakeup(self.s_port,self.logpath)   # 是否唤醒成功
        #mark=""
        asrvalue=""
        ismingzhong="" # 是否命中离线指令
        isopen_commond=""  # 是否命中开关指令
        if iswake:
            self.sucess = self.sucess + 1
            # 唤醒成功后，获取信息
            # 要保存的内容
            serialinfo = self.recvCmd(self.s_port, self.logpath)
            serialinfo = serialinfo.replace("\t", "").replace("\r", "")
            
            if self.firmstate == "1":
                # 在线asr信息
                asrvalue = self.getasrvalue(serialinfo)
                print("{}在线asr信息:{}".format(self.comvalue, asrvalue))
                #mark="在线"
            else:
                asrvalue = self.get_local_asr(serialinfo)
                #mark = "离线"
                print("{}离线asr信息:{}".format(self.comvalue, asrvalue))
                if asrvalue in self.hashtable:
                    ismingzhong=True
                    isopen_commond=self.is_mingzhong_offline(serialinfo)
                    print("是否命中离线指令词",ismingzhong)
                    print("是否命中开关机指令",isopen_commond)
                else:
                    ismingzhong = False
                    
               
                
        else:
            self.fail=self.fail+1
        print("%s总唤醒次数:%s"%(self.comvalue,str(self.total)))
        print("%s唤醒成功次数:%s"%(self.comvalue,str(self.sucess)))
        print("%s唤醒失败次数:%s"%(self.comvalue,str(self.fail)))
        ratioCmd = (self.sucess / self.total) * 100
        ratioCmd_value = "{:.2f}%".format(ratioCmd)
        print("%s唤醒成功率: %s" %(self.comvalue,ratioCmd_value))
        #print("{}{}asr信息:{}".format(self.comvalue,mark ,asrvalue))
        print("****************************************************")
        allline_info=self.read_fileinfo() # 读取文件获取原有的信息
        rowinfo = "%s %s %s %s %s %s %s \n" % (self.total, palyaudiotime, wav_value, iswake,asrvalue,ismingzhong,isopen_commond)
        allline_info.append(rowinfo)  # 添加新增加的信息
        first_headinfo=[]  # 头部信息
        first_headinfo.append("总唤醒次数:%s \n"%(str(self.total)))
        first_headinfo.append("唤醒成功次数:%s \n" % (str(self.sucess)))
        first_headinfo.append("唤醒失败次数:%s \n" % (str(self.fail)))
        first_headinfo.append("唤醒成功率:%s \n" % ratioCmd_value)
        #first_headinfo.append("序号 播放音频时间 wav 唤醒是否成功 asr 是否命中开关机命令")
        self.write_file(self.result_path, first_headinfo,"w+")  # 写入头部信息
        self.write_file(self.result_path,allline_info)  # 写入行信息

    # 获取tts返回的asr信息
    def getasrvalue(self,newdata):
        asrvalue = ""
        try:
            if newdata != "":
                # commond = re.compile(".*TTS.*text\"\:\"(.*)\"\,\"endSession\".*")
                #commond = re.compile(
                #    ".*test_output\"\:\{\"ev\"\:\"online tts\"\,\"text\"\:\"(.*)\"\,\"data\"\:\d+\,\"info\".*")
                #commond=re.compile("\"asr\":\"(.*)\"")
                commond=re.compile("\"nlu\":{\n+\"endSession\":true,\n+\"asr\":\"(.*)\",\n+\"tts\"",re.DOTALL)
                c = commond.findall(newdata)
                if len(c) > 0:
                    asrvalue = str(c[0]).replace(" ", "")
        except Exception as e:
            print("解析异常了：", e)

        finally:
            return asrvalue

    # 获取离线的asr信息
    def get_local_asr(self,newdata):
        local_asr = ""
        try:
            #commond = re.compile(
            #    ".*test_output.*ev\"\:\"local asr\"\,\"text\"\:\"(.*)\"\,\"data\"\:(.*),\"info\"\:\"ifly|dui\"")
            commond=re.compile("\"rec\":\"(.*)\",\"conf\"")
            c = commond.findall(newdata)
            if len(c) > 0:
                local_asr = str(c[0]).replace(" ", "")
        except Exception as e:
            print("解析异常了：", e)
        finally:
            return local_asr

    def recvCmd(self,serial, log_filename):
        i = 0
        # 10 秒内收到回应
        cmd_data = ""
        try:
            while i < 100:
                count = serial.inWaiting()
                if count > 0:
                    time.sleep(0.1)
                    buff = serial.read_all()
                    if isinstance(buff, bytes):
                        temp_data = buff.decode(encoding='utf-8', errors='ignore')
                        self.write_file(log_filename, temp_data)
                        cmd_data = cmd_data + temp_data
                else:
                    time.sleep(0.1)
                    i += 1
        except Exception as e:
            print("获取asr结果异常：" + str(e))
            self.write_file(log_filename, "获取asr结果异常：" + str(e))
        finally:
            return cmd_data


def read_file():
    with open(file_path, 'r') as f:
       list1= f.readlines()
    for i in range(0,len(list1)):
        list1[i]=list1[i].rstrip('\n')
    #print(list1)
    return list1

def initcominfo(serialFD,wakeup_word,define_printname,devicestate,lixian_hash):
    # com3的结果信息和日志信息
    nowtimeinfo = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    result_path = LOG_OUTPUT_DIRECTORY + define_printname+"唤醒率%s.txt" % nowtimeinfo
    log_filename = LOG_OUTPUT_DIRECTORY + define_printname + nowtimeinfo + '.log'
    # 初始化对象
    
    wakeobj=WAKEUP(result_path,serialFD,wakeup_word,log_filename,define_printname,devicestate,lixian_hash)
    return wakeobj


def read_uart():
    lixian_hash=read_file()  # 读取离线命令词表
    serialFd = serial.Serial('COM4', 115200, timeout=60)
    com3_obj=initcominfo(serialFd,"wakeupWord","com4在线","1",lixian_hash)

    serialFd1 = serial.Serial('COM16', 115200, timeout=60)
    com5obj = initcominfo(serialFd1, "wakeupWord", "COM16离线", "0",lixian_hash)

    # 播放音频文件.
    audiofile_list=os.listdir(WAKEUP_DIR)
    start_time=datetime.datetime.now()  # 开始执行时间
    print(start_time)  # 开始执行时间
    isend=False  # 是否结束
    for j in range(0,4):
        for i in range(0,len(audiofile_list)):
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
