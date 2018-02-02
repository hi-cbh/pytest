# urs/bin/python
# encoding:utf-8

import configparser as cparser
import os
import time
import unittest
from src.base.baseAdb import BaseAdb
from src.mail.mailOperation import EmailOperation
from src.aserver.AppiumServer import AppiumServer2
from src.db.sqlhelper import SQLHelper
from src.base.baseTime import BaseTime
from src.psam.psam import Psam
from src.testcase.v731.easycase.login import Login
from src.testcase.v731.easycase.send import Send
#
# PATH = lambda p:os.path.abspath(
#     os.path.join(os.path.dirname(__file__),p)
#     )


# ======== Reading user_db.ini setting ===========
base_dir = str(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
file_path = base_dir + "/user_db.ini"

cf = cparser.ConfigParser()
cf.read(file_path)

username = cf.get("userconf", "user1")
pwd = cf.get("userconf", "pwd1")

versionID = cf.get("verconf", "versionid")
##====================

class PeakValue(unittest.TestCase):
    
    def setUp(self):  
        # AppiumServer2().start_server()
        time.sleep(10)
        EmailOperation(username+"@139.com", pwd).mv_forlder(["100", "INBOX"])
        BaseAdb.adb_intall_uiautmator()
        
        self.driver = Psam(version="5.1.1")
    
    #释放实例,释放资源
    def tearDown(self):
        self.driver.quit()
        EmailOperation(username+"@139.com", pwd).mv_forlder(["INBOX", "100"])

        time.sleep(5)
        # AppiumServer2().stop_server()
        
        
    def testCase(self):
        
        network = BaseAdb.get_network_type()
        print('当前网络状态：%s' %network)
        
        runtimes = 12
        
        for x in range(1,runtimes):
            time.sleep(5)
            eo = EmailOperation(username+"@139.com", pwd)
            eo.check_inbox()
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

        

    
if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(PeakValue('testCase'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)