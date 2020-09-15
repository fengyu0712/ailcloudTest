# -*-coding:utf-8 -*-
import glob
import json
import sys
import os
import re
import subprocess
import openpyxl
import xlrd as xlrd


def MakeDir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # print(path)
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        try:
            os.makedirs(path)
        except FileExistsError:
            return True
        # print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        # print(path + ' 目录已存在')
        return False


# 猎户的asr测试
class OrionAsr():
    def __init__(self, url):
        # 正式环境地址：
        # url地址
        # if env=="pro":
        #     self.URL = "wss://speech.ainirobot.com/ws/streaming-asr"  # 正式环境地址
        # else:
        #     self.URL="wss://speech-test.ainirobot.com/ws/streaming-asr"   # 测试环境地址
        self.URL = url

    # 获取asr的值
    def get_asr(self, whole_logpath):
        if os.path.exists(whole_logpath) == False:
            return ""

        asr_value = ""
        with open(whole_logpath, 'r', encoding='utf-8') as file_to_read:
            lines = file_to_read.read()  # 整行读取数据
            if lines != "" and lines != None:
                a = re.search("statistics asr text:(.*)", lines, flags=0)
                if a == "" or a == None:
                    return ""
                asr_value = a.group(1)
                asr_value = str(asr_value).strip().replace(' ', '')
                # print(asr_value)
        return asr_value

    def run(self, wav_path, logpath):
        try:
            MakeDir(os.path.dirname(logpath))
            basename = os.path.basename(wav_path)
            if basename.endswith(".wav"):
                wav_path = wav_path.replace(".wav", ".pcm").replace("/wav", "/pcm")
            # logpath=logpath+'_'+basename.replace(".wav","").replace(".pcm","")+"_log.txt"
            MakeDir(os.path.join(logpath, 'log'))
            logpath = os.path.join(os.path.join(logpath, 'log'),
                                   basename.replace(".wav", "").replace(".pcm", "") + "_log.txt")
            # logpath='/home/kangyong/Data/wav/log_3.txt'
            commeline = "./qnet-test -server_url='{}'  -compress_type=0  -pid=7016 -protocol=leve0 -audio='{}' -output_file='{}' -write_file_level=3".format(
                self.URL,wav_path,logpath)
            ret = subprocess.run(commeline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 encoding="utf-8",
                                 timeout=8)

            if ret.returncode == 0:
                # print("success:", ret)
                result_asr = self.get_asr(logpath)
                # print("猎户result_asr", result_asr)
                if os.path.exists(logpath):
                    os.remove(logpath)
                wav_path = wav_path.replace(".pcm", ".wav")
                return {'filename': os.path.basename(wav_path), 'type': 'lh', 'text': result_asr}
            else:
                # print("error:", ret)
                # print('cmd:',commeline)
                wav_path = wav_path.replace(".pcm", ".wav")
                if os.path.exists(logpath):
                    os.remove(logpath)
                return {'filename': os.path.basename(wav_path), 'type': 'lh', 'text': ''}
        except Exception as e:
            #           print("猎户asr错误",e)
            wav_path = wav_path.replace(".pcm", ".wav")
            if os.path.exists(logpath):
                os.remove(logpath)
            return {'filename': os.path.basename(wav_path), 'type': 'lh', 'text': ''}


if __name__ == "__main__":
    # OrionAsr().run("D:/audio_file/wav音频/全品类/019/019M20_07_45_0001.wav","")
    # URL = "wss://speech-test.ainirobot.com/ws/streaming-asr"
    # c = OrionAsr(URL)
    # # t=c.run('/run/media/centos/report/pcm/cyangfp_000001.pcm','/run/media/centos/HD/PycharmProjects/Web_Nlu/dev_nlu/Web_Nlu/AsrClient/public/log')
    # # t=c.run(r'/home/kangyong/Data/wav/875ebfe7-ec5f-4a60-b995-f94c6bad5c3a_20200831082740_0b3d9fec-abed-4aa8-ba5a-0300bf797ed2.wav','/home/kangyong/Data')
    # print(os.getcwd())
    # # print(t)
    # dir = '/home/kangyong/Data/pcm'
    # input_dir = dir + r'/*.pcm'
    # list_im = glob.glob(input_dir)
    # wss = openpyxl.Workbook()
    # sheet = wss.create_sheet(title='result', index=-1)
    # for i in list_im:
    #     # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    #     wavpath = r'/home/kangyong/Data/wav/993ea1f5-5558-43e4-9baa-c9b043534e2b_20200831204743_8fa3168e-4840-4f52-b16a-0b88801bc08a.wav'
    #
    #     # t=c.run(r'/home/kangyong/Data/wav/006baaa1-1387-4ae2-b771-1ef2f64a0e4f_20200831114419_bfa12807-7534-48e5-9d80-57a19850764e.wav','/home/kangyong/Data')
    #     # print(t)
    #     r = c.run(wavpath, 'home/kangyong/Data/PythonProject/AsrResult/AarContrasts')
    #     print(r)
    #     # sheet.append([os.path.basename(i),json.dumps(r,ensure_ascii=False)])
    #     print('????????????????????????????????????????')
    #     break
    URL = "wss://speech-test.ainirobot.com/ws/streaming-asr"
    c = OrionAsr(URL)
    path = '/mnt/20200831_wav/pcm'
    filename = ''
    result = c.run(os.path.join(path, filename),os.getcwd())
    print(result)
