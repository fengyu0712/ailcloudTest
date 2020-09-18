from common.myredis import myRedis
from common.write_xls import WriteExcel

import Project_path,time

nowtime=time.strftime('%Y-%m-%d-%H-%M-%S')
result_path=Project_path.TestResult_path+"空调远程控制-自动化案例_Result%s.xls"%nowtime

#redis 应对关系

redis_db={
    0:'yb101',
    1:'HB'
}


w=WriteExcel()
header=['用例ID', '测试标签', '用例描述', '前置状态', '命令', '预期结果-nlu', '预期结果-luaResponse', '预期结果-tts','测试结果-nlu', '测试结果-luaResponse', '测试结果-tts','测试结果','mid']


def redisToxls(dblist):
    for i in range(len(dblist)):
        sheet=w.creattable(redis_db[dblist[i]])
        w.write_linedata(0,header,sheet)
        r=myRedis(dblist[i])
        key_list=r.get_keys()
        for i in range(len(key_list)):
            key_value=r.read_list(key_list[i])
            w.write_linedata(i+1,key_value,sheet)
    w.save_excel(result_path)
if __name__=='__main__':
    dblist = [0, 1]
    redisToxls(dblist)