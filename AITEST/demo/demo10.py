import winsound,time,os
from common.log import Logger
def file_all_path(path,file_type=None,filter_str=None):
    if filter_str==None:
        filter_str=""
    files_list = []
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                if file_type == None:
                    if filter_str in file:
                        files_list.append(os.path.join(root, file))
                else:
                    if file.split('.')[-1] ==file_type  and filter_str in file:
                        files_list.append(os.path.join(root, file))
    elif os.path.isfile(path):
        if path.split('.')[-1] ==file_type  and filter_str in path:
            files_list.append(path)
    else:
        print("无法解析目录：【%s】"%path)
    return files_list



wekup_wav_fail="E:\\test_wakeup"
test_list=file_all_path(wekup_wav_fail,file_type='wav')
test_num=10
Logger().info("共%s个唤醒音频，接下来每个音频循环%s次播放"%(len(test_list),test_num))
for i in range(0,len(test_list)):
    Logger().info("【第%s个音频】--%s"%(i+1,test_list[i]))
    n = test_num
    while n>0:
        Logger().info("第%s次播放：%s"%(test_num+1-n,test_list[i]))
        winsound.PlaySound(test_list[i], winsound.SND_FILENAME)
        time.sleep(5)
        n-=1

