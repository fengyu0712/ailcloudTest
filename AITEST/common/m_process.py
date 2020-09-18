from multiprocessing import Pool
import time
from common import Traversing_path

def mprocess(func,m,Poolnum=None):
    start_time = time.time()
    #默认四个进程
    if Poolnum==None:
        Poolnum=4
    p = Pool(Poolnum)
    for i in m:
        print("已添加子进程--%s"%i)
        p.apply_async(func, args=(i,))  # apply_async   引入的函数如果带有其他变量多进程会滞留，直接带入i不会
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
    endtime = time.time()
    print("this run take %s seconds" % format(endtime - start_time))

# if __name__=='__main__':
#     start_time = time.time()
#     case_path="F:\python_space\AITEST\\testcase\WS_Test"
#     case_path1 = case_path+"\\test_all_ws_new.py"
#     case_path2 = case_path+"\\test_websocket1.py"
#     # path = [case_path1, case_path2]
#     path = Traversing_path.file_all_path(case_path, filter_str="test")
#     print(path)
#     mprocess(runpy,path)
#     endtime = time.time()
#     print("this run take %s seconds" % format(endtime - start_time))