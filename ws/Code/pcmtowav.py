import wave
import os

# pcm_path="D:\\Users\ex_lijq4\Desktop/1/vad2local_2mic1.pcm"
wav_file="D:\\Users\ex_lijq4\Desktop/2/"

cmd_path = "D:/Users/ex_lijq4/Desktop/yinpin/"
a=os.listdir(cmd_path)
print(a)
for each in a:
    print(cmd_path+each)
    with open(cmd_path+each, 'rb') as pcmfile:
        pcmdata = pcmfile.read()
    with wave.open(wav_file+each+'.wav', 'wb') as wavfile:
        wavfile.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
        wavfile.writeframes(pcmdata)
