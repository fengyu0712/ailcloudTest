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

logpath = r"E:/log/1.txt"
# logpath="E:/log/rk3308.log"
result_path = 'E:/log/1.xls'
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


def ProcessLog(line=None, n=None, w_line=None):
    # print("========================================")
    if line == None:
        line = 0
    if n == None:
        n = 0
    if w_line == None:
        w_line = 0
    time0 = re.findall(list[0], linesdata[line])
    if len(time0) == 1 or n == 8:
        n = 0
    if len(time0) == 1:
        w_line += 1
        print(w_line)
    time1 = re.findall(list[n], linesdata[line])
    if time1 == []:
        if line + 1 < len(linesdata):
            line += 1
            ProcessLog(line, n, w_line)
    else:
        print(line, n, linesdata[line])
        w.write_onlydata(w_line, n, time1[0])
        if line + 1 < len(linesdata):
            line += 1
            n += 1
            ProcessLog(line, n, w_line)
    if line==len(linesdata):
        w.close()
ProcessLog()
w.close()
