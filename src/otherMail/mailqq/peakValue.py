# urs/bin/python
# encoding:utf-8

import configparser as cparser
import os
import time
import unittest
from src.base.baseAdb import BaseAdb
from src.db.sqlhelper import SQLHelper
from src.base.baseTime import BaseTime
from src.psam.psam import Psam
from src.otherMail.mailqq.qqbase.login import Login
from src.otherMail.mailqq.qqbase.send import Send
from src.otherMail.mailqq.qqbase.opendown import OpenDown
from src.otherMail.mailqq.qqbase.receive import Receive
from src.otherApk.gt.gtutil import GTTest

#
# PATH = lambda p:os.path.abspath(
#     os.path.join(os.path.dirname(__file__),p)
#     )


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


class PeakValue(unittest.TestCase):


    def setUp(self):
        try:
            BaseAdb.adb_intall_uiautmator()
            self.driver = Psam(version="6.0",apk=qq_apk,ativity=qq_ativity)
        except BaseException :
            print("setUp启动出错！")


    #释放实例,释放资源
    def tearDown(self):
        self.driver.quit()
        
    def testCase(self):
        
        network = BaseAdb.get_network_type()
        print('当前网络状态：%s' %network)
        
        runtimes = 10
        
        for x in range(1,runtimes):
            time.sleep(5)
            print('当前运行次数为：%r' %(str(x)))

            try:
                stat = u'开始登录' 
                login=Login(self.driver,username, pwd)
                login.login_action()

                gt = GTTest(qq_apk)
                gt.startGT()
                time.sleep(10)

                stat = u'发送邮件测试'
                send = Send(self.driver,username+'@qq.com')
                sendtime = send.send_action()

                self.assertTrue(sendtime != 0, "邮件发送出错！！！")

                stat = u'开始打开邮件、下载附件测试'
                od = OpenDown(self.driver)
                opentime = od.open_mail()

                self.assertTrue(opentime != 0, "打开邮件出错！！！")
                downtime = od.down_file()

                #删除邮件
                self.driver.swipe(self.driver.get_window_size()["width"] - 20, 670, 20, 670, 500)

                if self.driver.get_element("xpath=>//android.widget.TextView[contains(@text,'删除')]") != None:
                    self.driver.click("xpath=>//android.widget.TextView[contains(@text,'删除')]")
                # self.driver.click("xpath=>//android.widget.TextView[contains(@text,'收件箱')]")
                # 成功率很低，主要是打不开网页，https协议
                stat = u'接收本域邮件测试'
                re = Receive(self.driver,username2, pwd2, username+"@qq.com")
                receivetime = re.receiveAction()

                time.sleep(5)

                TestResult = []
                TestResult = gt.endGT()
                print(TestResult)


                datas = {'productName' : 'qq','versionID':versionID,'networkType':network,\
                         'nowTime':BaseTime.get_current_time(), \
                         'avgcpu':TestResult[0]["avg"].replace('%', ''),'maxcpu':TestResult[0]["max"].replace('%', ''), \
                         'avgmem':TestResult[1]["avg"],'maxmem':TestResult[1]["max"], \
                         'groupId':x}

                print(datas)
                SQLHelper.insert_cpu_mem(datas)
                
                
            except BaseException as be:
                print("运行到：%s 运行出错，当次数据不入数据库!" %stat)
                print(be)

        

    
if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(PeakValue('testCase'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)