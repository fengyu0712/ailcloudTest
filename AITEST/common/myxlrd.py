# import xlrd
from xlutils.copy import copy
import xlrd.sheet
import Project_path

class MyXlrd(xlrd.sheet.Sheet):
    def __init__(self,filename,position=None,name=None,number=None):
        super(MyXlrd, self).__init__(self,position,name,number)
        self.book=xlrd.open_workbook(filename)
        self.name=name

if __name__=="__main__":
    test_data_path = Project_path.TestData_path + "case.xlsx"
    r = MyXlrd(test_data_path)
    a = r.cell_value(1,1)
    print(a)