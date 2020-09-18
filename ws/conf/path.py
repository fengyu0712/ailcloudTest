import os
# from Common.conf import Read_conf
conf_path=os.path.split(os.path.realpath(__file__))[0]
projectfail=os.path.dirname(conf_path)

code_path=os.path.join(projectfail,'Code/')
log_path=os.path.join(projectfail,'log/')
date_path=os.path.join(projectfail,'test_date/')
result_path=os.path.join(projectfail,'test_result/')
audio_path=os.path.join(projectfail,'test_audio/')