import zipfile,os
def Zipfile(path,zippath=None):
    if zippath is None:
        zippath=os.path.join(os.path.dirname(path),os.path.basename(path)+".zip")
        # zippath=path+".zip"
    # 创建zip对象，
    fzip = zipfile.ZipFile(zippath, 'w', zipfile.ZIP_DEFLATED)
    if os.path.isdir(path):
        flist = os.listdir(path)
        # 获取压缩目录名称
        basename = os.path.basename(path)
        for name in flist:
            fpath = os.path.join(path, name)
            arcname = os.path.join(basename, name)
            # 写入要压缩文件，并添加归档文件名称
            fzip.write(fpath, arcname=arcname)
    elif os.path.isfile(path):
        # arcname=
        fzip.write(path,os.path.basename(path))
    else:
        print("无法解析目录：【%s】" % path)
    fzip.close()

if __name__=="__main__":
    path="E:\ws\log\\2020-06-23.log"
    a=os.path.basename(path)
    print(a)
    # path1="E:\ws\log"
    # path2 = "E:\ws\log\\2020-06-11.log.zip"
    Zipfile(path)