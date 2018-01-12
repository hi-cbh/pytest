# urs/bin/python
# encoding:utf-8

import os
import time
import sys

file_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(file_dir)
print(file_dir)

base_dir = str(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
PCpath = base_dir + "/logs/"
print("PC: %s" %PCpath)

from src.base.baseAdb import BaseAdb
from src.base.baseTime import BaseTime
from src.otherApk.gt.csvData import GetCSVData






class GTTest(object):

    def __init__(self, pkgname):
        self.pkgname = pkgname

    def startGT(self):

        print('GT开启')
        BaseAdb.adb_start_gt()
        print('GT添加package')
        BaseAdb.adb_gt_add_pkg(self.pkgname)
        print('GT添加CPU监控')
        BaseAdb.adb_gt_base_cmd("cpu", "1")
        print('GT添加Mem监控')
        BaseAdb.adb_gt_base_cmd("pri", "1")

        time.sleep(2)
        print('返回')
        BaseAdb.adb_back()

        time.sleep(2)

        print('开始记录时间')

    def endGT(self):

        SDpath = r"/mnt/sdcard/GT/GW/"
        print('记录CPU结果')
        BaseAdb.adb_gt_base_cmd("cpu", "0")
        print('记录MEM结果')
        BaseAdb.adb_gt_base_cmd("pri", "0")

        print('获取文件名')
        filename = BaseTime.current_time()
        print(filename)
        print('保存文件')
        BaseAdb.adb_gt_save(r"/runcode/" + filename, filename)

        remote = SDpath + self.pkgname+r"/runcode/"+filename+r"/"
        print(remote)
        time.sleep(2)

        print("PC: %s" %PCpath + filename+"/")
        # os.mkdir(PCpath)
        BaseAdb.adb_pull(remote, PCpath + filename + "/")
        time.sleep(2)
        ls = []
        d = GetCSVData(PCpath+filename+r"/", self.pkgname)
        ls.append(d.get_cpu())
        ls.append(d.get_mem())

        print(ls)
        return ls


if __name__ == "__main__":
    # BaseAdb.adb_clear("com.tencent.wstt.gt")
    # time.sleep(2)

    # gt = GTTest("cn.cj.pe")
    gt = GTTest("com.tencent.androidqqmail")
    gt.startGT()
    time.sleep(10)
    gt.endGT()
