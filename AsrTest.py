import glob
import os
import time
from collections import Counter
from threading import Thread

import openpyxl

from AsrEngineContrasts import ReplaceCharacter
from AsrEngineContrasts.AsrEngineDB import EngineDb
from AsrEngineContrasts.Api.SbcApi import SbcWebSocketApp, SbcClient
from AsrEngineContrasts.Api.XfApi import XfClient
from AsrEngineContrasts.Api.Orion import OrionAsr
from multiprocessing import Process, Queue
from AsrEngineContrasts.SBC import Sbc as SbcRunClient
# from queue import Queue
que = Queue()


def save_result(msg):
    que.put(msg)


def Sbc(datalist):
    for i in datalist:
        for n in range(3):
            try:
                socket = SbcClient()
                result = socket.run(i)
                save_result(result)
            except Exception as e:
                pass
            else:
                break
    # socket = SbcWebSocketApp(datalist, save_result)
    # socket.start()


def Xf(datalist):
    for i in datalist:
        for n in range(3):
            try:
                socket = XfClient()
                result = socket.run(i)
                save_result(result)
            except Exception as e:
                pass
            else:
                break



def Orion(datalist):
    path = os.getcwd()
    url = "wss://speech-test.ainirobot.com/ws/streaming-asr"
    # url = "wwss://speech.ainirobot.com/ws/streaming-asr"
    socket = OrionAsr(url)
    n = 0
    for i in datalist:
        # result=socket.run(r'/home/kangyong/Data/wav/875ebfe7-ec5f-4a60-b995-f94c6bad5c3a_20200831082740_0b3d9fec-abed-4aa8-ba5a-0300bf797ed2.wav',path)

        for n in range(3):
            try:
                result = socket.run(i, path)
                save_result(result)
                n = n + 1
            except Exception as e:
                pass
            else:
                break


#        if n ==10:
#            break


def make_avg_data(data, num, tasklist=None):
    task_data_list = []
    datalist = []
    if tasklist:
        for i in data:
            if os.path.basename(i) in tasklist:
                task_data_list.append(i)
    else:
        task_data_list = data

    avg = int((len(task_data_list) - 1) / num)
    start = 0
    end = 0
    for i in range(1, num + 1):
        if i == num:
            datalist.append(task_data_list[start:])
        else:
            end = avg * i
            datalist.append(task_data_list[start:end])
            start = avg * i
    return datalist


def SbcRun(dir, tasklist=None):
    input_dir = dir + r'/*.wav'
    list_im = glob.glob(input_dir)
    data_list = make_avg_data(list_im, 10, tasklist)
    t_list = []
    for i in data_list:
        print('数量：', len(i))
        t_list.append(Thread(target=Sbc, args=(i,)))
    for i in t_list:
        i.start()
        time.sleep(1)
    for i in t_list:
        i.join()
    print('SbcRun stop')


def XfRun(dir, data_list):
    input_dir = dir + r'/*.wav'
    list_im = glob.glob(input_dir)
    data_list = make_avg_data(list_im, 10, data_list)
    t_list = []
    for i in data_list:
        t_list.append(Thread(target=Xf, args=(i,)))
    for i in t_list:
        i.start()
    for i in t_list:
        i.join()


def OrionRun(dir, tasklist):
    input_dir = dir + r'/*.wav'
    list_im = glob.glob(input_dir)

    data_list = make_avg_data(list_im, 10)
    t_list = []
    for i in data_list:
        t_list.append(Thread(target=Orion, args=(i,)))
    for i in t_list:
        i.start()
    for i in t_list:
        i.join()


def save(taskname):
    sql = EngineDb()
    # sql.select_table(table)
    num = 0
    while True:
        msg = que.get()
        print('{}提交数据：{}'.format(taskname,msg))
        # print('提交数量：', num, taskname, msg)
        if msg == 'over':
            # sql.commit()
            break
        sql.save_asr_result(msg.get('filename'), msg.get('type')
                            , msg.get('text'), taskname)
        # num = num + 1
        # if num >= 10:
        #     sql.commit()
        #     num = 0


def run_asr(data_list=None, taskname=None):
    # sql = Sqlite()
    table = ''
    # if not tablename:
    #
    #
    #     sql.create_table(table)
    # else:
    #     table = tablename
    if not taskname:
        table = 'AsrEngineResult{}'.format(time.strftime('%Y%m%d%H%M%S', time.localtime()))
    # sql.select_table(table)
    print(time.sleep(2))
    Thread(target=save, args=(table,)).start()
    # OrionRun()
    dir = '/mnt/20200831_wav/wav'
    # dir ='/data0/code/testwav/pcm'
    p_list = []
    p_list.append(Process(target=SbcRun, args=(dir, data_list,)))
    p_list.append(Process(target=XfRun, args=(dir, data_list,)))
    p_list.append(Process(target=OrionRun, args=(dir, data_list,)))
    for p in p_list:
        p.start()
    for p in p_list:
        p.join()
    time.sleep(30)
    que.put('over')


def get_result():
    sql = EngineDb()
    table = 'AsrEngineResult20200911173923'
    # sql.select_table()
    group = sql.group()
    print(group)
    max = 0
    name = ''
    for i in group:
        if i[1] >= max:
            max = i[1]
            name = i[0]
    print(name, max)
    index = 1
    n2t = ReplaceCharacter()
    ta = openpyxl.Workbook()
    sheet = ta.active
    sheet.append(['filename', 'sbc', 'lh', 'xf', 'result'])
    # while True:
    #     res=sql.result(table,20000,index)
    #     if not res:
    #         break
    #     index=index+1
    #
    #     print(res)
    #     for  n in res:
    #         sheet.append(list(n))

    # print(t)
    while True:
        res = sql.results(table, 10000, index)
        if not res:
            break

        index=index+1
        for i in res:
            # print(i.__dict__)
            # data = sql.asr_result(i[0])
            # datalist = []
            # xf = '该音频未测试！！'
            # sbc = '该音频未测试！！'
            # lh = '该音频未测试！！'
            # filename = ''
            # for n in data:
            #     filename = n.filename
            #
            #     if n.category == 'sbc':
            #         sbc = n.text
            #     if n.category == 'xf':
            #         xf = n.text
            #
            #     if n.category == 'lh':
            #         lh = n.text
            # # 'sbc', 'lh', 'xf'
            filename=i.filename
            xf = i.xf
            sbc = i.sbc
            lh =i.lh
            re_data = [n2t.Number2Text(sbc), n2t.Number2Text(lh), n2t.Number2Text(xf)]
            result = Counter(re_data)
            items = list(result.items())
            text = ''
            if len(items) == 1:
                key = items[0][0]
                if key == '该音频未音频未测试！！':
                    test = '全部未测试'
                elif key:
                    text = '完全相同非空'
                else:
                    text = '完全相同空值'
            elif len(items) == 2:
                key = items[0][0]
                value = items[0][1]
                key1 = items[1][0]
                value1 = items[1][1]
                max_key = ''
                if value > value1:
                    max_key = key
                else:
                    max_key = key1
                if max_key:
                    if key == '该音频未测试！！':
                        test = '有两个引擎未测试'
                    else:
                        text = '有两个相同且不为空'
                else:
                    text = '有两个相同的空值'
            elif len(items) == 3:
                if '该音频未测试！！' in list(result.values()):
                    text = '有一个引擎未测试'
                else:
                    text = '完全不相同'
            sheet.append([filename, *re_data, text])
    # t2 = self.session.query(Result.filename).filter(Result.category == name).all()

    # for i in res:
    #     filename = i[0].replace('.pcm', '.wav')
    #     data = self.session.query(Result).filter(Result.filename == filename).all()
    #     datalist = []
    #     xf = '该音频未测试！！'
    #     sbc = '该音频未测试！！'
    #     lh = '该音频未测试！！'
    #     filename = ''
    #     for n in data:
    #         filename = n.filename
    #
    #         if n.category == 'sbc':
    #             sbc = n.text
    #         if n.category == 'xf':
    #             xf = n.text
    #
    #         if n.category == 'lh':
    #             lh = n.text
    #     re_data = [n2t.Number2Text(sbc), n2t.Number2Text(xf), n2t.Number2Text(lh)]
    #     result = Counter(re_data)
    #     items = list(result.items())
    #     text = ''
    #     if len(items) == 1:
    #         key = items[0][0]
    #         if key == '该音频未音频未测试！！':
    #             test = '全部未测试'
    #         elif key:
    #             text = '完全相同非空'
    #         else:
    #             text = '完全相同空值'
    #     elif len(items) == 2:
    #         key = items[0][0]
    #         value = items[0][1]
    #         key1 = items[1][0]
    #         value1 = items[1][1]
    #         max_key = ''
    #         if value > value1:
    #             max_key = key
    #         else:
    #             max_key = key1
    #         if max_key:
    #             if key == '该音频未测试！！':
    #                 test = '有两个引擎未测试'
    #             else:
    #                 text = '有两个相同且不为空'
    #         else:
    #             text = '有两个相同的空值'
    #     elif len(items) == 3:
    #         if '该音频未测试！！' in list(result.values()):
    #             text = '有一个引擎未测试'
    #         else:
    #             text = '完全不相同'
    #     sheet.append([filename, *re_data, text])
    #     print(re_data)
    ta.save('reuslt_finally_9-15_4.xlsx')
def insertcase():
    sql = EngineDb()
    file = open('D:\MyData\ex_kangyong\Desktop\wavfile.log', 'r')
    data = file.readlines()
    datalist = []
    for i in data:
        if len(i):
            datalist.append({'filename':i.rstrip('\n'),'dict_assert':"{}",'suiteid':10})
            if len(datalist) == 5000:
                sql.insertcase(datalist)
                datalist=[]
    sql.insertcase(datalist)



if __name__ == '__main__':
    get_result()
    # insertcase()
    #     data_list='''e10f1ef9ee4188fb9354651a48be98f8_20200831161944_e3758539-12de-4182-b104-69d103b5cf5d.wav
    # e86c7e26-7716-4fea-9406-501fe4621d35_20200831131932_801775b8-513a-4513-b3ff-4b3f7f9fdd6b.wav
    # b4c3115b-6d0b-4d3a-a881-e0d7455976de_20200831114507_c00ebde6-9057-4af1-915d-1bbc12068fd8.wav'''.splitlines()
    #     dir = '/home/kangyong/Data/wav'
    # run_asr()
    # sbc = SbcRunClient('2020914_test', '/mnt/20200831_wav')
    # sbc.start()
