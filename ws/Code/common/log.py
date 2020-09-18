import logging.handlers
import os
import time

from conf import path


class Logger(logging.Logger):
    def __init__(self, filename=None):
        super(Logger, self).__init__(self)
        # 日志文件名
        if filename  is None:
            filename = path.log_path
        self.filename = filename
        now = time.strftime('%Y-%m-%d-%H')
        self.filename=os.path.join(self.filename,now+"-Log.Log")
        # 创建一个handler，用于写入日志文件 (每天生成1个，保留30天的日志)
        self.fh = logging.handlers.TimedRotatingFileHandler(self.filename, 'D', 1, 30)
        self.fh.setLevel(logging.INFO)

        # 再创建一个handler，用于输出到控制台
        sh = logging.StreamHandler()
        sh.setLevel(logging.INFO)

        # 定义handler的输出格式
        formatter = logging.Formatter('[%(asctime)s] - %(filename)s[%(funcName)s] [Line:%(lineno)d] - [%(levelname)s]-[thread:%(thread)s]-[process:%(process)s] - %(message)s')
        self.fh.setFormatter(formatter)
        sh.setFormatter(formatter)
        # 给logger添加handler
        self.addHandler(self.fh)
        self.addHandler(sh)
    def close(self):
        self.fh.close()

if __name__ == '__main__':
    pass