# 读取和写入excel文件
import pandas as pd
import openpyxl
class DealExcel():
    def __init__(self,path,excelname):
        self.excelPath=path
        self.excel_name=excelname

    def read_excel(self):
       excelobj= pd.read_excel(self.excelPath,sheet_name=self.excel_name)
       list=[]
       for row in excelobj.itertuples(index=True,name="Pandas"):
           tuplelist=(getattr(row, "用例ID"),eval(getattr(row, "前置状态")),
                      getattr(row, "命令"),getattr(row, "预期结果_nlu"),getattr(row, "预期结果_tts"),
                      getattr(row, "预期结果_luaResponse"))
           list.append(tuplelist)
       return list


    def write_excel(self,dictinfo):
        wb = openpyxl.Workbook()
        ws = wb.create_sheet(self.excel_name)
        for i in dictinfo:
            print("***********************************************")
            keyvalue=dictinfo[i]
            print(keyvalue)
            ws.append(keyvalue)

        wb.save(self.excelPath)

if __name__=="__main__":
    d=DealExcel("E:/project/pytest+request/test_data/空调.xlsx","空调")
    d.read_excel("空调")