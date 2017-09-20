# urs/bin/python
# encoding:utf-8
<<<<<<< HEAD
import os,sys
import threading
from multiprocessing import Process
from base.baseTime import BaseTime
TestResult = [{'min': '0.0%', 'max': '0.79%', 'avg': '0.32%'}, {'min': 116.85, 'max': 116.86, 'avg': 116.86}]
=======
import os
>>>>>>> mac

datas = {'productName' : '139','versionID':"versionID",'networkType':"network",\
         'nowTime':BaseTime.getCurrentTime(), \
         'avgcpu':TestResult[0]["avg"],'maxcpu':TestResult[0]["max"], \
         'avgmem':TestResult[1]["avg"],'maxmem':TestResult[1]["max"], \
         'groupId':"x"}

<<<<<<< HEAD

print(float(TestResult[0]["avg"].replace('%', '')))
=======
# #需要使用线程的方式启动 appium server
# base_dir = str(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
# base_dir = base_dir.replace('\\', '/')
# file_path = base_dir + "/bat/"
# sys.path.append(file_path)
# print(file_path)
# os.system('start %sstartAppiumServer.bat' %file_path)

# readDeviceId = list(os.popen('adb devices').readlines())


# os.popen("PATH=$PATH:$HOME/bin:/sbin:/usr/bin:/usr/sbin")
# result = os.popen("echo $PATH")
# print(os.popen("echo $HOME").readlines())
# print(result.readlines())
# os.popen("/Users/apple/autoTest/android-sdk-macosx/platform-tools/adb")
# os.popen("adb")

import time
from src.base.baseAdb import BaseAdb
from src.psam.psam import Psam
import  unittest

# print("hello")
# 关闭，
# os.system('start stopAppiumServer.bat')
class TestDemo(unittest.TestCase):

        BaseAdb.adbIntallUiautmator()
        driver = Psam()
        BaseAdb.adbHome()
        time.sleep(1)
        BaseAdb.adbStop("cn.cj.pe")
        time.sleep(2)

        BaseAdb.adbStartApp("cn.cj.pe","com.mail139.about.LaunchActivity")
        # BaseAdb.adbHome()
        time.sleep(1)
        BaseAdb.adbStop("cn.cj.pe")
        time.sleep(2)

>>>>>>> mac
