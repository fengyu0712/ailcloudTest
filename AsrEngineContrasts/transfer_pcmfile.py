# -*- coding: utf-8 -*-
import os
import subprocess
# rootPath = "D:/audio_file/1/"  # 原音频文件路径
# pcm_new_rootPath = "D:/audio_file/1/pcm/"  # 转换为pcm文件后存放的路径
rootPath='/data1/20200831_wav/wav/'
pcm_new_rootPath='/data1/20200831_wav/pcm/'


if __name__=="__main__":
    list1 = os.listdir(rootPath)
    for item in list1:
        file_path = rootPath + item
        if os.path.isdir(file_path):
            continue

        if item.endswith(".wav")==False:
            continue

        new_filepath=pcm_new_rootPath+item.replace(".wav",".pcm")
        commonline = "sox -t wav " + file_path + " -t raw -r 16000 -c 1 -b 16 " + new_filepath + ""
        ret = subprocess.run(commonline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             timeout=5)
        print(ret)
        print("成功....")
