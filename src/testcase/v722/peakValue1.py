# urs/bin/python
# encoding:utf-8

import configparser as cparser
import os
import time
import unittest
from base.baseAdb import BaseAdb
from mail.mailOperation import EmailOperation
<<<<<<< HEAD
from aserver.AppiumServer import AppiumServer2
from db.sqlhelper import SQLHelper
from base.baseTime import BaseTime
=======
from psam.psam import Psam
from testcase.v722.easycase.login import Login
from testcase.v722.easycase.send import Send

>>>>>>> mac
PATH = lambda p:os.path.abspath(
    os.path.join(os.path.dirname(__file__),p)
    )


# ======== Reading user_db.ini setting ===========
base_dir = str(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
base_dir = base_dir.replace('\\', '/')
file_path = base_dir + "/user_db.ini"

cf = cparser.ConfigParser()
cf.read(file_path)

username = cf.get("userconf", "user1")
pwd = cf.get("userconf", "pwd1")

versionID = cf.get("verconf", "versionid")
##====================

class PeakValue(unittest.TestCase):
    
    def setUp(self):  
        AppiumServer2().start_server()
        time.sleep(10)
        EmailOperation(username+"@139.com", pwd).moveForlder(["100","INBOX"])
    
        BaseAdb.adbIntallUiautmator()
        
        self.driver = Psam()
    
    #释放实例,释放资源
    def tearDown(self):
        self.driver.quit()
        EmailOperation(username+"@139.com", pwd).moveForlder(["INBOX","100"])

        time.sleep(5)
        AppiumServer2().stop_server()
        
        
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
                TestResult = send.sendActionPeakValue()

                time.sleep(5)
                eo = EmailOperation(username+"@139.com", pwd)
                eo.clearForlder([u'已删除',u'已发送'])   
                time.sleep(5)   
                
                datas = {'productName' : '139','versionID':versionID,'networkType':network,\
                         'nowTime':BaseTime.getCurrentTime(), \
                         'avgcpu':TestResult[0]["avg"].replace('%', ''),'maxcpu':TestResult[0]["max"].replace('%', ''), \
                         'avgmem':TestResult[1]["avg"],'maxmem':TestResult[1]["max"], \
                         'groupId':x}
                
                SQLHelper.InsertCPUMEM(datas)
                
                
            except BaseException as be:
                print("运行到：%s 运行出错，当次数据不入数据库!" %stat)
                print(be)

        

    
if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(PeakValue('testCase'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)