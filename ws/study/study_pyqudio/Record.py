import threading
import pyaudio
import wave

class RecordThread(threading.Thread):
    def __init__(self, audiofile='record.wav'):
        threading.Thread.__init__(self)
        self.bRecord = True
        self.audiofile = audiofile
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
    def Timing_Record(self,RECORD_SECONDS):
        audio = pyaudio.PyAudio()
        wavfile = wave.open(self.audiofile, 'wb')
        wavfile.setnchannels(self.channels)
        wavfile.setsampwidth(audio.get_sample_size(self.format))
        wavfile.setframerate(self.rate)
        wavstream = audio.open(format=self.format,
                               channels=self.channels,
                               rate=self.rate,
                               input=True,
                               frames_per_buffer=self.chunk)
        for i in range(0, int(self.rate / self.chunk * RECORD_SECONDS)):
            wavfile.writeframes(wavstream.read(self.chunk))
        wavstream.stop_stream()
        wavstream.close()
        audio.terminate()
    def run(self):
        audio = pyaudio.PyAudio()
        wavfile = wave.open(self.audiofile, 'wb')
        wavfile.setnchannels(self.channels)
        wavfile.setsampwidth(audio.get_sample_size(self.format))
        wavfile.setframerate(self.rate)
        wavstream = audio.open(format=self.format,
                               channels=self.channels,
                               rate=self.rate,
                               input=True,
                               frames_per_buffer=self.chunk)
        while self.bRecord:
            wavfile.writeframes(wavstream.read(self.chunk))
        wavstream.stop_stream()
        wavstream.close()
        audio.terminate()
    def stopRecord(self):
        self.bRecord = False


if __name__ == "__main__":
    import time
    now=time.strftime("%Y%m%d%H%M%S")
    audio_record = RecordThread('G:\python\ws\study\study_pyqudio\\record%s.wav'%now)
    # audio_record.Timing_Record(5)
    audio_record.start()
    time.sleep(5)
    audio_record.stopRecord()
