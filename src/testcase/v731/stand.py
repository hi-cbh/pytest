# urs/bin/python
# encoding:utf-8

import configparser as cparser
import os
import time
import unittest
from src.base.baseAdb import BaseAdb
from src.otherApk.gt.gtutil import GTTest
from src.otherApk.power.powerAction import PowerAction
from src.otherApk.record360.flowRecord import FlowRecord360Action as flow360
from src.psam.psam import Psam
from src.aserver.AppiumServer import AppiumServer2
from src.mail.mailOperation import EmailOperation
from src.testcase.v731.easycase.login import Login
from src.testcase.v731.easycase.public import PublicUtil as pu
from src.base.baseTime import BaseTime
from src.db.sqlhelper import SQLHelper
from src.testcase.v731.easycase.receive import WebReceive
# PATH = lambda p:os.path.abspath(
#     os.path.join(os.path.dirname(__file__),p)
#     )


# ======== Reading user_db.ini setting ===========
base_dir = str(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
file_path = base_dir + "/user_db.ini"

cf = cparser.ConfigParser()
cf.read(file_path)

username = cf.get("userconf", "uctc")
pwd = cf.get("userconf", "pctc")
versionID = cf.get("verconf", "versionid")
##====================

class StandBy(unittest.TestCase):
    
    def setUp(self):
        BaseAdb.adb_intall_uiautmator()
        self.driver = Psam()
    
    #释放实例,释放资源
    def tearDown(self):
        self.driver.quit()

        time.sleep(5)
        # AppiumServer2().stop_server()

    def testCase(self):
        
        network = BaseAdb.get_network_type()
        print('当前网络状态：%s' %network)
        
        appPackage = "cn.cj.pe"  # 程序的package
        appActivity = "com.mail139.about.LaunchActivity"  # 程序的Activity

        fw = flow360(self.driver)
        gt = GTTest("cn.cj.pe")
        pa = PowerAction(self.driver)

        debug = True

        if debug:
            print("debug模式.......")
        else:
            print("正式环境测试")
        try:
             
            login=Login(self.driver,username, pwd)
            login.loginAction()
            print('等待5秒，预防没有弹窗出现邮件')
            pu.loadEmail(self.driver)
            

            BaseAdb.adb_stop(appPackage)
            time.sleep(5)
            BaseAdb.adb_start_app(appPackage, appActivity)
            time.sleep(8)
            BaseAdb.adb_home()
            time.sleep(3)

            if debug:
                print("静等待1分钟.....")
                for t in range(1,2):
                    print(u"等待分钟: %d" %t)
                    time.sleep(1*60)
            else:
                print("静等待5分钟.....")
                for t in range(1,6):
                    print(u"等待分钟: %d" %t)
                    time.sleep(1*60)

            print("准备测试环境.....")
            print("do something")
            fw.exec_preset()
            gt.startGT()
            pa.exec_preset()


            if debug:
                print("静等待2分钟.....")
                for t in range(1,2):
                    print(u"等待分钟: %d" %t)
                    time.sleep(1*60)
            else:
                print("静等待28分钟.....")
                for t in range(1,31):
                    print(u"等待分钟: %d" %t)
                    time.sleep(1*60)

            print("开始记录......")
            flow = fw.exec_record(u"139邮箱", network, False, False)
            time.sleep(5)
            mem = gt.endGT()
            elc = pa.exec_record("139", False)

            datas = {'productName' : '139','versionID':versionID,'networkType':network,'nowTime':BaseTime.get_current_time(), \
                 'electric':elc,'upflow':flow["up"], 'downflow':flow["down"],
                 'allflow':flow["all"],'avgmem':mem[1]["avg"],'groupId':"1"}

            print(datas)
            SQLHelper.insert_standyno(datas)
            time.sleep(15)

            print("清除")
            time.sleep(5)  
            BaseAdb.adb_stop("edu.umich.PowerTutor")
            BaseAdb.adb_stop("com.qihoo360.mobilesafe")
            time.sleep(5)

        except BaseException as be:
            print("运行出错，当次数据不入数据库!")
            print(be)

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(StandBy('testCase'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)