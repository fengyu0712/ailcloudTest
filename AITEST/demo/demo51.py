import re, os, xlsxwriter, datetime,threading
import sys

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


m_aicloud_end = "\[(.+?)\]\(m_aicloud_end.*VAD END"
m_cloud_speech_trans_ack = "\[(.+?)\]\(m_cloud_speech_trans_ack.*ASR"
m_parse_speech_reply_to_tts = "\[(.+?)\]\(m_parse_speech_reply_to_tts.*TTS"
io_open_default = "\[(.+?)\]\(io_open_default.*Opening 'http"
http_connect1 = "\[(.+?)\]\(http_connect.*Connected"
http_read_header = "\[(.+?)\]\(http_read_header.*Got"
http_connect2 = "\[(.+?)\]\(http_connect.*Got"
SDL_RunAudio = "\[(.+?)\]\(SDL_RunAudio.*Start"

logpath = r"E:\\AITEST\demo\\log\\1.log"
# logpath="E:/log/rk3308.log"
result_path = 'E:\\AITEST\demo\\log/1.xls'
now1 = datetime.datetime.now()
with open(logpath, encoding='utf-8') as f:
    linesdata = f.readlines()

data_list = []
list = [m_aicloud_end, m_cloud_speech_trans_ack, m_parse_speech_reply_to_tts, io_open_default, http_connect1,
        http_read_header, http_connect2, SDL_RunAudio]
w = WriteExcel(result_path)
w.creattable("log")
w.write_linedata(0, ["m_aicloud_end", "m_cloud_speech_trans_ack", "m_parse_speech_reply_to_tts", "io_open_default",
                     "http_connect1", "http_read_header", "http_connect2", "SDL_RunAudio"])


def ProcessLog(line,w_line):
    def t1(m, line):
        print(line, linesdata[line])
        result0 = re.findall(m, linesdata[line])
        if result0 != []:
            time0 = result0[0]
            # print(time0)
            return time0, line
        else:
            if  line<len(linesdata):
                return t1(m, line + 1)
    result1=t1(m_aicloud_end,line)
    time1=result1[0]
    print("time1:%s"%time1)
    result2 = t1(m_cloud_speech_trans_ack, result1[1])
    time2=result2[0]
    print("time2:%s" % time2)
    result3 = t1(m_parse_speech_reply_to_tts, result2[1])
    time3 = result3[0]
    print("time3:%s" % time3)
    result4 = t1(io_open_default, result3[1])
    time4 = result4[0]
    print("time4:%s" % time4)
    w_line+=1

line=0
while line<len(linesdata):
    a=ProcessLog(line,0)
    print(a)


