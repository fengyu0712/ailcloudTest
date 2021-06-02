# @Time : 2021/2/22 16:34 
# @Author : lijq36
# @File : audio_generation.py 
# @Software: PyCharm

import sys
import os
import uuid
import requests
from pydub import AudioSegment
from config import base_path

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


# 电脑还需安装ffmpeg，进行音频转码
# AudioSegment.ffmpeg = os.getcwd()+"\\ffmpeg\\bin\\ffmpeg.exe"


def audio_generation(audio_name):
    host = "http://tts.dui.ai/runtime/v1/synthesize?productId=278571380"
    data = {
        "context": {
            "productId": "278571380"
        },
        "request": {
            "audio": {
                "returnUrl": True
            },
            "requestId": f"{uuid.uuid1().hex}",
            "tts": {
                "speed": 1,
                "text": f"{audio_name}",
                "textType": "test",
                "voiceId": "gqlanf",
                "volume": 90
            }
        }
    }
    result = requests.post(host, json=data).json()
    tts_url = result["result"]["url"]
    audio_path = os.path.join(base_path + os.sep + "audio_file" + os.sep, audio_name + ".mp3")
    result_path = os.path.join(base_path + os.sep + "audio_file" + os.sep, audio_name + ".wav")

    with open(audio_path, "wb") as code:
        code.write(requests.get(tts_url).content)
    song = AudioSegment.from_mp3(audio_path)
    song.export(result_path, format='wav', bitrate="16k")
    # song.export(result_path, format='opus', bitrate="16k")
    print(f"生成音频文件{result_path}")
    os.remove(audio_path)


if __name__ == '__main__':
    audio_generation("明天天气怎么样")
