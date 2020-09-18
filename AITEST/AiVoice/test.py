#!/usr/bin/python3
# coding: utf-8
import os
from pypinyin import lazy_pinyin, TONE3
from pydub import AudioSegment


# 中间插入空白静音500ms。
silent = AudioSegment.silent(duration=500)

# 单字音频文件的路径
PINYIN_VOICE_PATH = 'E:\python_space\AITEST\AiVoice\pinyin'

# 最终合成的音频文件路径
EXPORT_PATH = 'E:\python_space\AITEST\AiVoice\\voice'

def load_voice_dict():
    voice_file_list = [f for f in os.listdir(PINYIN_VOICE_PATH) if f.endswith('.wav')]
    voice_dict = {}

    for voice_file in voice_file_list:
        name = voice_file[:-4]
        song = AudioSegment.from_wav(os.path.join(PINYIN_VOICE_PATH, voice_file))
        voice_dict.setdefault(name, song)
    return voice_dict

VOICE_DICT = load_voice_dict()

def txt_to_voice(text, name='test'):
    """
    将文字转换为音频
    :param text: 需要转换的文字
    :param name: 生成的音频文件名
    :return:
    """
    pinyin_list = lazy_pinyin(text, style=TONE3)
    print(pinyin_list)
    new = AudioSegment.empty()
    for piny in pinyin_list:
        piny_song = VOICE_DICT.get(piny)
        if piny_song is None and piny and piny[-1] not in '0123456789':
            # 没有音调
            piny = piny + '5'
            piny_song = VOICE_DICT.get(piny, silent)

        # 交叉渐入渐出方法
        # with_style = beginning.append(end, crossfade=1500)
        # crossfade 就是让一段音乐平缓地过渡到另一段音乐，crossfade = 1500 表示过渡的时间是1.5秒。
        crossfade = min(len(new), len(piny_song), 1500)/60
        new = new.append(piny_song, crossfade=crossfade)

        # new += piny_song

    new.export(os.path.join(EXPORT_PATH, "{}.mp3".format(name)), format='mp3')

def main():
    # text = '''    红海早过了。船在印度洋面上开驶着。但是太阳依然不饶人地迟落早起侵占去大部分的夜。
    # 夜仿佛纸浸了油，变成半透明体；它给太阳拥抱住了，分不出身来，也许是给太阳陶醉了，
    # 所以夕照霞隐褪后的夜色也带着酡红。到红消醉醒，船舱里的睡人也一身腻汗地醒来，洗了澡赶到甲板上吹海风，
    # 又是一天开始。这是七月下旬，合中国旧历的三伏，一年最热的时候。在中国热得更比常年利害，
    # 事后大家都说是兵戈之象，因为这就是民国二十六年【一九三七年】。'''
    text="美的智能家电"

    txt_to_voice(text)

if __name__ == '__main__':
    main()