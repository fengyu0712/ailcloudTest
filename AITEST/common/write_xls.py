import  xlwt,os
class WriteExcel:
    def __init__(self):
        self.wb = xlwt.Workbook()
    def creattable(self,sheet_name,cell_overwrite=None):
        if cell_overwrite==None:
            cell_overwrite=True
        sheet=self.wb.add_sheet(sheet_name,cell_overwrite_ok=cell_overwrite)
        return sheet
       # 此处的cell_overwrite_ok = True是为了能对同一个单元格重复操作。
    def write_onlydata(self,row,col,vale,sheet):
        sheet.write(row,col,vale)
    def write_linedata(self,row,list_data,sheet):
        for i in range(len(list_data)):
            self.write_onlydata(row,i,list_data[i],sheet)
    def save_excel(self,path):
        try:
            self.wb.save(path)
        except:
            os.makedirs(os.path.dirname(path))
            self.wb.save(path)


if __name__=='__main__':
    w=WriteExcel()
    path1 = 'D:/1111/test5.xls'
    a=['112','113','114','115']
    b='test'
    sheet=w.creattable(b)
    w.write_linedata(1,a,sheet)
    # for i in range(len(a)):
    #     w.write_onlydata(i,i,a[i])
    w.save_excel(path1)
