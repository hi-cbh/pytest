# urs/bin/python
# encoding:utf-8

import configparser as cparser
import os
import time
import unittest
from src.base.baseAdb import BaseAdb
from src.otherApk.record360.flowRecord import FlowRecord360Action as flow360
from src.psam.psam import Psam
from src.mail.mailOperation import EmailOperation
from src.base.baseTime import BaseTime
from src.db.sqlhelper import SQLHelper
from src.aserver.AppiumServer import AppiumServer2
from src.testcase.v722.easycase.login import Login
#
# PATH = lambda p:os.path.abspath(
#     os.path.join(os.path.dirname(__file__),p)
#     )


# ======== Reading user_db.ini setting ===========
base_dir = str(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
base_dir = base_dir.replace('\\','/')
file_path = base_dir + "/user_db.ini"

cf = cparser.ConfigParser()
cf.read(file_path)

username2 = cf.get("userconf", "user2")
pwd2 = cf.get("userconf", "pwd2")

versionID = cf.get("verconf", "versionid")
##====================

class LoginFlow(unittest.TestCase):
    
    def setUp(self):
        try:
            time.sleep(10)
            AppiumServer2().start_server()
            time.sleep(15)
            BaseAdb.adbIntallUiautmator()
            self.driver = Psam()
        except BaseException as error:
            print("setUp过程中错误")
        else:
            EmailOperation(username2+"@139.com", pwd2).clearForlder(["INBOX",u"已删除",u"已发送"])
            time.sleep(10)
            EmailOperation(username2+"@139.com", pwd2).moveForlder(["20","INBOX"])
            time.sleep(10)

    
    #释放实例,释放资源
    def tearDown(self):
        self.driver.quit()
        time.sleep(5)
        AppiumServer2().stop_server()
        EmailOperation(username2+"@139.com", pwd2).moveForlder(["INBOX","20"])

    def testCase(self):
        appPackage = "cn.cj.pe"  # 程序的package

        try:
            print("======运行首次登录流量开始======")
            # 前期准备
            time.sleep(5)
            fw = flow360(self.driver)
            fw.executePreset()
            
            BaseAdb.adbStop(appPackage)
            time.sleep(2)
            BaseAdb.adbClear(appPackage)
            time.sleep(5)
            # 准备完成
            
            network = BaseAdb.getNetworkType()
            print('当前网络状态：%s' %network)
            
            runtimes = 2
            for x in range(1,runtimes):
                print("运行首次等次数：%d" %x)
                try:
                    login=Login(self.driver,username2, pwd2)
                    login.loginActionLoginFlow()
                    
                    # 等待未读邮件出现
                    print('等待未读邮件出现.....20封')
                    isTrue = self.waitForEmailCount()
                    
                    if isTrue:
                        print('记录流量值')
                        result = fw.executeRecord(u"139邮箱", network, False)
                        time.sleep(5)
                        BaseAdb.adbHome()
                        time.sleep(2)
                        BaseAdb.adbStop(appPackage)
                        time.sleep(2)
                        BaseAdb.adbClear(appPackage)
                        time.sleep(5)
                        datas = {'productName' : '139','versionID':versionID,'networkType':network,'nowTime':BaseTime.getCurrentTime(), \
                                 'upflow':result["up"],'downflow':result["down"], 'allflow':result["all"],'groupId':x}
                        SQLHelper.Insertflowlogin(datas)
                        time.sleep(2)
                except BaseException as be:
                    print("运行首次等次数：%d 出错，当次数据不入数据库!" %x)
#                     print(be)
                    
        except BaseException as be:
            print("运行出错")
            print(be)
        finally:
            print("======运行首次登录流量结束======")
        

    def waitForEmailCount(self): 
        '''等待页面显示20封未读邮件'''
        timeout = int(round(time.time() * 1000)) + 60 * 1000
        if self.driver.element_wait("id=>cn.cj.pe:id/mailAlert", 60) != None:
            try: 
                while (int(round(time.time() * 1000) < timeout)):
                    emailCnt = self.driver.get_attribute("id=>cn.cj.pe:id/mailAlert", "text")

                    if(int(emailCnt) == 20):
                        return True
                    time.sleep(0.4)
            except BaseException as error:
                print('等待未读邮件是出错')
#                 print(error)
                return False
                
        else:
            print("没有未读邮件，或邮件数量不对")
            return False

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(LoginFlow('testCase'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)