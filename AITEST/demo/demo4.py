from common.http_request_new import Request
from common.m_process import mprocess
import json
path="D:\\Users\\lijq36\Desktop\\2"
result_path="E:\\test\\Result.txt"



def nlu(each):
    url = "https://nlu.sit.aimidea.cn:22012/nlu/v1"
    data = {"currentUtterance": "这款空调有什么特色", "sourceDevice": "空调", "multiDialog": "false", "slotMiss": "false",
            "suites": ["default"], "deviceId": "3141482994683870", "userGroup": "meiju",
            "userGroupCredential": "b82063f4-d39b-4940-91c3-5b67d741b4d3"}
    data["currentUtterance"] = each
    result = Request().requests(url, data, 'post')
    result = result.json()
    classifier = result['classifier']
    if classifier != "publicDomain":
        print(each + ":"+classifier)
        with open(result_path, 'a', encoding='utf8') as f:
            f.write(each+":"+str(result)+'\n')
            # f.close()
    else:
        print(each + ":"+classifier)


if __name__=="__main__":
    path1 = "D:\\Users\\lijq36\Desktop\\2"
    with open(path1, 'r', encoding='utf8') as f:
        a = f.readlines()
    for i in range(len(a)):
        nlu(a[i].replace("\n",""))
    # mprocess(nlu, a,Poolnum=1)

    #
