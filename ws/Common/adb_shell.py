import subprocess,time,re,os,winsound,time
def adb_info():
    cmd = "adb shell logread -f"
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          errors='ignore')
    for i in iter(p.stdout.readline, b''):
        print(i)
now = time.strftime('%Y-%m-%d-%H-%M-%S')

def w_info():
    adb_log_path = "adb_log_%s.log" % now
    f = open(adb_log_path, 'w')
    endtime = time.time() + 5
    cmd = "adb shell logread -f"
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         encoding='utf8', errors='ignore')
    for i in iter(p.stdout.readline, b''):
        f.write(i)
    return str

def get_info():
    str=''
    endtime = time.time() + 5
    cmd = "adb -s 1515841703 shell  logread -f"
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         encoding='utf8', errors='ignore')
    for i in iter(p.stdout.readline, b''):
        str+=i
        if time.time() > endtime:
            break
    return str
def get_devices_info():
    p = subprocess.Popen("adb devices", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                     encoding='utf8').communicate()[0]
    try:
        pattern = "\n(.*)	device"
        devices_list = re.findall(pattern, p)
        assert len(devices_list) > 0
    except:
        reslt = False
    else:
        reslt = devices_list
    return reslt

if __name__=="__main__":
    a=get_devices_info()
    print(a)
    # pattern1="asr\":\t\"(.*)\",\n\n\t\t\"tts"
    # b=re.findall(pattern1,a)
    # print(b)