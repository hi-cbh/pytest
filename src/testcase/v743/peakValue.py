# urs/bin/python
# encoding:utf-8

import configparser as cparser
import os
import time
import unittest
from src.base.baseAdb import BaseAdb
from src.mail.mailOperation import EmailOperation
from src.db.sqlhelper import SQLHelper
from src.base.baseTime import BaseTime
from src.psam.psam import Psam
from src.testcase.v743.easycase.login import Login
from src.testcase.v743.easycase.send import Send
from src.testcase.v743.easycase.openDown import OpenDown
from src.testcase.v743.easycase.receive import Receive
from src.otherApk.gt.gtutil import GTTest

# ======== Reading user_db.ini setting ===========
base_dir = str(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
file_path = base_dir + "/user_db.ini"

cf = cparser.ConfigParser()
cf.read(file_path)

username = cf.get("userconf", "user4")
pwd = cf.get("userconf", "pwd4")
username2 = cf.get("userconf", "user2")
pwd2 = cf.get("userconf", "pwd2")
filename = cf.get("userconf", "filename")
path = r'/mnt/sdcard/139PushEmail/download/%s@139.com/*%s.rar'  %(username, filename)


versionID = cf.get("verconf", "versionid")
##====================

class PeakValue(unittest.TestCase):
    
    def setUp(self):  
        time.sleep(10)
        EmailOperation(username+"@139.com", pwd).mv_forlder(["20", "INBOX"])
        BaseAdb.adb_intall_uiautmator()
        
        self.driver = Psam()
    
    #释放实例,释放资源
    def tearDown(self):
        self.driver.quit()
        EmailOperation(username+"@139.com", pwd).mv_forlder(["INBOX", "20"])
        time.sleep(5)

    def testCase(self):
        
        network = BaseAdb.get_network_type()
        print('当前网络状态：%s' %network)
        
        runtimes = 10
        
        for x in range(1,runtimes):
            time.sleep(5)
            eo = EmailOperation(username+"@139.com", pwd)
            eo.check_inbox(20)
            time.sleep(5)
            print('当前运行次数为：%r' %(str(x)))

            try:
                stat = u'开始登录' 
                login=Login(self.driver,username, pwd)
                login.loginActionPeakValue()

                time.sleep(10)

                appPackage = "cn.cj.pe"  # 程序的package
                appActivity = "com.mail139.about.LaunchActivity"  # 程序的Activity

                BaseAdb.adb_stop(appPackage)
                time.sleep(5)
                BaseAdb.adb_start_app(appPackage, appActivity)
                time.sleep(8)

                gt = GTTest("cn.cj.pe")
                gt.startGT()
                time.sleep(10)

                stat = u'开始打开邮件、下载附件测试'
                od = OpenDown(self.driver, path, filename)
                opentime = od.openAction()

                self.assertTrue(opentime != 0, "打开邮件错误！！！")
                downtime = od.downAction()
                od.setFirstEmail()

                stat = u'发送邮件测试'
                send = Send(self.driver,username2+'@139.com')
                sendtime = send.sendAction()

                stat = u'接收本域邮件测试'
                re = Receive(self.driver,username2, pwd2, username+"@139.com")
                receivetime = re.receiveAction()

                TestResult = []
                TestResult = gt.endGT()
                print(TestResult)

                # 删除第一封邮件
                self.del_first()

                time.sleep(5)
                eo = EmailOperation(username+"@139.com", pwd)
                eo.clear_forlder([u'已删除', u'已发送'])   
                time.sleep(5)   
                
                datas = {'productName' : '139','versionID':versionID,'networkType':network,\
                         'nowTime':BaseTime.get_current_time(), \
                         'avgcpu':TestResult[0]["avg"].replace('%', ''),'maxcpu':TestResult[0]["max"].replace('%', ''), \
                         'avgmem':TestResult[1]["avg"],'maxmem':TestResult[1]["max"], \
                         'groupId':x}

                SQLHelper.insert_cpu_mem(datas)

                
            except BaseException as be:
                print("运行到：%s 运行出错，当次数据不入数据库!" %stat)
                print(be)




    def del_first(self):

        if self.driver.element_wait('uiautomator=>testReceive') != None:
            h = 400
            print('=>查找第一封邮件位置')
            if self.driver.get_element("id=>android:id/list") != None:
                els = self.driver.get_sub_element("id=>android:id/list","class=>android.widget.LinearLayout")
                h = els[0].location['y']

            self.driver.swipe(self.driver.get_window_size()['width'] - 20, h, 20, h, 500)
            print("=>右滑删除")
            time.sleep(2)

            print('=>点击删除')
            self.driver.click("id=>cn.cj.pe:id/item_view_back_four")



    
if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(PeakValue('testCase'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)