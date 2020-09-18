import requests,json,pytest
from common.log import Logger
# from  bs4 import BeautifulSoup
import urllib3

class Request():
    def __init__(self,host=None):
        if host is None:
            self.host=''
        else:
            self.host=host
    # @pytest.mark.flaky(reruns=2, reruns_delay=redis_case)  # 重试机制
    def requests(self,url,data,type,headers=None,cookies=None):
        url=self.host+url
        if headers==None and type.upper()=="POST":
            headers = {"Content-Type": "application/json"}
        if cookies == None:
            cookies= ""
        if type.upper()=="GET":
            Logger().debug(u"%s正在进行【GET】请求"%url)
            Logger().debug("body:" + str(data))
            try:
                urllib3.disable_warnings()
                response=requests.get(url, params=data,headers=headers,cookies=cookies,verify=False)  #https verify=False
                status_code=response.status_code
            except Exception as  e:
                Logger().error(e)
            else:
                if status_code == 200:
                    Logger().info(u"%s请求成功"%url)
                else:
                    Logger().error("请求出错【status:%s】"%status_code)
                Logger().debug("response:" + response.text)
                return  response
        elif type.upper()=="POST":
            Logger().debug(u"%s正在进行【POST】请求"%url)
            Logger().debug("body:" + str(data))
            try:
                urllib3.disable_warnings()
                response=requests.post(url,data=json.dumps(data),headers=headers,cookies=cookies,verify=False)    #https verify=False
                status_code = response.status_code
            except Exception as  e:
                Logger().error(e)
            else:
                if status_code == 200:
                    pass
                    Logger().info(u"%s请求成功" % url)
                else:
                    Logger().error(u"请求出错【status:%s】" % status_code)
                Logger().debug("response:" + response.text)
                return response
        else:
            Logger().error(u"请求类型错误")

if __name__=="__main__":
    # url = "https://nlu.sit.aimidea.cn:22012/nlu/v1"
    url="http://sit.aimidea.cn:11003/v1/orion/tts"
    # data={
	# "currentUtterance": "打开空调",
	# "sourceDevice": "空调",
	# "multiDialog": "true",
	# "slotMiss": "true",
	# "suites": ["default"],
	# "deviceId": "1295234709638064",
	# "userGroup": "meiju",
	# "userGroupCredential": "b82063f4-d39b-4940-91c3-5b67d741b4d3"
    # }
    data="{'text':'现在几点'}"
    response = Request().requests(url,data,"get")
    print(response.text,type(response))



