import os
import Project_path
Project=Project_path.projectfail

#执行命令安装requirements.txt中的模块
os.system("pip install -r %s\\requirements.txt "%Project)

#导出模块列表
#pip3 freeze >requirements.txt