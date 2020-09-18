import  xlsxwriter
class WriteExcel:
    def __init__(self,path):
        self.wb = xlsxwriter.Workbook(path)
    def creattable(self,sheet_name):
        # self.wb.
        self.sheet=self.wb.add_worksheet(sheet_name)
    def write_onlydata(self,row,col,vale):
        self.sheet.write(row,col,vale)
    def write_linedata(self,row,list_data,start_col=None):
        if start_col is None:
            start_col=0
        for i in range(len(list_data)):
            self.write_onlydata(row,i+start_col,list_data[i])
    def close(self,):
        self.wb.close()

if __name__=='__main__':
    path1 = 'E:\AITEST\TestResult\\test5.xls'
    w = WriteExcel(path1)
    a=['112','113','114','115']
    b='test'
    w.creattable(b)
    w.write_linedata(1,a,start_col=2)
    w.close()
    # for i in range(len(a)):
    #     w.write_onlydata(i,i,a[i])

