# urs/bin/python
# encoding:utf-8

import os,time
import unittest
import configparser as cparser
from testcase.v722.easycase.login import Login
from testcase.v722.easycase.public import PublicUtil as pu
from base.baseAdb import BaseAdb
from otherApk.record360.flowRecord import FlowRecord360Action as flow360
from psam.psam import Psam
from base.baseTime import BaseTime
from mail.mailOperation import EmailOperation
from aserver.AppiumServer import AppiumServer2
from db.sqlhelper import SQLHelper
PATH = lambda p:os.path.abspath(
    os.path.join(os.path.dirname(__file__),p)
    )


# ======== Reading user_db.ini setting ===========
base_dir = str(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
base_dir = base_dir.replace('\\', '/')
file_path = base_dir + "/user_db.ini"

cf = cparser.ConfigParser()
cf.read(file_path)

username = cf.get("userconf", "user1")
pwd = cf.get("userconf", "pwd1")
versionID = cf.get("verconf", "versionid")
##====================

class BrushFlow(unittest.TestCase):
    
    def setUp(self):  
        AppiumServer2().start_server()
        time.sleep(10)
        EmailOperation(username+"@139.com", pwd).moveForlder(["100","INBOX"])         
        BaseAdb.adbIntallUiautmator()
        self.driver = Psam()
    
    #释放实例,释放资源
    def tearDown(self):
        self.driver.quit()
   
        EmailOperation(username+"@139.com", pwd).moveForlder(["INBOX","100"]) 
        time.sleep(5)
        AppiumServer2().stop_server()

    def testCase(self):
        
        network = BaseAdb.getNetworkType()
        width = self.driver.get_window_size()['width']
        height = self.driver.get_window_size()['height']
        print('当前网络状态：%s' %network)
        
        runtimes = 5
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
                result = fw.executeRecord(u"139邮箱", network, False)

                datas = {'productName' : '139',"versionID":versionID,'networkType':network,'nowTime':BaseTime.getCurrentTime(), \
                     'upflow':result["up"],'downflow':result["down"], 'allflow':result["all"], 'groupId':x}
                
                SQLHelper.Insertflowother(datas)
                
        except BaseException as be:
            print("运行出错，当次数据不入数据库!")
            print(be)

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(BrushFlow('testCase'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)