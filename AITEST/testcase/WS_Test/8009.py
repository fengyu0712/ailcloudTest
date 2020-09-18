from common.T_websocket import WsSingle
from common import Traversing_path
from common.conf import Conf
from common.m_process import mprocess
import Project_path
import ssl,json
from common.read_xls_news import Read_xls
from common.changeChineseNumToArab import changeChineseNumToArab

xls="D:\\Users\\lijq36\\Desktop\\8009.xls"
xls_new="E:\\AITEST\\TestResult\\8009.xls"
r = Read_xls(xls)
w=r.copy_book()

ssl._create_default_https_context = ssl._create_unverified_context
conf_path= Project_path.conf_path
url = Conf(conf_path + "/ws.ini").get_value("WS", "url")
ws=WsSingle(url)
wav_path="E:\\8009项目\\019"
wav_list=Traversing_path.file_all_path(wav_path,file_type="wav")
print(wav_list)

def test(wav):
    wav_name = wav.split('.')[0].split('\\')[-1]
    a = ws.runsingle(wav)
    result = json.loads(a)
    print(wav_name, result['text'].replace(' ', ""))


if __name__ == '__main__':
    mprocess(test,wav_list)
    ws.close()



# for each in wav_list:
#     wav_name=each.split('.')[0].split('\\')[-redis_case]
#     wav_id=wav_name.split('_')[-redis_case]
#     a=ws.runsingle(each)
#     txt=json.loads(a)['text'].replace(' ',"")
#     r.write_onlydata(w, int(wav_id), 5,txt,sheetname='019M41_02_020M24_13_021F30_1')
#     r.write_onlydata(w, int(wav_id), 6, wav_name,sheetname='019M41_02_020M24_13_021F30_1')
#     print(wav_name,txt)
# r.save_write(w,xls_new)
# ws.close()



