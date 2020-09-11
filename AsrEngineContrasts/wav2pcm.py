import glob
import subprocess
import os
path='/home/kangyong/Data/wav'
filelist=os
filepath=''
filepcm=''

input_dir = path + r'/*.wav'
list_im = glob.glob(input_dir)
for i in list_im:
    filepcm = i.replace('wav','pcm')
    cmd='sox -t wav '+ i+' -t raw -r 1600 -c 1 -b 16 ' + filepcm
    # ret = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8",
    #                                  timeout=8)
    # print(ret)
    os.system(cmd)
# CompletedProcess(args='sox -t wav /home/kangyong/Data/wav/aaaf67cd-04c8-4f46-9906-078a2dd28492_20200831172909_4be99dd9-d0f3-4a0d-b610-27940d72dc45.wav -t raw -r 1600 -c -b 16 /home/kangyong/Data/pcm/aaaf67cd-04c8-4f46-9906-078a2dd28492_20200831172909_4be99dd9-d0f3-4a0d-b610-27940d72dc45.pcm', returncode=1, stdout='', stderr="sox FAIL sox: Channels value `-b' is not a positive integer\n")
# CompletedProcess(args='sox -t wav /home/kangyong/Data/wav/aaaf67cd-04c8-4f46-9906-078a2dd28492_20200831172928_c5627126-7a88-4206-85d4-c024c5182158.wav -t raw -r 1600 -c -b 16 /home/kangyong/Data/pcm/aaaf67cd-04c8-4f46-9906-078a2dd28492_20200831172928_c5627126-7a88-4206-85d4-c024c5182158.pcm', returncode=1, stdout='', stderr="sox FAIL sox: Channels value `-b' is not a positive integer\n")
# C