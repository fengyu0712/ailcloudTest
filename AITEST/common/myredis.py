import redis,Project_path
from common.conf import Conf
conf_path = Project_path.conf_path + "db.ini"

class myRedis():
    def __init__(self,redis_db=None):
        if redis_db==None:
            redis_db=0
        conf_path = Project_path.conf_path + "db.ini"
        host = Conf(conf_path).get_value("Redis", "host")
        port= Conf(conf_path).get_value("Redis", "port")
        password = Conf(conf_path).get_value("Redis", "password")
        self.r = redis.Redis(host=host,port=port,db=redis_db,password=password,decode_responses=True)

    def push_list(self,list_data,key_name=None):
        list_data = list(list_data)
        if key_name==None:
            key_name=list_data[0]
        for i in range(len(list_data)):
            self.r.rpush(key_name, list_data[i])

    def push_onlydata(self,key_name,data):
        self.r.rpush(key_name, data)

    def set_str(self,str_data):
        self.r.get(str_data)

    def get_keys(self):
        keys=self.r.keys()
        return keys

    def read_list(self,key_name):
        list_data=self.r.lrange(key_name,0,-1)
        return list_data

    def delete(self,key):
        self.r.delete(key)

    def clear(self):
        list_keys=self.get_keys()
        for key in list_keys:
            self.delete(key)

if __name__ == '__main__':
    r=myRedis(redis_db=1)
    r.push_list(["1111",2,"测试"])

    k=r.get_keys()
    for each in k:
        m=r.read_list(each)
        print(m)


# r = redis.Redis(host='127.0.0.redis_case', port=6379,db=0, password='')
# b=r.keys()
# print(b)
# r.rpop("*")
# r.rpush("2","用例",2,3,4)
# a=r.lrange("0" , 0 , -redis_case)
# # print(a)
# for i in range(len(a)):
#     a[i] =a[i].decode('utf8')
# print(a)