import json
import os
import time
from threading import Thread
#
# from Crypto.Cipher import AES
# from binascii import b2a_hex, a2b_hex
#
#
# class EncryptStr(object):
#     def __init__(self, key):
#         self.key = key
#         self.mode = AES.MODE_CBC
#
#     def encrypt(self, text):
#         cryptor = AES.new(self.key, self.mode, self.key)
#         length = 16
#         count = len(text)
#         if (count % length != 0):
#             add = length - (count % length)
#         else:
#             add = 0
#         text = text + ('\0' * add)
#         self.ciphertext = cryptor.encrypt(text)
#         return b2a_hex(self.ciphertext)
#
#     # 解密后，去掉补足的空格用strip() 去掉
#     def decrypt(self, text):
#         cryptor = AES.new(self.key, self.mode, self.key)
#         plain_text = cryptor.decrypt(a2b_hex(text))
#         return plain_text.decode('utf-8').strip('\0')
#

class AsrRun(Thread):
    def __init__(self, runinfo, wav_rootpath,redis, uid):
        super(AsrRun, self).__init__()
        self.wav_rootpath = wav_rootpath
        self.runinfo = runinfo
        self.redis = redis
        self.uid = uid

    def AsrfFun(self,runinfo,whole_wavpath,logpath=None):
        return {}

    def run(self):
        path = os.path.dirname(os.path.realpath(__file__))
        currentdir = os.path.join(path, 'OrionLog')
        while True:
            data = self.redis.redis_get_case(self.uid)
            res = {}
            notes = None
            if data == 'over':
                break
            if data:
                try:
                    data = json.loads(data)
                    data['expect'] = data['dict_assert']['expect']
                    del data['dict_assert']
                    whole_wavpath = self.wav_rootpath + "/" + data['file'] + '/' + data['sheet'] + '/' + data[
                        'filename']
                    if os.path.exists(whole_wavpath):
                        logpath = os.path.join(currentdir, data['sheet'] + '_{}'.format(self.runinfo['report_id']))
                        print(data)
                        for i in range(5):
                            try:
                                res = self.AsrfFun(self.runinfo, whole_wavpath, logpath)
                                print('res:', res)
                            except Exception:
                                time.sleep(1)
                                continue
                            else:
                                if res:
                                    break

                    else:
                        res = None
                        notes = '路径："{}"文件不存在'.format(whole_wavpath)
                except Exception as e:
                    time.sleep(1)
                    res = None
                    notes = e
                    # errlog.error(str(e))
                    raise
                finally:
                    # log.info('res:'+str(res))
                    if res:
                        self.redis.redis_put_result(self.uid,dict(data, **res))
                        # redis.que_put_message(self.runinfo['resQueueName'], dict(data, **res))
                    else:
                        data['notes'] = str(notes)
                        # redis.que_put_message(self.runinfo['resQueueName'], data)
                        self.redis.redis_put_result(self.uid,data)

            else:
                break
        # redis.close()
if __name__ == '__main__':
    pc = EncryptStr('keyskeyskeyskeys')  # 初始化密钥
    e = pc.encrypt("passwd123")
    d = pc.decrypt("0e0dbd0509f9eaaafd420b8a2c72cbde")
    print(e, d)