import winsound, time, os
import logging.handlers
import os
import time, random

projectfail = os.path.split(os.path.realpath(__file__))[0]


class Logger(logging.Logger):
    def __init__(self, filename=None, level=None):
        super(Logger, self).__init__(self)
        # 日志文件名
        if filename is None:
            filename = projectfail
        self.filename = filename
        now = time.strftime('%Y-%m-%d')
        self.filename = os.path.join(self.filename, now + "-Log.log")
        # 创建一个handler，用于写入日志文件 (每天生成1个，保留30天的日志)
        self.fh = logging.handlers.TimedRotatingFileHandler(self.filename, 'D', 1, 30, encoding='utf-8')
        self.fh.setLevel(logging.DEBUG)
        # 再创建一个handler，用于输出到控制台
        sh = logging.StreamHandler()
        # 设置日志等级
        if level is None or level.upper() == "INFO":
            sh.setLevel(logging.INFO)
        elif level.upper() == "DEBUG":
            sh.setLevel(logging.DEBUG)
        elif level.upper() == "WARNING":
            sh.setLevel(logging.WARNING)
        elif level.upper() == "ERROR":
            sh.setLevel(logging.ERROR)
        else:
            sh.setLevel(logging.INFO)

        # 定义handler的输出格式
        formatter = logging.Formatter(
            '[%(asctime)s] - %(filename)s [Line:%(lineno)d] - [%(levelname)s]-[thread:%(thread)s]-[process:%(process)s] - %(message)s')
        self.fh.setFormatter(formatter)
        sh.setFormatter(formatter)
        # 给logger添加handler
        self.addHandler(self.fh)
        self.addHandler(sh)

    def close(self):
        self.fh.close()


def file_all_path(path, file_type=None, filter_str=None):
    if filter_str == None:
        filter_str = ""
    files_list = []
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                if file_type == None:
                    if filter_str in file:
                        files_list.append(os.path.join(root, file))
                else:
                    if file.split('.')[-1] == file_type and filter_str in file:
                        files_list.append(os.path.join(root, file))
    elif os.path.isfile(path):
        if path.split('.')[-1] == file_type and filter_str in path:
            files_list.append(path)
    else:
        print("无法解析目录：【%s】" % path)
    return files_list


wekup_wav_fail = "E:\唤醒小美音频"
wekup_list = file_all_path(wekup_wav_fail, file_type='wav')
test_list = random.sample(wekup_list, 20)
num = 10
Logger().info("本次测试随机选择[%s]个唤醒音频，接下来每个唤醒词循环播放[%s]次" % (len(test_list), num))
for i in range(len(test_list)):
    Logger().info("【第%s个音频】--%s" % (i + 1, test_list[i]))
    n = num
    while n > 0:
        Logger().info(num - n + 1)
        winsound.PlaySound(test_list[i], winsound.SND_FILENAME)
        time.sleep(10)
        n -= 1
