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
from src.otherMail.mail163.bash163.login import Login
from src.otherMail.mail163.bash163.send import Send
from src.otherMail.mail163.bash163.opendown import OpenDown
from src.otherMail.mail163.bash163.receive import Receive
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

username = cf.get("netconf", "user1")
pwd = cf.get("netconf", "pwd1")
username2 = cf.get("netconf", "user2")
pwd2 = cf.get("netconf", "pwd2")

versionID = cf.get("verconf", "versionid")

##====================
qq_apk="com.netease.mail"
qq_ativity="com.netease.mobimail.activity.LaunchActivity"


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
            stat = u'开始登录'
            try:

                login=Login(self.driver,username, pwd)
                login.login_action()

                time.sleep(2)

                gt = GTTest(qq_apk)
                gt.startGT()
                time.sleep(10)


                stat = u'发送邮件测试'
                send = Send(self.driver,username+'@163.com')
                sendtime = send.send_action()

                self.assertTrue(sendtime != 0, "邮件发送出错！！！")

                stat = u'开始打开邮件、下载附件测试'
                od = OpenDown(self.driver)
                opentime = od.open_mail()

                self.assertTrue(opentime != 0, "打开邮件出错！！！")
                od.down_file()

                # 删除邮件
                self.driver.swipe(self.driver.get_window_size()["width"] - 20, 450, 20, 450, 500)

                if self.driver.get_element("uiautomator=>删除") != None:
                    self.driver.click("uiautomator=>删除")

                stat = u'接收本域邮件测试'
                re = Receive(self.driver,username2, pwd2, username+"@163.com")
                re.receiveAction()


                TestResult = []
                TestResult = gt.endGT()
                print(TestResult)

                time.sleep(5)

                datas = {'productName' : '163','versionID':versionID,'networkType':network,
                         'nowTime':BaseTime.get_current_time(),
                         'avgcpu':TestResult[0]["avg"].replace('%', ''),'maxcpu':TestResult[0]["max"].replace('%', ''),
                         'avgmem':TestResult[1]["avg"],'maxmem':TestResult[1]["max"],
                         'groupId':x}

                print(datas)
                SQLHelper.insert_cpu_mem(datas)
                
                time.sleep(5)
            except BaseException as be:
                print("运行到：%s 运行出错，当次数据不入数据库!" %stat)
                print(be)

        

    
if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(PeakValue('testCase'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)