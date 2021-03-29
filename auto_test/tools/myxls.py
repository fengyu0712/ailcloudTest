import xlrd, os
import xlwt
from xlutils.copy import copy

from tools.file_tool import FileTool


class Read_xls():
    def __init__(self, filepath):
        self.filepath = filepath
        self.workbook = xlrd.open_workbook(filepath)

    def get_sheet_names(self):
        sheet_names = self.workbook.sheet_names()
        return sheet_names

    def read_data(self, sheetname=None, start_line=None, is_addsheetname=False):  # start_line 数据起止行
        if start_line == None:
            start_line = 1
        if sheetname == None:
            sheetname = self.get_sheet_names()[0]

        result = []
        shell_obj = self.workbook.sheet_by_name(sheetname)
        nrow = shell_obj.nrows
        indexe = start_line - 1
        for i in range(indexe, nrow):
            row_values = shell_obj.row_values(i)
            if is_addsheetname == True:
                row_values.append(sheetname)
            result.append(row_values)
        return result

    def read_cellvalue(self, row, col, bookname=None):  # row  行  col 列
        if bookname == None:
            bookname = self.get_sheet_names()[0]
        shell_obj = self.workbook.sheet_by_name(bookname)
        result = shell_obj.cell_value(row, col)
        return result

    def read_rowvalues(self, row, bookname=None, start_colx=None, end_colx=None):
        if bookname == None:
            bookname = self.get_sheet_names()[0]
        if start_colx == None:
            start_colx = 0
        shell_obj = self.workbook.sheet_by_name(bookname)
        result = shell_obj.row_values(row, start_colx, end_colx)
        return result

    def read_colvalues(self, col, bookname=None, start_rowx=None, end_rowx=None):
        if bookname == None:
            bookname = self.get_sheet_names()[0]
        if start_rowx == None:
            start_rowx = 0
        shell_obj = self.workbook.sheet_by_name(bookname)
        result = shell_obj.col_values(col, start_rowx, end_rowx)
        return result

    def copy_book(self):
        sheet = copy(self.workbook)
        return sheet

    def write_onlydata(self, sheet, row, col, value, sheetname=None):
        if sheetname == None:
            index = 0
        else:
            index = self.get_sheet_names().index(sheetname)
        w = sheet.get_sheet(index)
        # self.file_lock.acquire()
        w.write(row, col, value)

    def write_linedata(self, sheet, row, list_data, sheetname=None):
        if sheetname == None:
            sheetname = self.get_sheet_names()[0]
        for i in range(len(list_data)):
            self.write_onlydata(sheet, row, i, list_data[i], sheetname)

    def save_write(self, w, new_path):
        try:
            w.save(new_path)
        except:
            os.makedirs(os.path.dirname(new_path))
            w.save(new_path)

    def write_onlydata_new(self, sheet, row, col, value, new_path, sheetname=None):
        if sheetname == None:
            index = 0
        else:
            index = self.get_sheet_names().index(sheetname)
        w = sheet.get_sheet(index)
        w.write(row, col, value)
        sheet.save(new_path)

    def write_new(self, sheet, row, col, value, sheetname=None):
        if sheetname == None:
            index = 0
        else:
            index = self.get_sheet_names().index(sheetname)
        w = sheet.get_sheet(index)
        w.write(row, col, value)

    def save_write_new(self, w, new_path):
        try:
            w.save(new_path)
        except:
            os.makedirs(os.path.dirname(new_path))
            w.save(new_path)


class Write_xls:
    def __init__(self):
        self.wb = xlwt.Workbook()

    def creattable(self, sheet_name=None):
        if sheet_name == None:
            sheet_name = "sheet1"
        self.sheet = self.wb.add_sheet(sheet_name, cell_overwrite_ok=True)
        return self.sheet

    def write_onlydata(self, row, col, vale):
        self.sheet.write(row, col, str(vale))

    def write_linedata(self, row, list_data):
        for i in range(len(list_data)):
            self.write_onlydata(row, i, list_data[i])

    def save_excel(self, path):
        self.wb.save(path)


if __name__ == "__main__":

    # test_data = Project_path.TestData_path + "Test_data.xls"
    # r=Read_xls(test_data)
    # a = r.read_data()
    # print(a)
    # a=r.get_workbook()
    # for each in a:
    #     bookname=each
    #     b=r.read_data(bookname,redis_case)
    #     print(b)
    test_data_path = r"F:\git\Midea\auto_test\result\sit_TestResult_2021-03-25.xls"
    # result2 = Project_path.TestData_path + "\\1111\\result.xlsx"
    # result= Project_path.TestData_path + "result.xlsx"
    r = Read_xls(test_data_path)
    sheet_names = r.get_sheet_names()
    all_caseinfo = list()
    for devicetype in sheet_names:
        data = r.read_data(start_line=2, sheetname=devicetype, is_addsheetname=True)
        dict_data = FileTool().dict_info(data, devicetype=devicetype)
        all_caseinfo += dict_data
    print(all_caseinfo)
    # a=r.read_rowvalues(0,bookname="HB")
    # print(a)
    w = r.copy_book()
    data = "{'case_category': 'Public', 'case_id': 'public_001', 'case_name': '音乐技能', 'lock_device': '', 'steps': [{'is_wait': '', 'step': '发送“来一首歌”', 'params': '来一首歌', 'result': '控制完成', 'response': {'result': {'returnData': {'mid': '3100ef548dd311ebb68a98e7f4f1e716', 'code': 200, 'message': '', 'data': {'isMideaDomain': False, 'class': 'tts', 'endSession': True, 'isNlpFilter': False, 'tts': {'data': [{'text': '这句话什么意思，真心不懂', 'url': '', 'seq': 0}], 'type': 'Sort'}}}}, 'errorCode': '0'}}, {'is_wait': '', 'step': '校验-状态是否正确', 'params': {'nlg': {'isMideaDomain': False, 'errorCode': '0'}}, 'result': '执行通过'}], 'devicetype': 'meiju', 'index': 1}"
    # r.write_onlydata_new(w, 7, 5,"redis_case",result)
    # r.save_write(w,result2)
