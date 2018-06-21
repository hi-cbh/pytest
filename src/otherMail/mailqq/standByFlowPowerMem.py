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
from src.otherMail.mailqq.qqbase.login import Login

from src.base.baseTime import BaseTime
from src.db.sqlhelper import SQLHelper
from src.testcase.v731.easycase.receive import WebReceive


# ======== Reading user_db.ini setting ===========
base_dir = str(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
file_path = base_dir + "/user_db.ini"

cf = cparser.ConfigParser()
cf.read(file_path)

username = cf.get("qqconf", "user1")
pwd = cf.get("qqconf", "pwd1")
username2 = cf.get("qqconf", "user2")
pwd2 = cf.get("qqconf", "pwd2")

versionID = cf.get("verconf", "versionid")

##====================

qq_apk="com.tencent.androidqqmail"
qq_ativity="com.tencent.qqmail.launcher.desktop.LauncherActivity"


class StandByFlowPowerMem(unittest.TestCase):
    
    def setUp(self):
        BaseAdb.adb_intall_uiautmator()
        self.driver = Psam(version="6.0",apk=qq_apk,ativity=qq_ativity)
    
    #释放实例,释放资源
    def tearDown(self):
        self.driver.quit()


    def testCase(self):
        
        network = BaseAdb.get_network_type()
        print('当前网络状态：%s' %network)


        fw = flow360(self.driver)
        gt = GTTest(qq_apk)
        pa = PowerAction(self.driver)

        debug = False

        if debug:
            print("debug模式.......")
        else:
            print("正式环境测试")
        try:
             
            login=Login(self.driver,username2, pwd2)
            login.login_action()
            time.sleep(2)
            print("点击收件箱")
            self.driver.click("xpath=>//android.widget.TextView[contains(@text,'收件箱')]")
            time.sleep(2)
            print("加载更多")
            time_out = int(round(time.time() * 1000)) + 2 * 60 * 1000
            while int(round(time.time() * 1000)) < time_out:
                self.driver.swipe_up()
                self.driver.swipe_up()
                self.driver.swipe_up()
                self.driver.swipe_up()
                btn = self.driver.get_element(u"uiautomator=>加载更多",1)
                if btn != None:
                    btn.click()

                time.sleep(1)


            BaseAdb.adb_stop(qq_apk)
            time.sleep(5)
            BaseAdb.adb_start_app(qq_apk, qq_ativity)
            time.sleep(3)

            print("点击收件箱")
            self.driver.click("xpath=>//android.widget.TextView[contains(@text,'收件箱')]")
            time.sleep(3)

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
                for t in range(1,29):
                    print(u"等待分钟: %d" %t)
                    time.sleep(1*60)

            print("开始记录......")
            flow = fw.exec_record(u"QQ邮箱", network, False, False)
            time.sleep(5)
            mem = gt.endGT()
            elc = pa.exec_record("QQ", False)

            datas = {'productName' : 'qq','versionID':versionID,'networkType':network,'nowTime':BaseTime.get_current_time(), \
                 'electric':elc,'upflow':flow["up"], 'downflow':flow["down"], \
                 'allflow':flow["all"],'avgmem':mem[1]["avg"],'groupId':"1"}

            print(datas)
            SQLHelper.insert_standyno(datas)
            time.sleep(5)

            print("发送邮件......")
            for i in range(3):
                # BaseAdb.adb_shell("adb shell am broadcast -a my.email.broadcast")
                r = WebReceive('13697485262', 'chinasoft123',username2+'@qq.com')
                r.sendEmail()

                time.sleep(20)

            print("等待两分钟")
            time.sleep(2*60)


            print("再次记录......")
            flow = fw.exec_record(u"QQ邮箱", network, False)
            elc = pa.exec_record("QQ")
            emailcnt = 3
            print("接收邮件数量：%d" %emailcnt)

            datas = {'productName' : 'qq','versionID':versionID,'networkType':network,'nowTime':BaseTime.get_current_time(), \
                     'electric':elc,'upflow':flow["up"], 'downflow':flow["down"], \
                     'allflow':flow["all"],'emailcount':emailcnt,'groupId':"1"}

            print(datas)
            SQLHelper.insert_standy_email(datas)

            print("清除")
            time.sleep(5)
            BaseAdb.adb_stop("edu.umich.PowerTutor")
            BaseAdb.adb_stop("com.qihoo360.mobilesafe")
            time.sleep(5)


            # BaseAdb.adbStartApp(appPackage, appActivity)
            # self.driver.swipeDown()
            # time.sleep(5)
            # self.driver.swipeDown()
            # time.sleep(5)

        except BaseException as be:
            print("运行出错，当次数据不入数据库!")
            print(be)

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(StandByFlowPowerMem('testCase'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)