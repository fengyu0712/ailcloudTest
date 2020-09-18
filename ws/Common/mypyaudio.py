import pyaudio
import wave
from tqdm import tqdm
import time
def play_audio(wave_path):
  CHUNK = 1024
  wf = wave.open(wave_path, 'rb')
  # instantiate PyAudio (1)
  p = pyaudio.PyAudio()
  # open stream (2)
  stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
          channels=wf.getnchannels(),
          rate=wf.getframerate(),
          output=True)
  # read data
  data = wf.readframes(CHUNK)
  # play stream (3)
  datas = []
  while len(data) > 0:
    data = wf.readframes(CHUNK)
    datas.append(data)
  for d in tqdm(datas):
    stream.write(d)
  # stop stream (4)
  stream.stop_stream()
  stream.close()
  # close PyAudio (5)
  p.terminate()

def play_audio_callback(wave_path):
  CHUNK = 1024
  wf = wave.open(wave_path, 'rb')
  # instantiate PyAudio (1)
  p = pyaudio.PyAudio()
  def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, pyaudio.paContinue)
  # open stream (2)
  stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
          channels=wf.getnchannels(),
          rate=wf.getframerate(),
          output=True,
          stream_callback=callback)
  # read data
  stream.start_stream()
  while stream.is_active():
    time.sleep(0.1)
  # stop stream (4)
  stream.stop_stream()
  stream.close()
  # close PyAudio (5)
  p.terminate()


import pyaudio
import wave
from tqdm import tqdm
import time



def play_audio_callback1(wave_path):
    CHUNK = 1024

    wf = wave.open(wave_path, 'rb')

    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()

    def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)
        return (data, pyaudio.paContinue)

    # open stream (2)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    input=True,
                    output=True,
                    stream_callback=callback)

    # read data
    stream.start_stream()

    while stream.is_active():
        time.sleep(0.1)

    # stop stream (4)
    stream.stop_stream()
    stream.close()

    # close PyAudio (5)
    p.terminate()

if __name__=="__main__":
    # play_audio_callback("output.wav")
    wakeup_path = "E:/ws/test_audio/002M30_36_010003.wav"  # #唤醒文件：你好小美的音频文件
    play_audio(wakeup_path)
    print(1)