#coding=utf-8
from Crypto.Cipher import _DES3         #加密解密方法
import base64,re
BS = _DES3.block_size
import json
import requests
def pad(s):
    return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
#定义 padding 即 填充 为PKCS7

def unpad(s):
    return s[0:-ord(s[-1])]

class prpcrypt():
    def __init__(self, key):
        self.key = key
        self.mode = _DES3.MODE_CBC
        self.iv  = IV
    # DES3的加密模式为CBC
    def encrypt(self, text):
        text = pad(text)
        cryptor = _DES3.new(self.key, self.mode, self.iv)
        #self.iv 为 IV 即偏移量
        x = len(text) % 8
        if x != 0:
            text = text + '\0' * (8 - x)  # 不满16，32，64位补0
        # print(text)
        self.ciphertext = cryptor.encrypt(text)
        return base64.standard_b64encode(self.ciphertext).decode("utf-8")

    def decrypt(self, text):
        cryptor = _DES3.new(self.key, self.mode, self.iv)
        de_text = base64.standard_b64decode(text)
        plain_text = cryptor.decrypt(de_text)
        # st = str(plain_text.decode("utf-8")).rstrip('\0')         
        # out = unpad(st)
        # return out
        #上面注释内容解密如果运行报错，就注释掉试试
        return plain_text
if __name__ == '__main__':
    iv = "******"       #IV偏移量
    pc = prpcrypt('******')  # 自己设定的密钥
    message = {"ARRAYDATA":
                  {"FACILITYID":"","FACILITYNAME":"","FACILITYTYPE":"","PASSWORD":"***","USERNO":"***"},
                "TOKEN":"***",}

    js = json.dumps(message) #字典转str，再加密
    print (type(js))
    e = pc.encrypt(js)  # 加密内容
    d = pc.decrypt(e)   #解密内容
    print (e)             #加密后
    print (d)             #解密后
    url = "***"
    header = {"Content-Type":"application/x-www-form-urlencoded",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/3.8.0"}
    message1 ={"message":e}
    r = requests.post(url,headers=header,data=message1)

    text1 = r.text
    print (text1)
    d1 = pc.decrypt(text1)
    print(d1)

    r = re.findall('\{(.+)\}',d1)        #取值，对于返回值后面带有特殊字符，如空格、\等
    d = eval("{"+r[0]+"}")              #str转化成字典
    token =  d["ARRAYDATA"]["TOKEN"]    #字典取值
    print(token)