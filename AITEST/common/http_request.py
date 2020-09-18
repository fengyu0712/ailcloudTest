import requests
from common.log import Logger
from  bs4 import BeautifulSoup


class Request:
    def __init__(self,host):
        self.host=host
        self.Log=Logger()
    def request(self,url,data,type):
        url=self.host+url
        if type.upper()=="GET":
            try:
                self.Log.info("正在进GET：【%s】接口"%url)
                req=requests.get(url, params=data)
                result = req.json()
                status_code=req.status_code
            except Exception as  e:
                self.Log.error(e)
            else:
                if status_code == 200:
                    self.Log.info("请求完成【status:%s】"%status_code)
                else:
                    self.Log.error("请求出错【status:%s】"%status_code)
                return result
        elif type.upper()=="POST":
            try:
                self.Log.info("正在进POST：【%s】接口" % url)
                req=requests.post(url,data=data)
                result=req.json()
                status_code = req(url, data)
            except Exception as  e:
                self.Log.error(e)
            else:
                if status_code == 200:
                    self.Log.info("请求完成【status:%s】"%status_code)
                else:
                    self.Log.error("请求出错【status:%s】"%status_code)
                return result
        else:
            self.Log.error("请求类型错误")
        self.Log.close()
    def requests(self,url,data,type):
        url=self.host+url
        if type.upper()=="GET":
            try:
                self.Log.info("正在进GET：【%s】接口" % url)
                req=requests.get(url, params=data)
                result = req.text
                status_code=req.status_code
            except Exception as  e:
                self.Log.error(e)
            else:
                if status_code == 200:
                    self.Log.info("请求完成【status:%s】"%status_code)
                else:
                    self.Log.error("请求出错【status:%s】"%status_code)
                return result
        elif type.upper()=="POST":
            try:
                self.Log.info("正在进POST：【%s】接口" % url)
                result=requests.post(url,data=data).json()
                status_code = requests.post(url, data)
            except Exception as  e:
                self.Log.error(e)
            else:
                if status_code == 200:
                    self.Log.info("请求完成【status:%s】"%status_code)
                else:
                    self.Log.error("请求出错【status:%s】"%status_code)
                return result
        else:
            self.Log.error("请求类型错误")
        self.Log.close()


if __name__=="__main__":
    # host = "http://bkt.jeagine.com"
    # url="/api/user/signin"
    # data={'appKey': 'all', 'terminal': 2, 'account': 13000000000, 'category_id': 80, 'password': 123456}

    host='http://linksit.aimidea.cn:10000'
    url='/cloud/connect'
    data={
    "topic": "cloud.connect",
    "mid": "6aad0b12-2192-4b90-8f40-08a2bc0b5c2a",
    "version": "redis_case.0",
    "request": {
        "apiVer": "redis_case.0.0",
        "timestamp": 1234567890,
        "pki":"fndjsafhop3u8rheowfh"
    },
    "params": {
        "sn": "0000DB11138104887174101101740000",
        "category": "0xDB",
        "model": "123",
        "id": "23454365465643",
        "ip": "0.0.0.0",
        "mac": "88e9fe5d3829",
        "random": "545623"
    }
}

    a=Request(host).requests(url,data,"post")
    print(a)


