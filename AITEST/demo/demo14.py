import re, os, xlsxwriter,datetime


class WriteExcel:
    def __init__(self, path):
        self.wb = xlsxwriter.Workbook(path)

    def creattable(self, sheet_name):
        # self.wb.
        self.sheet = self.wb.add_worksheet(sheet_name)

    def write_onlydata(self, row, col, vale):
        self.sheet.write(row, col, vale)

    def write_linedata(self, row, list_data, start_col=None):
        if start_col == None:
            start_col = 0
        for i in range(len(list_data)):
            self.write_onlydata(row, i + start_col, list_data[i])

    def close(self, ):
        self.wb.close()


# logpath = r"E:/log/rk3308.log"
logpath = r"E:/log/testlog.txt"


m_aicloud_end = "\[(.+?)\]\(m_aicloud_end(.*)VAD END"
m_cloud_speech_trans_ack = "\[(.+?)\]\(m_cloud_speech_trans_ack(.*)ASR"
m_parse_speech_reply_to_tts = "\[(.+?)\]\(m_parse_speech_reply_to_tts(.*)TTS"
http_connect1 = "\[(.+?)\]\(http_connect(.*)Connected"
io_open_default = "\[(.+?)\]\(io_open_default(.+?)Opening 'http"
http_read_header = "\[(.+?)\]\(http_read_header(.*)Got"
http_connect2 = "\[(.+?)\]\(http_connect(.*)Got"
SDL_RunAudio = "\[(.+?)\]\(SDL_RunAudio(.*)Start"


now1 = datetime.datetime.now()
with open(logpath, encoding='utf-8') as f:
    linesdata = f.readlines()


data_list = []
line = 0
while line < len(linesdata):
    def t2(m, str1):
        time1 = re.findall(m, linesdata[line])
        # print(time1)
        if len(time1) > 0:
            data_list.append(str1 + ":" + time1[0][0])
    t2(m_aicloud_end, "m_aicloud_end")
    t2(m_cloud_speech_trans_ack, "m_cloud_speech_trans_ack")
    t2(m_parse_speech_reply_to_tts, "m_parse_speech_reply_to_tts")
    t2(io_open_default, "io_open_default")
    t2(http_connect1, "http_connect1")
    t2(http_read_header, "http_read_header")
    t2(http_connect2, "http_connect2")
    t2(SDL_RunAudio, "SDL_RunAudio")
    line += 1
print("完成正则筛选数据,共:%s条数据"%len(data_list))

for i in range(len(data_list) - 1, 0, -1):
    if "m_aicloud_end" in data_list[i] and "m_aicloud_end" in data_list[i + 1]:
        del data_list[i]

for j in range(len(data_list) - 1, 0, -1):
    if "SDL_RunAudio" in data_list[j] and "SDL_RunAudio" in data_list[j - 1]:
        del data_list[j]

print("删除无效数据后,共:%s条数据"%len(data_list))

result_path = 'E:\AITEST\TestResult\\3308_result.xls'
w = WriteExcel(result_path)
w.creattable("3308拆解耗时")
w.write_linedata(0, ["m_aicloud_end", "m_cloud_speech_trans_ack", "m_parse_speech_reply_to_tts", "io_open_default",
                     "http_connect1", "http_read_header", "http_connect2", "SDL_RunAudio"])
list0 = []
for a in range(len(data_list)):
    for b in range(a,len(data_list)):
        if "m_aicloud_end" in data_list[a] and "m_aicloud_end" in data_list[b] and 9 > b - a > 0 and data_list[a:b]!=[]:
            list0.append(data_list[a:b])
            break
print("按照语音对话组合,共:%s条数据"%len(list0))

for i in range(len(list0)):
    for j in range(len(list0[i])):
        print(list0[i][j])
        time_list = list0[i][j].split(":", 1)
        if time_list[0] == "m_aicloud_end":
            w.write_onlydata(i+1, 0, time_list[1])
        elif time_list[0] == "m_cloud_speech_trans_ack":
            w.write_onlydata(i+1, 1, time_list[1])
        elif time_list[0] == "m_parse_speech_reply_to_tts":
            w.write_onlydata(i+1, 2, time_list[1])
        elif time_list[0] == "io_open_default":
            w.write_onlydata(i+1, 3, time_list[1])
        elif time_list[0] == "http_connect1":
            w.write_onlydata(i+1, 4, time_list[1])
        elif time_list[0] == "http_read_header":
            w.write_onlydata(i+1, 5, time_list[1])
        elif time_list[0] == "http_connect2":
            w.write_onlydata(i+1, 6, time_list[1])
        elif time_list[0] == "SDL_RunAudio":
            w.write_onlydata(i+1, 7, time_list[1])
        else:
            print("error")
        j+=1
    i+=1
w.close()
now2 = datetime.datetime.now()
t_time = now2 - now1
print(t_time)