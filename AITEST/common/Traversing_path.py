import os

#获取目录和文建名

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
def dir_all_path(path,filter_str=None):
    if filter_str==None:
        filter_str=""
    dir_list = []
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for dir in dirs:
                if  filter_str in dir:
                    dir_list.append(os.path.join(root, dir))

    return dir_list

if __name__=="__main__":

    # case_path="E:\\AI_test\\testcase\\WS_Test"
    # case_path1 = case_path+"\\test_all_ws_new.py"
    #
    # a=file_all_path(case_path)
    # print(a)
    a="E:\log\\20200731"
    b=file_all_path(a,file_type="log")
    print(b)