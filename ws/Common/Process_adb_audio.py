import subprocess,time,re,os,winsound
from Common import log,read_xls_news
from Common import mypyaudio
from multiprocessing import Manager,Process,Pool

cmd = "adb shell logread -f"
p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding='utf8',errors='ignore')
Log = log.Logger()
def adb_info(pattern,timeout=None):
    if timeout  is None:
        timeout = 3
    begin_time = time.time()
    endtime = begin_time + timeout
    result = False
    for i in iter(p.stdout.readline, b''):
        Log.debug(i)
        nowtime = time.time()
        if nowtime > endtime:
            break
        result_data = re.findall(pattern, i)
        try:
            result = result_data[0]
        except:
            result = False
        else:
            if len(result)>1:
                break
    p.kill()
    return result



def adb_info_listPatten(pattern_list,timeout):
    endtime = time.time() + timeout
    result_list = []
    for j in range(0,len(pattern_list)):
        pattern=pattern_list[j]
        for i in iter(p.stdout.readline, b''):
            if time.time() > endtime:
                break
            Log.debug(i)
            result_data = re.findall(pattern, i)
            if len(result_data)>0:
                result = result_data[0]
                if result !="":
                    result_list.append(result)
                    break
        j+=1
    while len(result_list)<len(pattern_list):
        result_list.append(False)
    p.kill()
    return result_list

def main(patternlist,wav_path,timeout=None):
    if timeout is None:
        timeout=5
    q = Pool(2)
    res = q.apply_async(adb_info_listPatten, args=(patternlist,timeout,))
    # q.apply_async(winsound.PlaySound, args=(wav_path,winsound.SND_FILENAME,))
    q.apply_async(mypyaudio.play_audio, args=(wav_path,))
    q.close()
    q.join()
    print("结果是：%s" % res.get())
    return  res.get()

def main2(patternlist,wav_path,timeout=None):
    if timeout is None:
        timeout=5
    from concurrent.futures import ThreadPoolExecutor
    threadPool = ThreadPoolExecutor(max_workers=4, thread_name_prefix="test_")
    res = threadPool.submit(adb_info_listPatten, patternlist,timeout,)
    # q.apply_async(winsound.PlaySound, args=(wav_path,winsound.SND_FILENAME,))
    threadPool.submit(mypyaudio.play_audio, wav_path,)
    threadPool.shutdown(wait=True)
    print("结果是：%s" % res.result())
    return  res.result()


pattern2="text\":	\"(.*)\""
pattern = "\n(.*)	device"
wakeup_pattern = "ev(.*)wake up"
asr_pattern = "asr\":\\t\"(.*)\","
startTTS_pattern = "ev(.*)speak request start"
endTTS_pattern = "ev(.*)speak end"
in_fullduplex_pattern = "info(.*)full duplex"
mid_pattern="mid\":	\"(.*)\","
sessionId_patteern="sessionId\":	\"(.*)\","
pre_path = "E:\ws\\002M30_36\\002M30_36_010001.wav"  # 前置指令，进入全双工用
wakeup_path = "E:/ws/test_audio/002M30_36_010003.wav"  # #唤醒文件：你好小美的音频文件

if __name__ == '__main__':
    patternlist=[wakeup_pattern,pattern2,sessionId_patteern]
    main2(patternlist,wakeup_path,timeout=8)



