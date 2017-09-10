# urs/bin/python
# encoding:utf-8
import os,sys

# PATH = lambda p:os.path.abspath(
#     os.path.join(os.path.dirname(__file__),p)
#     )
# 
# print()
# 

#需要使用线程的方式启动 appium server
base_dir = str(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
base_dir = base_dir.replace('\\', '/')
file_path = base_dir + "/bat/"
sys.path.append(file_path)
print(file_path)
os.system('start %sstartAppiumServer.bat' %file_path)

# 关闭，
# os.system('start stopAppiumServer.bat')
