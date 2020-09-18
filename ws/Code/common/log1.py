__author__ = 'Administrator'
import logging.handlers
import time
import os
from conf import path

class Logger:
    def __init__(self, filename=None):
        # 日志文件名
        if filename  is None:
            filename = path.log_path
        filename = filename
        now = time.strftime('%Y-%m-%d')
        self.filename = os.path.join(filename, now + "-Log.Log")
        # 创建一个handler，用于写入日志文件 (每天生成1个，保留30天的日志)

        self.logger = logging.getLogger()
        self.fh = logging.handlers.TimedRotatingFileHandler(self.filename, 'D', 1, 30, encoding="utf8")
        self.logger.setLevel(logging.DEBUG)
        self.sh = logging.StreamHandler()
        self.sh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(asctime)s] - %(pathname)s%(funcName)s [Line:%(lineno)d] - [%(levelname)s]-[thread:%(thread)s]-[process:%(process)s] - %(message)s')
        self.fh.setFormatter(formatter)
        self.sh.setFormatter(formatter)
        self.logger.addHandler(self.fh)
        self.logger.addHandler(self.sh)

    def debug(self,message,):
        self.logger.debug(message)
        self.logger.removeHandler(self.sh)
        self.logger.removeHandler(self.fh)
        self.fh.close()

    def info(self,message):
        self.logger.info(message)
        self.logger.removeHandler(self.sh)
        self.logger.removeHandler(self.fh)
        self.fh.close()

    def warning(self,message):
        self.logger.warning(message)
        self.logger.removeHandler(self.sh)
        self.logger.removeHandler(self.fh)
        self.fh.close()

    def error(self,message):
        self.logger.error(message)
        self.logger.removeHandler(self.sh)
        self.logger.removeHandler(self.fh)
        self.fh.close()

    def caiticalllog(self,message):
        self.logger.critical(message)
        self.logger.removeHandler(self.sh)
        self.logger.removeHandler(self.fh)
        self.fh.close()




