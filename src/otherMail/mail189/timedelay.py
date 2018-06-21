# urs/bin/python
# encoding:utf-8

import os,time,unittest,sys
import configparser as cparser
from src.base.baseTime import BaseTime
from src.db.sqlhelper import SQLHelper
from src.base.baseAdb import BaseAdb
from src.mail.mailOperation import EmailOperation
from src.psam.psam import Psam
from src.otherMail.mail189.bash189.login import Login
from src.otherMail.mail189.bash189.opendown import OpenDown
from src.otherMail.mail189.bash189.send import Send
from src.otherMail.mail189.bash189.receive import Receive
from src.otherApk.gt.gtutil import GTTest
# sys.path.append(r"/Users/apple/git/pytest/")

# ======== Reading user_db.ini setting ===========
base_dir = str(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
file_path = base_dir + "/user_db.ini"

cf = cparser.ConfigParser()
cf.read(file_path)

username = cf.get("corp21cn", "user3")
pwd = cf.get("corp21cn", "pwd3")
username2 = cf.get("corp21cn", "user2")
pwd2 = cf.get("corp21cn", "pwd2")

versionID = cf.get("verconf", "versionid")

##====================

qq_apk="com.corp21cn.mail189"
qq_ativity="com.corp21cn.mailapp.activity.ClientIntroducePage"

class Timedelay(unittest.TestCase):

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


                time.sleep(10)
                gt = GTTest("com.corp21cn.mail189")
                gt.startGT()

                stat = u'发送邮件测试'
                send = Send(self.driver,username+'@189.cn')
                sendtime = send.send_action()

                self.assertTrue(sendtime != 0, "邮件发送出错！！！")


                stat = u'开始打开邮件、下载附件测试'
                opentime = OpenDown(self.driver).open_mail()

                # time.sleep(2)
                # BaseAdb.adb_back()
                # time.sleep(2)
                #
                # # 删除邮件
                # self.driver.swipe(self.driver.get_window_size()["width"] - 20, 450, 20, 450, 500)
                # time.sleep(2)
                # BaseAdb.adb_tap(1000/1440 * self.driver.get_window_size()["width"], 500/2560 * self.driver.get_window_size()["height"])
                # time.sleep(2)


                # self.assertTrue(opentime != 0, "打开邮件出错！！！")
                downtime = OpenDown(self.driver).down_file()

                # 删除邮件
                self.driver.swipe(self.driver.get_window_size()["width"] - 20, 450, 20, 450, 500)
                time.sleep(2)
                BaseAdb.adb_tap(1300/1440 * self.driver.get_window_size()["width"], 500/2560 * self.driver.get_window_size()["height"])
                time.sleep(2)

                stat = u'接收本域邮件测试'
                re = Receive(self.driver,username2, pwd2, username+"@189.cn")
                receivetime = re.receiveAction()

                data = gt.endGT()
                print(data)

                time.sleep(5)
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

                testResult = {'productName' : '189','versionID':versionID,'networkType': network,'nowTime':BaseTime.get_current_time(), 'groupId':x}

                datas = dict(testResult , **result)

                SQLHelper.insert_timedelay(datas)



if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(Timedelay('testCase'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)