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
        text = self.cn2dig(text).lower()
        # print(text)
        return self.otherReplace(text)
    def otherReplace(self,text):
        if '+' in text:
            text=text.replace("+", "加")
        if '-' in text:
            text=text.replace("-", "减")
        if '×' in text:
            text=text.replace("×", "乘")
        if '÷' in text:
            text=text.replace("÷", "除以")
        if '=' in text:
            text = text.replace("=", "等于")

        if '/' in text:
            a = re.compile("\d+/\d+")
            c = a.findall(text)
            for i in c:
                t=i.split('/')
                text = text.replace(i, "{}分之{}".format(t[1],t[0]))
        if ':' in text:
                a = re.compile("\d+:\d+")
                c = a.findall(text)
                for i in c:
                    t=i.split(':')
                    if t[1] == '00':
                        text = text.replace(i, t[0]+'点')
                    else:
                        text = text.replace(i, i.replace(':','.'))
        if '.' in text :
            a1 = re.compile("\d+.\d+分")
            c = a1.findall(text)
            for i in c:
                    text = text.replace(i, i.replace('分', ''))
        if '点钟' in text :
            a1 = re.compile("\d+点钟+")
            c = a1.findall(text)
            for i in c:
                text = text.replace(i, i.replace('钟', ''))
        return text

if __name__ == '__main__':

    n2t=ReplaceCharacter()
    d=n2t.otherReplace('订3:00的闹钟')
    print(d)
    d=n2t.otherReplace('定1个2:50的闹钟')
    print(d)
    d=n2t.otherReplace('999+99等于多少')

    print(d)
    d = n2t.otherReplace('明天早上7:00')
    print(d)
    d = n2t.otherReplace('14-3+2等于几')
    print(d)
    d = n2t.otherReplace('不是晚上8:20闹钟上午8:22')
    print(d)
    d = n2t.otherReplace('明天上午6:40叫我起床')
    print(d)
    d = n2t.otherReplace('13.32分的时候提醒我')
    print(d)
    d = n2t.otherReplace('下午5点钟提醒我')
    print(d)
    d = n2t.otherReplace('下午5:00提醒我')
    print(d)
    # a = re.compile("\d+.\d+分")
    # c = a.findall('13.32分的时候提醒我')
    # print(c)




