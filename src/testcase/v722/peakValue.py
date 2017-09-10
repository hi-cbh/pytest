# urs/bin/python
# encoding:utf-8

import os,time
import unittest
import configparser as cparser
from testcase.v722.easycase.login import Login
from testcase.v722.easycase.send import Send
from base.baseAdb import BaseAdb
from psam.psam import Psam
from mail.mailOperation import EmailOperation

PATH = lambda p:os.path.abspath(
    os.path.join(os.path.dirname(__file__),p)
    )


# ======== Reading user_db.ini setting ===========
base_dir = str((os.path.dirname(__file__)))
base_dir = base_dir.replace('\\', '/')
file_path = base_dir + "/user_db.ini"

cf = cparser.ConfigParser()
cf.read(file_path)

username = cf.get("userconf", "user1")
pwd = cf.get("userconf", "pwd1")

##====================

class PeakValue(unittest.TestCase):
    
    def setUp(self):  
        eo = EmailOperation(username+"@139.com", pwd)
        eo.moveForlder(["100","INBOX"])
        
        BaseAdb.adbIntallUiautmator()
        
        self.driver = Psam()
    
    #释放实例,释放资源
    def tearDown(self):
        self.driver.quit()
        eo = EmailOperation(username+"@139.com", pwd)
        eo.moveForlder(["INBOX","100"])

    def testCase(self):
        
        network = BaseAdb.getNetworkType()
        print('当前网络状态：%s' %network)
        
        runtimes = 2
        
        for x in range(1,runtimes):
            time.sleep(5)
            eo = EmailOperation(username+"@139.com", pwd)
            eo.checkInbox()
            time.sleep(5)
            print('当前运行次数为：%r' %(str(x)))

            try:
                stat = u'开始登录' 
                login=Login(self.driver,username, pwd)
                login.loginActionPeakValue()
                   
                stat = u'发送邮件' 
                send = Send(self.driver,username+'@139.com')
                send.sendActionPeakValue()
                
                time.sleep(5)
                eo = EmailOperation(username+"@139.com", pwd)
                eo.clearForlder([u'已删除',u'已发送'])   
                time.sleep(5)   
            except BaseException as be:
                print("运行到：%s 运行出错，当次数据不入数据库!" %stat)
                print(be)

        

    
if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(PeakValue('testCase'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)