import re
_MAPPING = (u'零', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九', u'十', u'十一', u'十二', u'十三', u'十四', u'十五', u'十六', u'十七',u'十八', u'十九')
_P0 = (u'', u'十', u'百', u'千',)
_S4 = 10 ** 4

def _to_chinese4(string):
    a=re.findall(r"\d+\.?\d*", string)[0]
    num=int(a)
    print(a)
    assert (0 <= num and num < _S4)
    if num < 20:
        result= _MAPPING[num]
    else:
        lst = []
        while num >= 10:
            lst.append(num % 10)
            num = num / 10
        lst.append(num)
        c = len(lst)  # 位数
        result = u''

        for idx, val in enumerate(lst):
            val = int(val)
            if val != 0:
                result += _P0[idx] + _MAPPING[val]
                if idx < c - 1 and lst[idx + 1] == 0:
                    result += u'零'
    r=string.replace(str(a),result)
    # print(r)
    return r

a=_to_chinese4('27度')
print(a)