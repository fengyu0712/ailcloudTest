__author__ = 'Administrator'
import logging.handlers
import time
import os
import Project_path

class Logger:
    def __init__(self, filename=None,level=None):
        # 日志文件名
        if filename is None:
            filename = Project_path.Log_path
        filename = filename
        now = time.strftime('%Y-%m-%d')
        self.filename = os.path.join(filename, now + ".log")
        # 创建一个handler，用于写入日志文件 (每天生成1个，保留30天的日志)
        self.logger = logging.getLogger()
        self.fh = logging.handlers.TimedRotatingFileHandler(self.filename, 'D', 1, 30, encoding="utf8")
        self.sh = logging.StreamHandler()
        self.fh.setLevel(logging.DEBUG)
        if level is None or level.upper()=="INFO":
            self.sh.setLevel(logging.INFO)
        elif level.upper()=="DEBUG":
            self.sh.setLevel(logging.DEBUG)
        elif level.upper() == "WARNING":
            self.sh.setLevel(logging.WARNING)
        elif level.upper() == "ERROR":
            self.sh.setLevel(logging.ERROR)
        else:
            self.sh.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(asctime)s] - %(pathname)s [Line:%(lineno)d] - [%(levelname)s]-[thread:%(thread)s]-[process:%(process)s] - %(message)s')
        self.fh.setFormatter(formatter)
        self.sh.setFormatter(formatter)
        self.logger.addHandler(self.fh)
        self.logger.addHandler(self.sh)

    def debug(self,message,):
        self.logger.debug(message)
        self.logger.removeHandler(self.sh)
        self.logger.removeHandler(self.fh)
        # self.fh.close()

    def info(self,message):
        self.logger.info(message)
        self.logger.removeHandler(self.sh)
        self.logger.removeHandler(self.fh)
        # self.fh.close()

    def warn(self,message):
        self.logger.warning(message)
        self.logger.removeHandler(self.sh)
        self.logger.removeHandler(self.fh)
        # self.fh.close()

    def error(self,message):
        self.logger.error(message)
        self.logger.removeHandler(self.sh)
        self.logger.removeHandler(self.fh)
        # self.fh.close()

    def caiticalllog(self,message):
        self.logger.critical(message)
        self.logger.removeHandler(self.sh)
        self.logger.removeHandler(self.fh)
        # self.fh.close()
    def close(self):
        self.fh.close()



