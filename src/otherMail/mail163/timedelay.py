# urs/bin/python
# encoding:utf-8

import os,time,unittest,sys
import configparser as cparser
from src.base.baseTime import BaseTime
from src.db.sqlhelper import SQLHelper
from src.base.baseAdb import BaseAdb
from src.mail.mailOperation import EmailOperation
from src.psam.psam import Psam
from src.otherMail.mail163.bash163.login import Login
from src.otherMail.mail163.bash163.opendown import OpenDown
from src.otherMail.mail163.bash163.send import Send
from src.otherMail.mail163.bash163.receive import Receive

# sys.path.append(r"/Users/apple/git/pytest/")

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

class Timedelay(unittest.TestCase):

    def setUp(self):
        try:
            # BaseAdb.adb_intall_uiautmator()
            self.driver = Psam(version="5.1",apk=qq_apk,ativity=qq_ativity)
        except BaseException :
            print("setUp启动出错！")
        #
        # else:
        #     EmailOperation(username+"@139.com", pwd).mv_forlder(["990", "INBOX"])
        #     time.sleep(10)



    #释放实例,释放资源
    def tearDown(self):
        self.driver.quit()
        # print("运行结束")
        #
        # time.sleep(5)
        # # AppiumServer2().stop_server()
        #
        # EmailOperation(username+"@139.com", pwd).mv_forlder(["INBOX", "990"])


    def testCase(self):

        network = BaseAdb.get_network_type()
        print('当前网络状态：%s' %network)

        runtimes = 2

        for x in range(1,runtimes):
            # 复位
            logintime = 0
            opentime = 0
            downtime = 0
            sendtime = 0
            receivetime = 0

            print('当前运行次数为：%r' %(str(x)))

            stat = u'开始登录时延测试'

            try:

                login=Login(self.driver,username, pwd)
                logintime = login.login_action()

                stat = u'发送邮件测试'
                send = Send(self.driver,username+'@163.com')
                sendtime = send.send_action()

                self.assertTrue(sendtime != 0, "邮件发送出错！！！")

                stat = u'开始打开邮件、下载附件测试'
                od = OpenDown(self.driver)
                opentime = od.open_mail()

                self.assertTrue(opentime != 0, "打开邮件出错！！！")
                downtime = od.down_file()

                # 删除邮件
                self.driver.swipe(self.driver.get_window_size()["width"] - 20, 450, 20, 450, 500)

                if self.driver.get_element("uiautomator=>删除") != None:
                    self.driver.click("uiautomator=>删除")

                stat = u'接收本域邮件测试'
                re = Receive(self.driver,username2, pwd2, username+"@163.com")
                receivetime = re.receiveAction()

            except BaseException as be:
                print("运行到：%s 运行出错，当次数据不入数据库!" %stat)
                print(be)
            else:
                result = {'logintime': logintime, 'readtime': opentime, 'downtime':downtime, 'sendtime':sendtime, 'receivetime':receivetime}

                # 将 None的值，赋值为 0
                for k,v in result.items():
                    if v == None:
                        print('赋值')
                        result[k] = 0

                print(result)

                # testResult = {'productName' : '139','versionID':versionID,'networkType': network,'nowTime':BaseTime.get_current_time(), 'groupId':x}
                #
                # datas = dict(testResult , **result)
                #
                # SQLHelper.insert_timedelay(datas)



if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(Timedelay('testCase'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)