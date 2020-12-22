import serial
import time
import datetime
import winsound
import os



# 日志目录
now = time.strftime('%Y-%m-%d-%H-%M-%S')
log_filename = "E:/儿童空调/唤醒率/思必驰方言四川话儿童空调唤醒率测试结果-3米-负45度-噪声%s.log"%now

# 命令词目录
WAKEUP_DIR = "E:/儿童空调/语料/四川话/四川话唤醒词/"

# 唤醒标识：
wake_up_mark="wakeupWord"

# 循环次数
CYCLE_COUNT = 45

# 串口信息:名称,波特率
serialName="COM4"
serialbout=115200


def write_file(fp, lines, mode='a+'):
    with open(fp, mode, encoding="utf-8") as f:
        f.writelines(lines)
        f.close()


def recvWakeup(serial,logfd):
    txt = wake_up_mark
    i = 0
    # 5秒内收到数据
    new_data=""
    while i < 50:
        data = serial.read_all()
        if len(data) == 0:
            # continue
            time.sleep(0.1)
            i += 1
        elif isinstance(data,bytes):
            print(data)
            new_data = data.decode(encoding='utf-8', errors='ignore')
            print(new_data)
            log_ts_str = "[" + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S.%f') + "] " + new_data
            write_file(logfd, log_ts_str)
            break

    ret=new_data.find(txt)
    if ret != -1:
        print('wakeup success')
        return True
    else:
        print('wakeup failure')
        return False

def read_uart():
    serialFd = serial.Serial(serialName, serialbout, timeout=60)
    total=0
    sucess=0
    fail_count=0

    # 播放音频文件.
    audiofile_list=os.listdir(WAKEUP_DIR)
    for c in range(0,CYCLE_COUNT):
        for i in range(0,len(audiofile_list)):
            wav_value=audiofile_list[i]
            time.sleep(2)
            write_file(log_filename,"播放音频文件:" + wav_value+"\n")
            wakeup_path = WAKEUP_DIR+wav_value
            winsound.PlaySound(wakeup_path, winsound.SND_FILENAME)  # 播放唤醒词
            time.sleep(1)
            is_wakeup = recvWakeup(serialFd,log_filename)  # 接收是否唤醒成功
            print(is_wakeup)
            total=total+1
            if is_wakeup:
                sucess=sucess+1
            else:
                fail_count=fail_count+1

            print("总唤醒次数:",str(total))
            print("唤醒成功次数:",str(sucess))
            print("唤醒失败次数:", str(fail_count))
            ratioCmd = (sucess / total) * 100
            ratioCmd_value = "{:.2f}%".format(ratioCmd)
            print("唤醒成功率: " + str(ratioCmd_value))
            write_file(log_filename, "总唤醒次数" + str(total) + "\n")
            write_file(log_filename, "唤醒成功次数" + str(sucess) + "\n")
            write_file(log_filename, "唤醒失败次数" + str(fail_count) + "\n")
            write_file(log_filename, "唤醒成功率" + str(ratioCmd_value) + "\n")

    serialFd.close()

if  __name__ == '__main__':
    read_uart()
