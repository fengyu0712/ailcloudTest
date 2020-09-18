#录音学习
import pyaudio
import wave
import threading
from tqdm import tqdm
# 定义数据流块

# 要写入的文件名
# WAVE_OUTPUT_FILENAME = "output.wav"
# 创建PyAudio对象

class MypyaudioThread(threading.Thread):
    def __init__(self,mode,wavpath):
        threading.Thread.__init__(self)
        self.bRecord = True
        self.wavpath=wavpath
        self.p = pyaudio.PyAudio()
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.frames = []
        self.wf = wave.open(self.wavpath, 'rb')
        # 打开数据流
        if mode=='output' :
            #播放音频的数据流设置

            self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                            channels=self.wf.getnchannels(),
                            rate=self.wf.getframerate(),
                            output=True)
        else:
            #录音的数据流设置
            self.stream = self.p.open(format=self.FORMAT,
                            channels=self.CHANNELS,
                            rate=self.RATE,
                            input=True,
                            frames_per_buffer=self.CHUNK)
    def play_sound(self):
        data = self.wf.readframes(self.CHUNK)
        # play stream (3)
        datas = []
        while len(data) > 0:
            data = self.wf.readframes(self.CHUNK)
            datas.append(data)
        for d in tqdm(datas):
            self.stream.write(d)
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
    def Timing_Record(self,RECORD_SECONDS):
        # 录音时间
        self.frames = []
        for i in range(0, int(self.RATE /self. CHUNK * RECORD_SECONDS)):
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)

        print("* done recording")
        # 停止数据流
        self.stream.stop_stream()
        self.stream.close()
        # 关闭PyAudio
        self.p.terminate()
        # 写入录音文件
        self.wf.setnchannels(self.CHANNELS)
        self.wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        self.wf.setframerate(self.RATE)
        self.wf.writeframes(b''.join(self.frames))
        self.wf.close()

    def start_Record(self):
        while self.bRecord:
            self.wf.writeframes(self.stream.read(self.CHUNK))
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
    def stopRecord(self):
        self.bRecord = False
        # 停止数据流

if __name__ == "__main__":
    # wakeup_path = "E:/ws/test_audio/002M30_36_010003.wav"  # #唤醒文件：你好小美的音频文件
    # Mypyaudio("output",wakeup_path).play_sound()
    R=MypyaudioThread("input","input.wav")
    R.start()
    print("开始录音")
    import time
    time.sleep(2)
    R.stopRecord()

# print("* recording")
#
# # 开始录音
# frames = []
# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#     data = stream.read(CHUNK)
#     frames.append(data)
#
# print("* done recording")
#
# # 停止数据流
# stream.stop_stream()
# stream.close()
#
# # 关闭PyAudio
# p.terminate()
#
# # 写入录音文件
# wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
# wf.setnchannels(CHANNELS)
# wf.setsampwidth(p.get_sample_size(FORMAT))
# wf.setframerate(RATE)
# wf.writeframes(b''.join(frames))
# wf.close()