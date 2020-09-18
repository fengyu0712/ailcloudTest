import requests,json,pytest
from AITEST.Common.log import Logger
from  bs4 import BeautifulSoup


class Request():
    def __init__(self,host=None):
        self.Log=Logger()
        if host is None:
            self.host=''
        else:
            self.host=host
    # def request(self,url,data,type,h=None,c=None):
    #     if h==None:
    #         h = {"Content-Type": "application/json; charset=utf-8", }
    #     if c==None:
    #         c=""
    #     if type.upper()=="GET":
    #         self.Log.debug("正在进行【GET】请求")
    #         try:
    #             req=requests.get(url,data,hearder=h,cookies=c)
    #             result = req.json()
    #             # status_code=req.status_code
    #         except Exception as  e:
    #             self.Log.error(e)
    #         else:
    #         #     if status_code == 200:
    #         #         self.Log.info("请求完成【status:%s】"%status_code)
    #         #     else:
    #         #         self.Log.error("请求出错【status:%s】"%status_code)
    #             return result
    #     elif type.upper()=="POST":
    #         data=json.dumps(data)
    #         self.Log.debug("%s正在进行【POST】请求"%url)
    #         try:
    #             req=requests.post(url,data,hearder=h,cookies=c)
    #             result=req.json()
    #             # status_code = req.status_code
    #         except Exception as  e:
    #             self.Log.error(e)
    #         else:
    #         #     if status_code == 200:
    #         #         self.Log.info("请求完成【status:%s】"%status_code)
    #         #     else:
    #         #         self.Log.error("请求出错【status:%s】"%status_code)
    #             return result
    #     else:
    #         self.Log.error("请求类型错误")
    #     self.Log.close()
    # @pytest.mark.flaky(reruns=2, reruns_delay=1)  # 重试机制
    def requests(self,url,data,type,h=None,c=None):
        url=self.host+url
        if h==None:
            h = {"Content-Type": "application/json"}
            if c == None:
                c= ""
        if type.upper()=="GET":
            self.Log.debug("%s正在进行【GET】请求"%url)
            try:
                req=requests.get(url, params=data,headers=h,cookies=c)
                result = req.json()
                status_code=req.status_code
            except Exception as  e:
                self.Log.error(e)
            else:
                if status_code == 200:
                    self.Log.info("%s请求成功"%url)
                else:
                    self.Log.error("请求出错【status:%s】"%status_code)
                return result
        elif type.upper()=="POST":
            self.Log.debug("%s正在进行【POST】请求"%url)
            try:
                req=requests.post(url,data=json.dumps(data),headers=h,cookies=c)
                result=req.json()
                status_code = req.status_code
            except Exception as  e:
                self.Log.error(e)
            else:
                if status_code == 200:
                    self.Log.info("%s请求成功" % url)
                else:
                    self.Log.error("请求出错【status:%s】" % status_code)
                return result
        else:
            self.Log.error("请求类型错误")

if __name__=="__main__":
    # url = "http://sit.aimidea.cn:11003/v1/nlu"
    url="http://bkt.jeagine.com/api/user/signin"
    # host="http://bkt.jeagine.com"
    # url="/api/user/signin"
    # data = {"currentUtterance":"你好","sourceDevice":"","multiDialog":"false","slotMiss":"false","suite":"default","deviceId":"5672644312938899","userGroup":"meiju","userGroupCredential":"b82063f4-d39b-4940-91c3-5b67d741b4d3"}
    data={'account': '13017600000', 'appKey': 'all', 'category_id': 80, 'password': '123456', 'terminal': 2}
    result = Request().requests(url,data,"get")
    print(result,type(result))


