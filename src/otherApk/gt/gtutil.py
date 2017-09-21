# urs/bin/python
# encoding:utf-8

import os
import time
from src.base.baseAdb import BaseAdb
from src.base.baseTime import BaseTime
from src.otherApk.gt.csvData import GetCSVData
#
# PATH = lambda p: os.path.abspath(
#     os.path.join(os.path.dirname(__file__), p)
# )

base_dir = str(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
# base_dir = base_dir.replace('\\', '/')
PCpath = base_dir + "/logs/"
print(PCpath)



class GTTest(object):

    def __init__(self, pkgname):
        self.pkgname = pkgname

    def startGT(self):

        print('GT开启')
        BaseAdb.adbStartGT()
        print('GT添加package')
        BaseAdb.adbGTAddPkg(self.pkgname)
        print('GT添加CPU监控')
        BaseAdb.adbGTbaseCommand("cpu", "1")
        print('GT添加Mem监控')
        BaseAdb.adbGTbaseCommand("pri", "1")

        time.sleep(2)
        print('返回')
        BaseAdb.adbBack()

        time.sleep(2)

        print('开始记录时间')

    def endGT(self):

        SDpath = r"/mnt/sdcard/GT/GW/"
        print('记录CPU结果')
        BaseAdb.adbGTbaseCommand("cpu", "0")
        print('记录MEM结果')
        BaseAdb.adbGTbaseCommand("pri", "0")

        print('获取文件名')
        filename = BaseTime.currentTime()
        print(filename)
        print('保存文件')
        BaseAdb.adbGTSave(r"/runcode/"+filename, filename)

        remote = SDpath + self.pkgname+r"/runcode/"+filename+r"/"
        print(remote)
        time.sleep(2)

        BaseAdb.adbPull(remote ,PCpath+filename+r"/")
        time.sleep(2)
        ls = []
        d = GetCSVData(PCpath+filename+r"/", 'cn.cj.pe')
        ls.append(d.getCPUValue())
        ls.append(d.getMEMValue())

        print(ls)
        return ls


if __name__ == "__main__":
    # BaseAdb.adbClear("com.tencent.wstt.gt")
    # time.sleep(2)

    gt = GTTest("cn.cj.pe")
    gt.startGT()
    time.sleep(10)
    gt.endGT()
