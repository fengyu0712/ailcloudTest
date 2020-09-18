import websocket,time,json
from websocket import ABNF
from common.log import Logger
from common.conf import Conf
import Project_path
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
conf_path= Project_path.conf_path
data0=Conf(conf_path+"/ws.ini").get_value("WS","content")




class WsSingle:
    def __init__(self,url):
        self.ws = websocket.create_connection(url)  # 创建连接
        Logger().info("WebSocket链接建立成功")
    # @pytest.mark.flaky(reruns=2, reruns_delay=redis_case)  # 重试机制
    def runsingle(self,wavfile,content=None,step=None):
        if content==None:
            content=eval(data0)
        if step==None:  # 如果audioType是wav，此处需要修改为3200
            step=3200
        self.ws.send(json.dumps(content))

        try:
            with open(wavfile, 'rb') as f:
                while True:
                    data = f.read(step)
                    if data:
                        # print(data)
                        self.ws.send(data, ABNF.OPCODE_BINARY)
                    if len(data) < step:
                        break
                    time.sleep(0.01)
        except Exception as e:
            Logger().error(e)
        else:
            self.ws.send('', ABNF.OPCODE_BINARY)
            result = self.ws.recv()
            return result
        # with open(wavfile, 'rb') as f:
        #     while True:
        #         data = f.read(step)
        #         if data:
        #             # print(data)
        #             self.ws.send(data, ABNF.OPCODE_BINARY)
        #         if len(data) < step:
        #             break
        #
        #         # time.sleep(0.redis_case)
        # self.ws.send('', ABNF.OPCODE_BINARY)
        # result=self.ws.recv()
        # return result
    def close(self):
        self.ws.close()
        Logger().info("WebSocket链接关闭")

# E:\AI_test\testdata\test_audio\002M30_36_010001.wav

wavfile1="E:\\AI_test\\testdata\\test_audio\\002M30_36_010001.wav"
wavfile2="E:\\AI_test\\testdata\\test_audio\\002M30_36_010002.wav"
if __name__ == "__main__":
    url = Conf(conf_path + "/ws.ini").get_value("WS", "url")
    ws=WsSingle(url)
    start = time.clock()
    a=ws.runsingle(wavfile1)
    b=ws.runsingle(wavfile2)
    time = time.clock() - start
    print(a, b,start, time)
    # ws.close()



