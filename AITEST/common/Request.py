import  requests
from common.Parsejson import ParseJson
import json
class Request():
    def get_request(self,url,header,data):
        pass

    def post_request(self,url,jsondata,header=None):
            if header is None:
                response = requests.post(url=url, json=jsondata)
            else:
                response = requests.post(url=url, json=jsondata, headers=header)

            dict={}
            retun_content=json.loads(response.content.decode("utf-8",errors="ignore"))
            print(retun_content)
            ttsvalue=retun_content['data']['tts']
            ttstext=ttsvalue['data'][0]["text"]
            dict["tts"]=ttstext
            dict["nlu"] = retun_content['data']['nlu']
            extraData_value= retun_content['data']['extraData']
            dict["luaData"]=""
            if extraData_value!=None and extraData_value !="None" :
                dict["luaData"] = extraData_value['luaData']
            return dict


