# urs/bin/python
# encoding:utf-8

import configparser as cparser
import os
import time
import unittest
from base.baseAdb import BaseAdb
from mail.mailOperation import EmailOperation
from otherApk.gt.gtutil import GTTest
from otherApk.power.powerAction import PowerAction
from otherApk.record360.flowRecord import FlowRecord360Action as flow360
from psam.psam import Psam
from testcase.v722.easycase.login import Login
from testcase.v722.easycase.public import PublicUtil as pu

PATH = lambda p:os.path.abspath(
    os.path.join(os.path.dirname(__file__),p)
    )


# ======== Reading user_db.ini setting ===========
base_dir = str(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
# base_dir = base_dir.replace('\\', '/')
file_path = base_dir + "/user_db.ini"

cf = cparser.ConfigParser()
cf.read(file_path)

username = cf.get("userconf", "user1")
pwd = cf.get("userconf", "pwd1")

##====================

class StandByFlowPowerMem(unittest.TestCase):
    
    def setUp(self):  
        BaseAdb.adbShell("adb shell am start -W -n com.test.sendmail/.MainActivity")
        BaseAdb.adbHome()
        time.sleep(2)
        
        EmailOperation(username+"@139.com", pwd).moveForlder(["100","INBOX"]) 
        BaseAdb.adbIntallUiautmator()
        self.driver = Psam()
    
    #释放实例,释放资源
    def tearDown(self):
        self.driver.quit()
        EmailOperation(username+"@139.com", pwd).moveForlder(["INBOX","100"]) 


    def testCase(self):
        
        network = BaseAdb.getNetworkType()
        print('当前网络状态：%s' %network)
        
        appPackage = "cn.cj.pe"  # 程序的package
        appActivity = "com.mail139.about.LaunchActivity"  # 程序的Activity

        fw = flow360(self.driver)
        gt = GTTest("cn.cj.pe")
        pa = PowerAction(self.driver)

        try:
             
            login=Login(self.driver,username, pwd)
            login.loginAction()
            
            pu.loadEmail(self.driver)
            
            BaseAdb.adbStop(appPackage)
            time.sleep(5)
            BaseAdb.adbStartApp(appPackage, appActivity)
            time.sleep(3)
            BaseAdb.adbHome()
            time.sleep(3)
             
            print("静等待5分钟.....")
            for t in range(1,2):
                print(u"等待分钟: %d" %t)
                time.sleep(1*60)
            
            print("准备测试环境.....")
            print("do something")
            fw.executePreset()
            gt.startGT()
            pa.executePreset()
            
            print("静等待28分钟.....")
            for t in range(1,2):
                print(u"等待分钟: %d" %t)
                time.sleep(1*60)
            
            print("开始记录......")
            fw.executeRecord(u"139邮箱", network, False,False)
            time.sleep(5)
            gt.endGT()
            pa.executeRecord("139",False)
            
            print("发送邮件......")
            for i in range(3):
                BaseAdb.adbShell("adb shell am broadcast -a my.email.broadcast")
                time.sleep(20)
             
            print("等待两分钟")    
            time.sleep(2*60)
            
                
            print("再次记录......")
            fw.executeRecord(u"139邮箱", network, False)
            pa.executeRecord("139")
            emailcnt = EmailOperation(username+"@139.com", pwd).checkInboxCnt()
            print("接收邮件数量：%d" %emailcnt)
            
            print("清除")
            time.sleep(5)  
            EmailOperation(username+"@139.com", pwd).checkInbox()
            time.sleep(5)
            BaseAdb.adbStop("edu.umich.PowerTutor")
            BaseAdb.adbStop("com.qihoo360.mobilesafe")  
            time.sleep(5)
        except BaseException as be:
            print("运行出错，当次数据不入数据库!")
            print(be)

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(StandByFlowPowerMem('testCase'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)