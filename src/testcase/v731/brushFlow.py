# urs/bin/python
# encoding:utf-8

import configparser as cparser
import os
import time
import unittest
from src.base.baseAdb import BaseAdb
from src.otherApk.record360.flowRecord import FlowRecord360Action as flow360
from src.psam.psam import Psam
from src.base.baseTime import BaseTime
from src.mail.mailOperation import EmailOperation
from src.aserver.AppiumServer import AppiumServer2
from src.db.sqlhelper import SQLHelper
from src.testcase.v731.easycase.login import Login
from src.testcase.v731.easycase.public import PublicUtil as pu
#
# PATH = lambda p:os.path.abspath(
#     os.path.join(os.path.dirname(__file__),p)
#     )


# ======== Reading user_db.ini setting ===========
base_dir = str(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
file_path = base_dir + "/user_db.ini"

cf = cparser.ConfigParser()
cf.read(file_path)

username = cf.get("userconf", "user4")
pwd = cf.get("userconf", "pwd4")
versionID = cf.get("verconf", "versionid")
##====================

class BrushFlow(unittest.TestCase):
    
    def setUp(self):  
        # AppiumServer2().start_server()
        # time.sleep(10)
        EmailOperation(username+"@139.com", pwd).mv_forlder(["100", "INBOX"])         
        BaseAdb.adb_intall_uiautmator()
        self.driver = Psam()
    
    #释放实例,释放资源
    def tearDown(self):
        self.driver.quit()
   
        EmailOperation(username+"@139.com", pwd).mv_forlder(["INBOX", "100"]) 
        time.sleep(5)
        # AppiumServer2().stop_server()

    def testCase(self):
        
        network = BaseAdb.get_network_type()
        width = self.driver.get_window_size()['width']
        height = self.driver.get_window_size()['height']
        print('当前网络状态：%s' %network)

        runtimes = 12

        appPackage = "cn.cj.pe"  # 程序的package
        appActivity = "com.mail139.about.LaunchActivity"  # 程序的Activity

        fw = flow360(self.driver)

        try:

            login=Login(self.driver,username, pwd)
            login.loginAction()

            time.sleep(5)

            pu.loadEmail(self.driver)
            
            BaseAdb.adb_stop(appPackage)
            time.sleep(5)
            BaseAdb.adb_start_app(appPackage, appActivity)
            time.sleep(3)
            BaseAdb.adb_home()
            time.sleep(3)
            fw.exec_preset()
            for x in range(1,runtimes):
                BaseAdb.adb_home()
                time.sleep(2)
                print('启动139')
                BaseAdb.adb_start_app(appPackage, appActivity)
                time.sleep(10)
                print('下拉')
                stime = time.time()
                self.driver.swipe(width/2, 350, width/2, height - 100, 500)
                time.sleep(10)
                BaseAdb.adb_home()
                time.sleep(3)
                result = fw.exec_record(u"139邮箱", network, False)
                etime = time.time()
                valueTime = str(round((etime - stime), 2))
                print('[获取流量时间]: %r'  %valueTime)

                datas = {'productName' : '139',"versionID":versionID,'networkType':network,'nowTime':BaseTime.get_current_time(), \
                     'upflow':result["up"],'downflow':result["down"], 'allflow':result["all"], 'groupId':x}
                
                SQLHelper.insert_flow_other(datas)
                
        except BaseException as be:
            print("运行出错，当次数据不入数据库!")
            print(be)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(BrushFlow('testCase'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)