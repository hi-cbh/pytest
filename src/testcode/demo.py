# urs/bin/python
# encoding:utf-8
import os,sys
import threading
from multiprocessing import Process
from base.baseTime import BaseTime
TestResult = [{'min': '0.0%', 'max': '0.79%', 'avg': '0.32%'}, {'min': 116.85, 'max': 116.86, 'avg': 116.86}]

datas = {'productName' : '139','versionID':"versionID",'networkType':"network",\
         'nowTime':BaseTime.getCurrentTime(), \
         'avgcpu':TestResult[0]["avg"],'maxcpu':TestResult[0]["max"], \
         'avgmem':TestResult[1]["avg"],'maxmem':TestResult[1]["max"], \
         'groupId':"x"}


print(float(TestResult[0]["avg"].replace('%', '')))