import configparser


class Conf:
    def __init__(self,path):
        self.path=path
        self.cf = configparser.ConfigParser()
    def get_value(self,section,option):
        self.cf.read(self.path, encoding='utf-8')
        value=self.cf.get(section,option)
        return value
    #eval 自动转换返回类型
    def get_int(self,section,option):
        value=self.cf.getint(section,option)
        return value
    def updata_value(self,section,option,value):
        self.cf.read(self.path, encoding='utf-8')
        self.cf.set(section,option,value)
        with open(self.path, 'w') as fw:  # 循环写入
            self.cf.write(fw)
# E:\AI_test\conf\ws.ini

if __name__=='__main__':
    import Project_path

    conf_path = Project_path.conf_path
    test0 = Conf(conf_path + "sn.ini").get_value("AC", "yb101")
    # Conf(conf_path + "/ws.ini").updata_value("WS", "test","E:\AI_test\\testdata\\test_audio1")
    # test = Conf(conf_path + "ws.ini").get_value("WS", "test")
    print(test0)