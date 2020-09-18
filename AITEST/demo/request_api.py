import requests, time
from requests import Timeout


class get_respone_data:
    def __init__(self, respone, q_data=None, **kwargs):
        self.respone = respone
        self.status_code = None
        self.cost_time = None
        self.text = None
        self.json = None
        self.respone_header = None
        self.respone_dict = None
        self.status = None
        self.q_data = q_data
        self.kwargs = kwargs
        self.url = None

    def exception_handler(self, request, exception):
        self.respone = request
        if isinstance(exception, Timeout):
            self.status_code = 504
            self.text = '请求超时！！'
        self.status = False
        self.respone_dict = {'status_codestatus_code': self.status_code,
                             'cost_time': self.cost_time,
                             'text': self.text,
                             'json': self.json,
                             'respone_header': self.respone_header,
                             'status': self.status

                             }
        print(self.respone_dict)

    def _make_data(self):
        q_data = self.kwargs['datas']
        q_data['respone'] = {}
        q_data['respone']['nlu'] = {}
        q_data['respone']['nlu']['data'] = self.json
        q_data['respone']['nlu']['status'] = self.status
        type = self.kwargs['title']
        self.q_data.put(q_data)

    def get_result(self, timeout=False, *args, **kwargs):
        if timeout:
            self.status = False
            self.status_code = 504
            self.text = '超时'
        else:
            self.respone.encoding = 'utf-8'
            self.status_code = self.respone.status_code
            self.cost_time = self.respone.elapsed
            self.status = self.respone.ok
            self.text = self.respone.text
            self.respone_header = self.respone.headers
            if self.status:
                self.json = self.respone.json()
        self.respone_dict = {'status_code': self.status_code,
                             'cost_time': self.cost_time,
                             'text': self.text,
                             'json': self.json,
                             'respone_header': self.respone_header,
                             'status': self.status

                             }
        if self.kwargs:
            if self.kwargs['title'] == 'Lua':
                print('%s - ID: %s Name:%s -->> URL：%s' % (
                    self.kwargs['title'], self.kwargs['id'], self.kwargs['name'],
                    requests.utils.unquote(self.respone.url)))
            # print('%s - ID: %s Name:%s -->> 响应时间为：%s秒' % (
            #     self.kwargs['title'], self.kwargs['id'], self.kwargs['name'], self.respone.elapsed.total_seconds()))
        return self


class api:
    def __init__(self, url, method, data=None, headers=None, callback=None, timeout=20, **kwargs):
        self.callback = callback
        self.session = requests.Session()
        self.kwargs = kwargs
        self.url = url
        self.data = data
        self.json_data = data
        self.headers = headers
        self.method = method
        self.time_out = timeout

    def _post(self):
        # print(self.json_data)
        if 'json' in self.headers['Content-Type']:
            respone = self.session.post(url=self.url, json=self.json_data, headers=self.headers, timeout=self.time_out,
                                        hooks={"response": self.callback})
        elif 'form-data' in self.headers['Content-Type']:
            respone = self.session.post(url=self.url, data=self.json_data, headers=self.headers, timeout=self.time_out,
                                        hooks={"response": self.callback})
        return respone

    def _get(self):
        response = self.session.get(url=self.url, headers=self.headers, params=self.data, timeout=self.time_out,
                                    hooks={"response": self.callback})
        return response

    def run(self):
        timeout = False
        for i in range(2):
            try:
                if self.method.upper() == 'POST':
                    # print()
                    self.respone = self._post()
                elif self.method.upper() == 'GET':
                    self.respone = self._get()
                if self.respone.ok:
                    break
                else:
                    time.sleep(1)
            except  Timeout:
                timeout = True
                print('%s - ID: %s Name:%s -->> 响应时间为：%s' % (
                    self.kwargs['title'], self.kwargs['id'], self.kwargs['name'], '超时'))
        return get_respone_data(self.respone, **self.kwargs).get_result(timeout)


def test_rasa_api(q):
    url2 = 'http://47.98.120.217:5005/model/parse'
    payload2 = {
        "text": q,
        "productModel": "YB101"
    }
    headers = {
        'Content-Type': "application/json;charset=utf-8"
    }
    print("rasa api:" + url2)
    sesion = api(url=url2, method='post', data=payload2, headers=headers, id='333', name='rasa', title='test')
    rs = sesion.run()
    # print(sesion.respone.json())
    return rs


def test_java_api(utterance="打开空调"):
    # url1 = "http://localhost:8080/three_scenarios/nlp/listen/nlu"
    url1 = "http://101.37.129.119:22012/three_scenarios/nlp/listen/nlu"
    payload1 = {
        "currentUtterance": utterance,
        "sourceDevice": "空调",
        "isSlotMissingThisRound": False,
        "clearDialogHistory": False,
        "userGroup": "nlp",
        "userGroupCredential": "11c19213-25ef-46d8-b863-e7603c7aa00e",
        "hideMetaData": True
    }
    headers = {
        'Content-Type': "application/json;charset=utf-8"
    }
    print("java api:" + url1)
    sesion = api(url=url1, method='post', data=payload1, headers=headers, id='333', name='java', title='test')
    rs = sesion.run()
    # print(sesion.respone.json())
    return rs


if __name__ == '__main__':
    print("-------------------rasa-------------------------")
    r1 = test_rasa_api("介绍下这款空调的亮点吧")
    c1 = float(str(r1.cost_time).split(":")[2])
    print("rasa costTime = %f ms" % c1)
    print("-------------------java-------------------------")
    r2 = test_java_api("介绍下这款空调的亮点吧")
    c2 = float(str(r2.cost_time).split(":")[2])
    print("java costTime = %f ms" % c2)
