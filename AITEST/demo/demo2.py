import time
import winsound
from common import Traversing_path

# list=Traversing_path.file_all_path("E:\云知声\信噪比唤醒词")

list=['E:\\云知声\\信噪比唤醒词\\001M26_01_40_0001.wav', 'E:\\云知声\\信噪比唤醒词\\001M28_01_42_0001.wav', 'E:\\云知声\\信噪比唤醒词\\001M33_08_42_0001.wav', 'E:\\云知声\\信噪比唤醒词\\003M29_01_40_0001.wav', 'E:\\云知声\\信噪比唤醒词\\004F22_01_40_0001.wav', 'E:\\云知声\\信噪比唤醒词\\005F20_01_40_0001.wav', 'E:\\云知声\\信噪比唤醒词\\005M37_05_42_0001.wav', 'E:\\云知声\\信噪比唤醒词\\006M37_11_42_0001.wav', 'E:\\云知声\\信噪比唤醒词\\008F31_02_40_0001.wav', 'E:\\云知声\\信噪比唤醒词\\008M27_08_42_0001.wav', 'E:\\云知声\\信噪比唤醒词\\010F30_02_40_0001.wav', 'E:\\云知声\\信噪比唤醒词\\011F27_01_42_0001.wav', 'E:\\云知声\\信噪比唤醒词\\011F55_03_40_0001.wav', 'E:\\云知声\\信噪比唤醒词\\012F29_06_42_0001.wav', 'E:\\云知声\\信噪比唤醒词\\013F26_00_42_0001.wav', 'E:\\云知声\\信噪比唤醒词\\014M53_03_40_0001.wav', 'E:\\云知声\\信噪比唤醒词\\015F34_05_42_0001.wav', 'E:\\云知声\\信噪比唤醒词\\015M50_03_40_0001.wav', 'E:\\云知声\\信噪比唤醒词\\016F30_06_42_0001.wav', 'E:\\云知声\\信噪比唤醒词\\017F35_04_42_0001.wav']

file=list[12]
print(file)


# for i in range(len(list)):
#     a=

n=1
while n<=20:
    print(n)
    winsound.PlaySound(file, winsound.SND_FILENAME)
    time.sleep(2.5)
    n+=1
# pygame.mixer.init()
# print("播放音乐1")
# pygame.mixer.music.load(file)
# pygame.mixer.music.play()
# time.sleep(10)
# pygame.mixer.music.stop()