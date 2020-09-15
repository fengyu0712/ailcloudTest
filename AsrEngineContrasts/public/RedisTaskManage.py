import uuid

import redis, json


class Server(object):
    def __init__(self, host='127.0.0.1', port=6379, db=0):
        self.pool = redis.ConnectionPool(host=host, port=port, db=db)
        self.__conn = redis.StrictRedis(connection_pool=self.pool)

    def get_conn(self):
        return self.__conn

    def keys(self, pattern='*'):
        return self.__conn.keys(pattern)

    def del_key(self, key):
        self.__conn.delete(key)

    def qsize(self, key):
        return self.__conn.llen(key)  # 返回队列里面list内元素的数量

    def set(self, name, value):
        if isinstance(value, dict) or isinstance(value, list):
            value = json.dumps(value)
        self.__conn.set(name, value)

    def mget(self, keys, *args):
        return self.__conn.mget(keys, args)

    def get(self, name):
        item = self.__conn.get(name)
        if item:

            return item.decode()
        else:
            return None

    def close(self):
        self.__conn.close()

    def publish(self, msg, chan=None):
        """
        在指定频道上发布消息
        :param msg:
        :return:
        """
        # publish(): 在指定频道上发布消息，返回订阅者的数量
        if isinstance(msg, dict) or isinstance(msg, list):
            msg = json.dumps(msg, ensure_ascii=False)
        self.__conn.publish(chan, msg)
        # if chan:
        #     self.__conn.publish(chan, msg)
        # else:
        #     self.__conn.publish(self.chan_sub, msg)
        return True

    def sub(self, chan=None):
        # 返回发布订阅对象，通过这个对象你能1）订阅频道 2）监听频道中的消息
        pub = self.__conn.pubsub()
        # 订阅某个频道，与publish()中指定的频道一样。消息会发布到这个频道中
        pub.subscribe(chan)
        # if chan:
        #     pub.subscribe(chan)
        # else:
        #     pub.subscribe(self.chan_sub)
        pub.parse_response()
        return pub

    def que_put_message(self, key, message):
        # chan=self.chan
        if isinstance(message, list) or isinstance(message, dict):
            self.__conn.rpush(key, json.dumps(message))  # 添加新元素到队列最右方
        else:
            self.__conn.rpush(key, message)

    def que_left_put_message(self, key, message):
        # chan=self.chan
        if isinstance(message, list) or isinstance(message, dict):
            self.__conn.lpush(key, json.dumps(message))  # 添加新元素到队列最zuo方
        else:
            self.__conn.lpush(key, message)

    def get_nowait(self, chan):
        # 直接返回队列第一个元素，如果队列为空返回的是None
        item = self.__conn.lpop(chan)
        if item:
            return item.decode(encoding='utf-8')
        else:
            return None

    def get_dict_wait(self, chan, timeout=None):
        try:
            task, item = self.__conn.blpop(chan, timeout=timeout)
            item = bytes.decode(item, encoding='utf-8')
        except TypeError:
            pass
            # print('TypeError')
        else:
            # if item:
            #     data = json.loads(item)
            return item

    def get_dict_nowait(self, chan):
        # 直接返回队列第一个元素，如果队列为空返回的是None
        try:
            item = self.__conn.lpop(chan)
            item = bytes.decode(item, encoding='utf-8')
        except TypeError:
            pass
            # print('TypeError')
        else:
            # print(item)
            if item:
                data = json.loads(item)
                return data


class BaseRedis():
    def __init__(self, redis, type, *args, **kwargs):
        self.chan = 'RedisNluTask'
        self.type = type
        self.redis = redis

    def redis_set_data(self, uid, data):
        return self.redis.set('task:{}:job:{}:data'.format(self.type, uid), data)

    def redis_set_status(self, uid, status):
        return self.redis.set('task:{}:job:{}:status'.format(self.type, uid), status)

    def redis_get_data(self, uid):
        return self.redis.get('task:{}:job:{}:data'.format(self.type, uid))

    def redis_get_status(self, uid):
        return self.redis.get('task:{}:job:{}:status'.format(self.type, uid))

    def redis_set_percent(self, uid, data):
        return self.redis.set('task:{}:job:{}:percent'.format(self.type, uid), data)

    def redis_get_percent(self, uid):
        return self.redis.get('task:{}:job:{}:percent'.format(self.type, uid))

    def redis_put_case(self, uid, data):
        key = 'task:{}:job:{}:case'.format(self.type, uid)
        self.redis.que_put_message(key, data)

    def redis_put_result(self, uid, data):
        key = 'task:{}:job:{}:result'.format(self.type, uid)
        self.redis.que_put_message(key, data)

    def redis_get_case(self, uid, timeout=10):
        key = 'task:{}:job:{}:case'.format(self.type, uid)
        return self.redis.get_dict_wait(key, timeout)

    def redis_get_case_size(self, uid):
        key = 'task:{}:job:{}:case'.format(self.type, uid)
        return self.redis.qsize(key)

    def redis_get_result(self, uid, timeout=None):
        key = 'task:{}:job:{}:result'.format(self.type, uid)
        return self.redis.get_dict_wait(key, timeout)

    def redis_get_result_size(self, uid):
        key = 'task:{}:job:{}:result'.format(self.type, uid)
        return self.redis.qsize(key)

    def redis_publish(self, data):
        uid = str(uuid.uuid1())
        self.redis.publish({'id': uid, 'data': data, 'type': self.type}, self.chan)
        return uid

    def redis_resume_publish(self, data):
        uid = data.get('CeleryId')
        self.task_del_case_result(uid)
        self.redis.publish({'id': uid, 'data': data, 'type': self.type}, self.chan)

        return uid

    def redis_subscribe(self):
        return self.redis.sub(self.chan)

    def redis_listen(self, callback=None):
        sub = self.redis_subscribe()
        while True:
            msg = sub.listen()
            for i in msg:
                if i["type"] == "message":
                    data = i.get('data')
                    # data = json.loads(i["data"].decode())
                    if callback:
                        callback(data)
                    else:
                        print(data)

                elif i["type"] == "subscrube":
                    print(str(i["chennel"], encoding="utf-8"))

    def redis_stop(self, uid):
        key = 'task:{}:job:{}:case'.format(self.type, uid)
        self.redis.del_key(key)
        for i in range(100):
            self.redis.que_put_message(key, 'over')

    def task_stop(self, uid):
        self.redis_stop(uid)
        self.redis_set_status(uid, 'stop')

    def task_del_case_result(self, uid):
        key = 'task:{}:job:{}:case'.format(self.type, uid)
        self.redis.del_key(key)
        key = 'task:{}:job:{}:result'.format(self.type, uid)
        self.redis.del_key(key)

    def task_over(self, uid):
        self.redis_set_status(uid, 'over')
        self.task_del_case_result(uid)

    def task_running(self, uid):
        # self.redis_stop(uid)
        self.redis_set_status(uid, 'runing')

    def task_list(self, value: str):
        key = 'task:{}:job:*:status'.format(self.type)
        print(self.redis.keys())
        data = self.redis.keys(key)
        task = []
        for i in data:
            d = self.redis.get(i)
            if d == value:
                id = i.decode().split(':')[3]
                task.append(id)
        return task

    def task_runing_list(self):
        return self.task_list('running')


class Manager(Server):
    def __init__(self, *args, **kwargs):
        super(Manager, self).__init__(*args, **kwargs)
        self.chan = 'RedisNluTask'

    @property
    def nlu(self):
        return BaseRedis(self, 'nlu')

    # @property
    def asr(self):
        return BaseRedis(self, 'asr')

    # def redis_set_data(self, uid, data):
    #     return self.set('task:{}:job:{}:data'.format(self.type, uid), data)
    #
    # def redis_set_status(self, uid, status):
    #     return self.set('task:{}:job:{}:status'.format(self.type, uid), status)
    #
    # def redis_get_data(self, uid):
    #     return self.get('task:{}:job:{}:data'.format(self.type, uid))
    #
    # def redis_get_status(self, uid):
    #     return self.get('task:{}:job:{}:status'.format(self.type, uid))
    #
    # def redis_set_percent(self, uid, data):
    #     return self.set('task:{}:job:{}:percent'.format(self.type, uid), data)
    #
    # def redis_get_percent(self, uid):
    #     return self.get('task:{}:job:{}:percent'.format(self.type, uid))
    #
    # def redis_put_case(self, uid, data):
    #     key = 'task:{}:job:{}:case'.format(self.type, uid)
    #     self.que_put_message(key, data)
    #
    # def redis_put_result(self, uid, data):
    #     key = 'task:{}:job:{}:result'.format(self.type, uid)
    #     self.que_put_message(key, data)
    #
    # def redis_get_case(self, uid, timeout=10):
    #     key = 'task:{}:job:{}:case'.format(self.type, uid)
    #     return self.get_dict_wait(key, timeout)
    #
    # def redis_get_case_size(self, uid):
    #     key = 'task:{}:job:{}:case'.format(self.type, uid)
    #     return self.qsize(key)
    #
    # def redis_get_result(self, uid, timeout=None):
    #     key = 'task:{}:job:{}:result'.format(self.type, uid)
    #     return self.get_dict_wait(key, timeout)
    #
    # def redis_get_result_size(self, uid):
    #     key = 'task:{}:job:{}:result'.format(self.type, uid)
    #     return self.qsize(key)
    #
    # def redis_publish(self, data, type):
    #     uid = str(uuid.uuid1())
    #     self.publish({'id': uid, 'data': data, 'type': type}, self.chan)
    #     return uid

    def redis_subscribe(self):
        return self.sub(self.chan)

    def redis_listen(self, callback=None):
        sub = self.redis_subscribe()
        while True:
            msg = sub.listen()
            for i in msg:
                if i["type"] == "message":
                    data = i.get('data')
                    # data = json.loads(i["data"].decode())
                    if callback:
                        callback(data)
                    else:
                        print(data)

                elif i["type"] == "subscrube":
                    print(str(i["chennel"], encoding="utf-8"))

    # def redis_stop(self, uid):
    #     key = 'task:{}:job:{}:case'.format(self.type, uid)
    #     self.del_key(key)
    #     for i in range(100):
    #         self.que_put_message(key, 'over')


def hello(data):
    print('hello', data)


if __name__ == "__main__":
    a = Manager('127.0.0.1', 6379)
    b = a.nlu.task_runing_list()

    # print(a.keys())
    # a.redis_set_data('123456', 1243)
    # a.redis_put_case('123456', {'adb': 123456})

    # sub=a.redis_subscribe()
    # while True:
    #     # msg=sub.parse_response()
    #     msg=sub.get_message()
    #     print(msg)
    # a.redis_publish({'123': 123})
    # a.redis_listen(hello)
