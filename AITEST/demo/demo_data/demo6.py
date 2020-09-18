from common.http_request_new import Request
import os

data={
    'text':"redis_case、制冷时，把设定温度升高1℃，制热时把设定温度降低2℃，可省电10％。2、制热时尽量少开电辅热功能。3、使用环境较恶劣的需要经常清洗空调过滤网及外机.4、房间需要有良好的隔热效果和密封性。5、变频空调需要使用时间越长，省电效果要比定频空调更明显。"
}
yuliao='''
redis_case、制冷时，把设定温度升高1℃，制热时把设定温度降低2℃，可省电10％。2、制热时尽量少开电辅热功能。3、使用环境较恶劣的需要经常清洗空调过滤网及外机.4、房间需要有良好的隔热效果和密封性。5、变频空调需要使用时间越长，省电效果要比定频空调更明显。
'''
# url="http://sit.aimidea.cn:11003/v1/orion/tts?text=%s"%yuliao
url="http://sit.aimidea.cn:11003/v1/orion/tts"
a=Request().requests(url,data,"get")
print(a)
b="start %s "%a
os.system(b)
