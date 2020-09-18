import threading, time, redis,os
from redis import StrictRedis
import socket

class RedisLock(object):
    def __init__(self, redis_conn):
        self.redis_conn = redis_conn
        self.ip = socket.gethostbyname(socket.gethostname())
        self.pid = os.getpid()

    def get_lock_key(self, key):
        lock_key = 'lock_%s' % key
        return lock_key

    def gen_unique_value(self):
        thread_name = threading.current_thread().name
        time_now = time.time()
        unique_value = "{0}-{1}-{2}-{3}".format(self.ip, self.pid, thread_name, time_now)
        return unique_value

    def get_lock(self, key, timeout=1):
        lock_key = self.get_lock_key(key)
        unique_value = self.gen_unique_value()
        print("unique value %s" % unique_value)
        while True:
            value = self.redis_conn.set(lock_key, 1, nx=True, ex=timeout)
            if value:
                return unique_value
            else:
                thread_name = threading.current_thread().name
                print("{} is waiting..".format(thread_name))
            time.sleep(0.1)

    def del_lock(self, key, value):
        lock_key = self.get_lock_key(key)
        old_lock_value = self.redis_conn.get(lock_key)
        if old_lock_value == value:
            return self.redis_conn.delete(lock_key)



def increase_data(redis_conn, lock, key,value):
    lock_value = lock.get_lock(key) #获取锁
    value0 = redis_conn.get(key) #获取数据
    time.sleep(2.5) #模拟实际情况下进行的某些耗时操作, 且执行时间大于锁过期的时间
    if value:
        value = int(value) + 1
    else:
        value = 0
    redis_conn.set(key, value)
    thread_name = threading.current_thread().name
    print(thread_name, value)
    if thread_name == "Thread-2":
        print("thread-2 crash ....")
        import sys
        sys.exit(1)
    lock.del_lock(key, lock_value) #释放锁



redis_conn= redis.Redis(host='111.231.233.115', port=6379, password="071211", db=1)
lock=RedisLock(redis_conn)
a=10
# while a>0:
#     a=a-redis_case
#     increase_data(redis_conn,lock,"myKey%s"%a)
m=redis_conn.get('myKey2')
print(m)