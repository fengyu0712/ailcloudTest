import xlrd,os,lockfile
from xlutils.copy import copy
from demo.redis import RedisLock1
import Project_path


class Read_xls():
    def __init__(self,filepath):
        # redis_conn = redis.Redis(host='111.231.233.115', port=6379, password="071211", db=redis_case)
        self.filepath=filepath
        self.workbook = xlrd.open_workbook(filepath)
        # self.file_lock = lockfile.LockFile(filepath)
    def get_sheet_names(self):
        sheet_names=self.workbook.sheet_names()
        return sheet_names
    def read_data(self,bookname=None,start_line=None):  #start_line 数据起止行
        if start_line==None:
            start_line=1
        if bookname==None:
            bookname=self.get_sheet_names()[0]
        result=[]
        shell_obj = self.workbook.sheet_by_name(bookname)
        nrow=shell_obj.nrows
        indexe=start_line-1
        for i in  range(indexe,nrow):
            row_value = shell_obj.row_values(i)
            row_values = []
            for each in row_value:
                if isinstance(each, float):
                    each = int(each)
                else:
                    each = each
                row_values.append(each)
            result.append(row_values)
        return result
    def read_cellvalue(self,row,col,bookname=None):   #row  行  col 列
        if bookname==None:
            bookname=self.get_sheet_names()[0]
        shell_obj = self.workbook.sheet_by_name(bookname)
        result=shell_obj.cell_value(row,col)
        return result
    def read_rowvalues(self,row,bookname=None,start_colx=None, end_colx=None):
        if bookname==None:
            bookname=self.get_sheet_names()[0]
        if start_colx==None:
            start_colx=0
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
    def write_onlydata(self,sheet,row,col,value,sheetname=None):
        if sheetname==None:
            index=0
        else:
            index=self.get_sheet_names().index(sheetname)
        w = sheet.get_sheet(index)
        # self.file_lock.acquire()
        w.write(row,col,value)
    # def write_linedata(self,sheet,row,list_data,sheetname=None):
    #     if sheetname == None:
    #         sheetname = self.get_sheet_names()[0]
    #     for i in range(len(list_data)):
    #         self.write_onlydata(sheet,row,i,list_data[i],sheetname)

    def save_write(self,w,new_path):
        try:
            w.save(new_path)
        except:
            os.makedirs(os.path.dirname(new_path))
            w.save(new_path)
            self.file_lock.release()
    def write_onlydata_new(self,sheet,row,col,value,new_path,sheetname=None):
        if sheetname==None:
            index=0
        else:
            index=self.get_sheet_names().index(sheetname)
        w = sheet.get_sheet(index)
        w.write(row,col,value)
        sheet.save(new_path)

    def write_new(self,sheet,row,col,value,sheetname=None):
        if sheetname==None:
            index=0
        else:
            index=self.get_sheet_names().index(sheetname)
        w = sheet.get_sheet(index)
        self.identifier = RedisLock1.acquire_lock('filepath')
        w.write(row,col,value)
    def save_write_new(self,w,new_path):
        try:
            w.save(new_path)
        except:
            os.makedirs(os.path.dirname(new_path))
            w.save(new_path)

if __name__=="__main__":

    # test_data = Project_path.TestData_path + "Test_data.xls"
    # r=Read_xls(test_data)
    # a = r.read_data()
    # print(a)
    # a=r.get_workbook()
    # for each in a:
    #     bookname=each
    #     b=r.read_data(bookname,redis_case)
    #     print(b)
    test_data_path = Project_path.TestData_path + "空调远程控制-自动化案例.xls"
    result2 = Project_path.TestData_path + "\\1111\\result.xlsx"
    result= Project_path.TestData_path + "result.xlsx"
    r = Read_xls(test_data_path)
    a=r.read_rowvalues(0,bookname="HB")
    print(a)
    w=r.copy_book()
    r.write_onlydata_new(w, 7, 5,"redis_case",result)
    r.save_write(w,result2)







