# urs/bin/python
# encoding:utf-8

import os
import unittest
import configparser as cparser
from testcase.v722.easycase.login import Login
from testcase.v722.easycase.send import Send
from testcase.v722.easycase.openDown import OpenDown
from testcase.v722.easycase.receive import Receive
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
username2 = cf.get("userconf", "user2")
pwd2 = cf.get("userconf", "pwd2")
filename = cf.get("userconf", "filename")
path = r'/mnt/sdcard/139PushEmail/download/%s@139.com/*%s.rar'  %(username, filename)
        
##====================


class Timedelay(unittest.TestCase):
    
    def setUp(self): 
        eo = EmailOperation(username+"@139.com", pwd)
        eo.moveForlder(["990","INBOX"])
        BaseAdb.adbIntallUiautmator()
        self.driver = Psam()
        
        
    
    #释放实例,释放资源
    def tearDown(self):
        self.driver.quit()
        print("运行结束")
        eo = EmailOperation(username+"@139.com", pwd)
        eo.moveForlder(["INBOX", "990"])
        

    def testCase(self):
        
        network = BaseAdb.getNetworkType()
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

            try:
                stat = u'开始登录时延测试' 
                login=Login(self.driver,username, pwd)
                logintime = login.loginActionTime()

                
                stat = u'开始打开邮件、下载附件测试' 
                od = OpenDown(self.driver, path, filename)
                opentime = od.openAction() 
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

                result = {'login': logintime, 'open': opentime, 'down':downtime, 'send':sendtime, 'receive':receivetime}
                
                # 将 None的值，赋值为 0
                for k,v in result.items():
                    if v == None:
                        print('赋值')
                        result[k] = 0
                         
                print(result)
        
        

    
if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(Timedelay('testCase'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)