import json
import os
import time

from AsrEngineContrasts.Api.Orion import OrionAsr
from AsrEngineContrasts.AsrEngineDB import EngineDb
import uuid
from AsrEngineContrasts.public.RedisTaskManage import Manager
from threading import Thread


class LeiHu(object):
    def __init__(self, taskname, wav_base_path):
        self.id = uuid.uuid1()
        self.redis = Manager().asr()
        self.taskname = taskname
        self.wav_base_path = wav_base_path
        self.run_item = [10]
        self.case_num = 0

    def _resume_read_case(self):
        sql = EngineDb()
        done = sql.select_done_id(self.taskname, 'lh')
        index = 1
        while True:
            data = sql.select_case(self.run_item, pagesize=1000, pageindex=index, done_case=done)
            if not data:
                break
            index = index + 1
            for i in data:
                # print(i)
                self.redis.redis_put_case(self.id, i)
        for i in range(100):
            self.redis.redis_put_case(self.id, 'over')

    def _resume_none_read_case(self):
        sql = EngineDb()
        done = sql.select_run_none_id(self.taskname, 'lh')
        index = 1
        self.case_num = len(done)
        print('数量:', self.case_num)
        while True:
            data = sql.select_case(self.run_item, pagesize=1000, pageindex=index, run_case=done)
            print('数量2:', len(data))
            if not data:
                break
            index = index + 1
            for i in data:
                # print(i)
                self.redis.redis_put_case(self.id, i)
        for i in range(100):
            self.redis.redis_put_case(self.id, 'over')

    def _read_case(self):
        sql = EngineDb()
        index = 1
        while True:
            data = sql.select_case([10], pagesize=1000, pageindex=index)
            if not data:
                break
            index = index + 1
            for i in data:
                # print(i)
                self.redis.redis_put_case(self.id, i)
        for i in range(100):
            self.redis.redis_put_case(self.id, 'over')

    def _run(self):
        url = "wss://speech-test.ainirobot.com/ws/streaming-asr"
        socket = OrionAsr(url)
        path = os.getcwd()
        while True:
            data = self.redis.redis_get_case(self.id)
            if data == 'over':
                break
            if not data:
                continue
            data = json.loads(data)
            whole_wavpath = os.path.join(os.path.join(self.wav_base_path, 'wav'), data.get('filename'))
            if os.path.exists(whole_wavpath):
                for i in range(5):
                    try:
                        result = socket.run(whole_wavpath, path)
                        self.redis.redis_put_result(self.id, result)
                    except Exception:
                        time.sleep(1)
                        continue
                    else:
                        break

            else:
                res = None
                notes = '路径："{}"文件不存在'.format(whole_wavpath)
                print(notes)



    def _save(self):
        sql = EngineDb()
        # sql.select_table(table)
        num = 0
        while True:
            data = self.redis.redis_get_result(self.id, 0)

            if data == 'over':
                # sql.commit()
                print(data)
                break
            if not data:
                continue
            data = json.loads(data)
            try:
                print('{}数量{}提交第{}条数据：{}'.format(self.taskname, self.case_num, num, data))
                sql.save_asr_result(data.get('filename'), data.get('type')
                                    , data.get('text'), self.taskname)
                num=num+1
                # if num == 50:
                #     num=0
                sql.commit()
            except Exception as e:
                continue

    def client_run(self):
        sbc_list = []
        for i in range(10):
            sbc_list.append(Thread(target=self._run))
        for i in sbc_list:
            i.start()
        for i in sbc_list:
            i.join()
        for i in range(100):
            self.redis.redis_put_result(self.id, 'over')

    def start(self):
        self.redis.task_del_case_result(self.id)
        # Thread(target=self._read_case).start()
        Thread(target=self._resume_read_case).start()
        Thread(target=self.client_run).start()
        self._save()
        self.redis.task_del_case_result(self.id)

    def _run_none(self):
        Thread(target=self._resume_none_read_case).start()
        Thread(target=self.client_run).start()
        self._save()
        self.redis.task_del_case_result(self.id)

    def resume(self):
        self.start()
        sql = EngineDb()
        done = sql.count_done_case(self.taskname, 'lh')
        case_num = sql.count_case_number(self.run_item)
        if done != case_num:
            self.start()
        self.redis.task_del_case_result(self.id)
        self._run_none()


if __name__ == '__main__':
    sbc = XunFei('2020914_test', '/mnt/20200831_wav')
    sbc.start()
