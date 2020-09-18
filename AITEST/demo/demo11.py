import winsound, time, os
import logging.handlers
import os
import time

projectfail = os.path.split(os.path.realpath(__file__))[0]
now = time.strftime('%Y%m%d')

class Logger(logging.Logger):
    def __init__(self, filename=None, level=None):
        super(Logger, self).__init__(self)
        # 日志文件名
        if filename is None:
            filename = projectfail
        self.filename = filename
        logpath="E:\\log"
        self.filename = os.path.join(logpath, "libmulti_wake" +now+ ".log")
        # 创建一个handler，用于写入日志文件 (每天生成1个，保留30天的日志)
        self.fh = logging.handlers.TimedRotatingFileHandler(self.filename, 'D', 1, 30, encoding='utf-8')
        # self.fh = logging.FileHandler(self.filename)
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


def file_all_path(path, file_type=None, find_str=None):
    if find_str == None:
        find_str = ""
    files_list = []
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                if file_type == None:
                    if find_str in file:
                        files_list.append(os.path.join(root, file))
                else:
                    if file.split('.')[-1] == file_type and find_str in file:
                        files_list.append(os.path.join(root, file))
    elif os.path.isfile(path):
        if path.split('.')[-1] == file_type and find_str in path:
            files_list.append(path)
    else:
        print("无法解析目录：【%s】" % path)
    return files_list


wekup_wav_fail = "E:\唤醒小美音频"
stop="E:\需求\唯一唤醒\现在几点.wav"
test_list = file_all_path(wekup_wav_fail, file_type='wav')

n = 1
while True:
    for each in test_list:
        Logger().info("第[%s]播放：%s" % (n, each))
        winsound.PlaySound(each, winsound.SND_FILENAME)
        time.sleep(1)
        # winsound.PlaySound(stop, winsound.SND_FILENAME)
        # time.sleep(8)
        n += 1






