import time
import pygame

file = r'result.mp3'
pygame.mixer.init()
print("播放音乐1")
pygame.mixer.music.load(file)
pygame.mixer.music.play()
time.sleep(10)
pygame.mixer.music.stop()



# import time
# import os
# os.system("result.mp3")
# time.sleep(10)
# os.system("taskkill /F /IM wmplayer.exe")