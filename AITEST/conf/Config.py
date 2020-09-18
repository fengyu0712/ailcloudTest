import configparser
from conf.project_path import *

class ReadConfigFile():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(conf_path+"/config.ini")

    def get_env(self):
        env_value=str(self.get_value("env","run_env"))
        print("************",env_value)
        domain_value=self.get_value(env_value,"domain")
        url_value = self.get_value(env_value, "url")
        return domain_value,url_value

    def get_devicesinfo(self):
        devicesvalue= self.get_value("devices", "devicesinfo")
        uid=self.get_value("devices", "uid")
        query_replyinfo=self.get_value("devices","query_reply_info")
        return uid,devicesvalue,query_replyinfo

    def get_value(self,section_value,option_value):
        value = self.config.get(section_value, option_value)
        return value
