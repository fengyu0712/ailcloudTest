import re
from collections import Counter


class ReplaceCharacter():
    def __init__(self):
        self.CN_NUM = {
            u'〇': 0,
            u'一': 1,
            u'二': 2,
            u'三': 3,
            u'四': 4,
            u'五': 5,
            u'六': 6,
            u'七': 7,
            u'八': 8,
            u'九': 9,

            u'零': 0,
            u'壹': 1,
            u'贰': 2,
            u'叁': 3,
            u'肆': 4,
            u'伍': 5,
            u'柒': 7,
            u'捌': 8,
            u'玖': 9,

            u'貮': 2,
            u'两': 2,
        }
        self.CN_UNIT = {
            u'十': 10,
            u'拾': 10,
            u'百': 100,
            u'佰': 100,
            u'千': 1000,
            u'仟': 1000,
            u'万': 10000,
            u'萬': 10000,
            u'亿': 100000000,
            u'億': 100000000,
            u'兆': 1000000000000,
        }

    def cn2dig(self, cn):
        try:

            if cn is None:
                return ""
            cn = cn.replace("\n", "") + " "
            # 截取字符
            lcn = list(cn)
            suffix_value = "".join(lcn[0:3])
            is_suffix = False
            if suffix_value in ["来一首", "来一段", "来一段"]:
                lcn = lcn[3::]
                is_suffix = True
            # print(lcn)

            remark = False
            alldata = []  # 临时数组
            for cndig in lcn:
                tempvalue = cndig
                # print(tempvalue)
                if tempvalue in self.CN_UNIT:
                    remark = True
                    # print("当前的",alldata)
                    if len(alldata) != 0:
                        lastvalue = alldata[-1]
                        # print(lastvalue)
                        if isinstance(lastvalue, int):
                            alldata[-1] = lastvalue * self.CN_UNIT[tempvalue]
                        else:
                            alldata.append(self.CN_UNIT[tempvalue])
                    else:
                        alldata.append(self.CN_UNIT[tempvalue])

                    continue

                if cndig in self.CN_NUM:
                    tempvalue = self.CN_NUM[cndig]

                alldata.append(tempvalue)

            count_value = 0
            return_value = ""
            unit = 0
            for i in range(0, len(alldata)):
                index_value = alldata[i]
                unit = 0
                if remark and isinstance(index_value, int):
                    count_value = count_value + index_value
                    unit = 1
                if unit == 0:
                    if count_value != 0:
                        return_value = return_value + str(count_value) + index_value
                        count_value = 0
                    else:
                        return_value = return_value + str(index_value)
            if is_suffix:
                return_value = suffix_value + return_value

            # print("********",return_value)
            if return_value.find("100分之") != -1:
                a = re.compile("(.*)(100分之\d+)(.*)")
                c = a.findall(return_value)
                # print(c)
                whole_value = ""
                for c_value in c[0]:
                    if c_value.find("100分之") != -1:
                        c_value = c_value.replace("100分之", "") + "%"

                    whole_value = whole_value + c_value

                return_value = whole_value

            elif return_value.find("点") != -1:
                a = re.compile("\d+点\d+")
                c = a.findall(return_value)
                if len(c) > 0:
                    for current_index in range(len(c)):
                        replace_value = str(c[current_index]).replace("点", ".")
                        return_value = return_value.replace(c[current_index], replace_value)

            reg = "[\,|\，]"
            return_value = re.sub(reg, '', return_value)
            return return_value.strip().replace(" ", "")
        except Exception as e:
            print("替换字符串出错", e, cn)
            return cn
            # raise
    def _assert(self, expect, value):
        if expect == value:
            return True
        else:
            return False
    def Number2Text(self,text):
        text = self.cn2dig(text)
        # print(text)
        return text

if __name__ == '__main__':
    import xlrd
    import openpyxl
    ws=openpyxl.Workbook()
    ws_sheet=ws.create_sheet('result',-1)
    ta=xlrd.open_workbook(r'D:\MyData\ex_kangyong\Desktop\reuslt_finally.xlsx')
    sheet=ta.sheet_by_name('Sheet')
    num=sheet.nrows
    n2t=ReplaceCharacter()
    for i in range(num):
        data = sheet.row_values(i)
        if i==0:
            ws_sheet.append(data)
            continue
        result= Counter([n2t.Number2Text(data[1]),n2t.Number2Text(data[2]),n2t.Number2Text(data[2])])
        items=list(result.items())
        text=''
        if len(items) == 1:
            key=items[0][0]
            if key:
                text = '完全相同非空'
            else:
                text='完全相同空值'
        elif len(items) == 2:
            key = items[0][0]
            value = items[0][1]
            key1 = items[1][0]
            value1 = items[1][1]
            max_key=''
            if value > value1:
                max_key=key
            else:
                max_key = key1
            if max_key:
                text = '有两个相同且不为空'
            else:
                text = '有两个相同的空值'
        elif len(items) == 3:
            text = '完全不相同'




        ws_sheet.append([n2t.Number2Text(data[0]),n2t.Number2Text(data[1]),n2t.Number2Text(data[2]),n2t.Number2Text(data[2]),text])
    ws.save(r'D:\MyData\ex_kangyong\Desktop\reuslt_finally_2.2_1.xlsx')


