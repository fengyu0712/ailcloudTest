# coding: utf-8
# 导包
import  logging.handlers
from config import base_path
import os
import datetime

# 新建类
class GetLog(logging.Logger):

  # 新建一个日志器变量
  __logger=None

  @classmethod
  # 新建获取日志器的方法
  def get_logger(cls):
      # 判断日志器是否为空
      if cls.__logger is None:
          # 获取日志器
          cls.__logger=logging.getLogger()
          # 修改默认级别
          cls.__logger.setLevel(logging.INFO)
          nowtimeinfo = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
          log_path=base_path+os.sep+"log"+os.sep+nowtimeinfo+".log"
          # 获取处理器
          th=logging.handlers.TimedRotatingFileHandler(filename=log_path,when='midnight',interval=1,backupCount=3,encoding='utf-8')
          sh = logging.StreamHandler()
          sh.setLevel(logging.DEBUG)

          # 获取格式器
          fmt ="%(asctime)s - %(levelname)s - %(message)s"
          fm=logging.Formatter(fmt)
          sh.setFormatter(fm)
          # 将格式器添加到处理器中
          th.setFormatter(fm)
          # 将日志器添加到日志器中
          # addHandler(th)
          # self.addHandler(sh)
      # 返回日志器
      return cls.__logger

if __name__ == '__main__':
    log=GetLog.get_logger()
    log.info("测试信息级别日志")
    log.info("测试错误级别日志")

