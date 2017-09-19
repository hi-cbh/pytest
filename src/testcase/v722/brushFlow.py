# urs/bin/python
# encoding:utf-8

import configparser as cparser
import os
import time
import unittest
from base.baseAdb import BaseAdb
from mail.mailOperation import EmailOperation
from otherApk.record360.flowRecord import FlowRecord360Action as flow360
from psam.psam import Psam
from testcase.v722.easycase.login import Login
from testcase.v722.easycase.public import PublicUtil as pu

PATH = lambda p:os.path.abspath(
    os.path.join(os.path.dirname(__file__),p)
    )


# ======== Reading user_db.ini setting ===========
base_dir = str(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
file_path = base_dir + "/user_db.ini"

cf = cparser.ConfigParser()
cf.read(file_path)

username = cf.get("userconf", "user1")
pwd = cf.get("userconf", "pwd1")

##====================

class BrushFlow(unittest.TestCase):
    
    def setUp(self):  
        eo = EmailOperation(username+"@139.com", pwd)
        eo.moveForlder(["100","INBOX"])         
        BaseAdb.adbIntallUiautmator()
        self.driver = Psam()
    
    #释放实例,释放资源
    def tearDown(self):
        self.driver.quit()
   
        eo = EmailOperation(username+"@139.com", pwd)
        eo.moveForlder(["INBOX","100"]) 

    def testCase(self):
        
        network = BaseAdb.getNetworkType()
        width = self.driver.get_window_size()['width']
        height = self.driver.get_window_size()['height']
        print('当前网络状态：%s' %network)
        
        runtimes = 2
        appPackage = "cn.cj.pe"  # 程序的package
        appActivity = "com.mail139.about.LaunchActivity"  # 程序的Activity

        fw = flow360(self.driver)

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
            fw.executePreset()
            for x in range(1,runtimes):
                BaseAdb.adbHome()
                time.sleep(2)
                print('启动139')
                BaseAdb.adbStartApp(appPackage, appActivity)
                time.sleep(10)
                print('下拉')
                self.driver.swipe(width/2, 350, width/2, height - 100, 500)
                time.sleep(10)
                BaseAdb.adbHome()
                time.sleep(3)
                fw.executeRecord(u"139邮箱", network, False)
                
        except BaseException as be:
            print("运行出错，当次数据不入数据库!")
            print(be)

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(BrushFlow('testCase'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)