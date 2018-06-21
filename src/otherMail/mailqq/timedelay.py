# urs/bin/python
# encoding:utf-8

import os,time,unittest,sys
import configparser as cparser
from src.base.baseTime import BaseTime
from src.db.sqlhelper import SQLHelper
from src.base.baseAdb import BaseAdb
from src.mail.mailOperation import EmailOperation
from src.psam.psam import Psam
from src.otherMail.mailqq.qqbase.login import Login
from src.otherMail.mailqq.qqbase.opendown import OpenDown
from src.otherMail.mailqq.qqbase.send import Send
from src.otherMail.mailqq.qqbase.receive import Receive

# sys.path.append(r"/Users/apple/git/pytest/")

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


class Timedelay(unittest.TestCase):

    def setUp(self):
        try:
            BaseAdb.adb_intall_uiautmator()
            self.driver = Psam(version="6.0",apk="com.tencent.androidqqmail",ativity="com.tencent.qqmail.launcher.desktop.LauncherActivity")
        except BaseException :
            print("setUp启动出错！")



    #释放实例,释放资源
    def tearDown(self):
        self.driver.quit()

    def testCase(self):

        network = BaseAdb.get_network_type()
        print('当前网络状态：%s' %network)

        runtimes = 12

        for x in range(1,runtimes):
            # 复位
            logintime = 0
            opentime = 0
            downtime = 0
            sendtime = 0
            receivetime = 0

            print('当前运行次数为：%r' %(str(x)))

            try:
                stat = u'开始登录时延测试'
                login=Login(self.driver,username, pwd)
                logintime = login.login_action()

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

                testResult = {'productName' : 'qq','versionID':versionID,'networkType': network,'nowTime':BaseTime.get_current_time(), 'groupId':x}

                datas = dict(testResult , **result)

                SQLHelper.insert_timedelay(datas)



if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(Timedelay('testCase'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)