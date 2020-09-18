import winsound,time
from common import Traversing_path
from playsound import playsound

test_fail="E:\需求\竞品测试\\002_1\\002"
wekup_wav="E:\需求\竞品测试\唤醒词\新建文件夹\db_04_0001.wav"
stop_play="E:\需求\竞品测试\唤醒词\停止播放.mp3"
test_list=Traversing_path.file_all_path(test_fail,file_type='wav')

def T1(i):
    a = input("输入指令（1：下一个；2：重试本条语料；0：播放停止）:")
    if a == '1':
        print("开始下一条测试！")
        i = i + 1
    elif a == '0':
        print("播放停止命令")
        playsound(stop_play)
        T1(i)
    elif a == '2':
        print("重试本条语料")
        i = i
    else:
        print("未定义的命令！")
        i=i
    return i


i=0
while i<len(test_list):
    print(test_list[i])
    winsound.PlaySound(wekup_wav, winsound.SND_FILENAME)
    time.sleep(1)
    winsound.PlaySound(test_list[i], winsound.SND_FILENAME)
    i=T1(i)

