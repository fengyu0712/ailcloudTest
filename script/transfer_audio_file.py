# -*- coding: utf-8 -*-
import os
from queue import Queue
import subprocess
from threading import  Thread

rootPath = "D:/audio_file/1/"  # 原音频文件路径
pcm_new_rootPath = "D:/audio_file/1/pcm/"  # 转换为pcm文件后存放的路径

wav_new_rootPath = "D:/audio_file/1/wav/"  # 转换为pcm文件后存放的路径

is_trans_wav = True  # 是否需要转换wav格式,true 表示转换，false表示不转换.
is_trans_pcm = True  # 是否需要转换pcm格式

def trans_pcm(source_path,new_filepath):
    commonline = "sox -t wav " + source_path + " -t raw -r 16000 -c 1 -b 16 " + new_filepath + ""
    ret = subprocess.run(commonline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         timeout=5)
    if ret.returncode == 0:
        print("转换成功")

    else:
        print("转换失败", ret)

def trans_wav(source_path,new_filepath):
    commonline = "sox \"" + source_path + "\" -r 16000 -c 1 -b 16 \"" + new_filepath + "\" "
    print(commonline)
    ret = subprocess.run(commonline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         timeout=5)
    if ret.returncode == 0:
        print("转换成功")

    else:
        print("转换失败", ret)

def create_dir(a_path):
    try:
        if not os.path.exists(a_path):
            os.makedirs(a_path)
    except:
        pass

    finally:
        pass

def start_transfer(q):
    while True:
        if q.empty():
            return
        else:
            source_path=q.get()
            basename=os.path.basename(source_path)
            basepath=os.path.dirname(source_path)+"/"
            child_path=basepath.replace(rootPath,"")
            if is_trans_wav:
                a_path = wav_new_rootPath + child_path
                create_dir(a_path)

                trans_wav(source_path, a_path+basename)

            if is_trans_pcm:
                a_path = pcm_new_rootPath + child_path
                create_dir(a_path)

                new_filepath = a_path + basename.replace(".wav", ".pcm")
                trans_pcm(source_path, new_filepath)

def put_wav_to_quene(q,current_rootpath):
    list1 = os.listdir(current_rootpath)
    print(list1)
    for item in list1:
        file_path = current_rootpath + item
        if os.path.isdir(file_path):     # 如果是目录，则递归进行转换.
            put_wav_to_quene(q,file_path+"/")
            continue

        if item.endswith(".wav") == False:
            continue

        q.put(file_path);


if __name__=="__main__":
     q=Queue()
     t1=Thread(target=put_wav_to_quene,args=(q,rootPath,))
     t1.start()
     t1.join()

     thread_num =10
     threads = []
     for i in range(thread_num):
         t2 = Thread(target=start_transfer, args=(q,))
         threads.append(t2)

     for i in range(thread_num):
         threads[i].start()
     for i in range(thread_num):
         threads[i].join()
