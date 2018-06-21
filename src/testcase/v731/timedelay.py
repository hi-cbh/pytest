# urs/bin/python
# encoding:utf-8

import os,time,unittest,sys
import configparser as cparser
from src.base.baseTime import BaseTime
from src.db.sqlhelper import SQLHelper
from src.aserver.AppiumServer import AppiumServer2
from src.base.baseAdb import BaseAdb
from src.mail.mailOperation import EmailOperation
from src.psam.psam import Psam
from src.testcase.v731.easycase.login import Login
from src.testcase.v731.easycase.openDown import OpenDown
from src.testcase.v731.easycase.receive import Receive
from src.testcase.v731.easycase.send import Send


# sys.path.append(r"/Users/apple/git/pytest/")

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


class Timedelay(unittest.TestCase):

    def setUp(self):
        try:
            BaseAdb.adb_intall_uiautmator()
            self.driver = Psam("6.0")
        except BaseException :
            print("setUp启动出错！")

        else:
            EmailOperation(username+"@139.com", pwd).mv_forlder(["990", "INBOX"])
            time.sleep(10)



    #释放实例,释放资源
    def tearDown(self):
        self.driver.quit()
        print("运行结束")

        time.sleep(5)
        # AppiumServer2().stop_server()

        EmailOperation(username+"@139.com", pwd).mv_forlder(["INBOX", "990"])


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
                logintime = login.loginAction()


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

                testResult = {'productName' : '139','versionID':versionID,'networkType': network,'nowTime':BaseTime.get_current_time(), 'groupId':x}

                datas = dict(testResult , **result)

                SQLHelper.insert_timedelay(datas)



if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(Timedelay('testCase'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)