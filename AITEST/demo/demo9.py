import time,sys,os,platform
# 获取绝对路径，以便shell脚本跑
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from pydub import AudioSegment
from common.Traversing_path import file_all_path

# 音频文件路径
path = "E:\AITEST\demo\o_mp3\\"
path1 = "E:\AITEST\demo\\t_mp3\\"
# 读取音频文件，设置采样率<default=44100>
#
# a=file_all_path(path1,file_type="mp3")
# for each in a:
#     mp3_name = each.split('\\')[-1].replace('mp4','mp3')
#     result_path = path + mp3_name
#     song = AudioSegment.from_mp3(each).set_frame_rate(22050)
#     # 按32k的bitrate导出文件到指定路径,这里是直接覆盖原文件
#     song.export(result_path, format='mp3', bitrate='16k')
#     print('已转码--%s'%result_path)



path2="E:\AITEST\demo\o_mp3\相亲.mp4"
result_path="E:\AITEST\demo\\t_mp3\\三鞭子.mp3"
result_path1="E:\AITEST\demo\\t_mp3\\三鞭子1.mp3"
# song = AudioSegment.from_file(path2)
# song.export(result_path, format='mp3', bitrate='128k')
# print(result_path)
song = AudioSegment.from_mp3(result_path).set_frame_rate(22050) #采样率也要修改才行
song.export(result_path1, format='mp3', bitrate='24k')
print(result_path1)