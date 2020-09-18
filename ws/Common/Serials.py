import os,re
import winsound
import time
import datetime
import serial
import serial.tools.list_ports

class MySerial():
    def __init__(self,baud_bate,serialName=None):
        plist = list(serial.tools.list_ports.comports())
        if len(plist) <= 0:
            print("The Serial port can't find!")
        else:
            plist_0 = list(plist[0])
            if serialName  is None:
                serialName = plist_0[0]
            self.serialFd = serial.Serial(serialName, baud_bate, timeout=60)
            print("check which port was really used >", self.serialFd.name)
            if self.serialFd.isOpen():
                print("Serial port open success")
            else:
                print("Serial port open failed")
    def recvCmd(self, pattern,checktime=None):
        if checktime is None:
            checktime=10
        for i in range(checktime*2):
            data = self.serialFd.read_all()
            data = str(data, encoding="utf8")
            if data == "":
                time.sleep(0.5)
                continue
            else:
                break
        result_data = re.findall(pattern, data)
        try:
            result_data=result_data[0]
        except:
            result_data=None
        return result_data
    def recvCmd2(self, pattern,mode=None,checktime=None):
        if checktime is None:
            checktime=2
        result_data = {}
        for i in range(checktime*2):
            data = self.serialFd.read_all()
            data = str(data, encoding="utf-8")
            if isinstance(pattern,dict):
                for k in pattern:
                    result_data0 = re.findall(pattern[k], data)
                    if result_data0!=[]:
                        result_data[k]=result_data0[0]
                if  mode=="OR":
                    if result_data == {}:
                        time.sleep(0.5)
                        continue
                    else:
                        break
                elif mode=="AND":
                    if len(result_data)<len(pattern):
                        time.sleep(0.5)
                        continue
                    else:
                        break
                else:
                    if len(result_data) < len(pattern):
                        time.sleep(0.5)
                        continue
                    else:
                        break

            else:
                result_data = re.findall(pattern, data)
                try:
                    result_data=result_data[0]
                except:
                    result_data=None
                if result_data  is None:
                    time.sleep(0.5)
                    continue
                else:
                    break
        return result_data
    def close(self):
        self.serialFd.close()

if __name__=="__main__":
    pre_path = "E:\ws\\002M30_36\\002M30_36_010001.wav"
    wakeup_path = "E:/ws/test_audio/002M30_36_010003.wav"
    pattern0="\"wakeupWord\"\:\"(.*)\"\,\"major"
    pattern1 = "\"asr\":	\"(.*)\""
    pattern ={"pattern0":pattern0,"pattern1":pattern1}
    s=MySerial("921600")
    winsound.PlaySound(wakeup_path, winsound.SND_FILENAME)
    winsound.PlaySound(pre_path, winsound.SND_FILENAME)
    # r=s.recvCmd2(pattern1)
    r=s.recvCmd(pattern0)
    print(r)