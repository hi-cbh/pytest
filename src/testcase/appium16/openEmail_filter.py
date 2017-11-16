# urs/bin/python
# encoding:utf-8
# import os
# import time,sys
import unittest
# import configparser as cparser
import time
from src.psam.psam import Psam

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from appium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait
#
# PATH = lambda p:os.path.abspath(
#     os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__),p)))
# )
# sys.path.append(r'/Users/apple/git/pytest/src/')
# print("file: %s" %PATH)

# from src.aserver.AppiumServer import AppiumServer2
# from src.db.sqlhelper import SQLHelper
# from src.base.baseTime import BaseTime
# from src.mail.mailOperation import EmailOperation
# from src.psam.psam import Psam
# from src.testcase.v722.easycase.login import Login
# from src.testcase.v722.easycase.public import PublicUtil as pu



from src.base.baseAdb import BaseAdb

GetMax = 3  # 获取的组数量
RunMax = 11  # 大循环最大允许次数
RunMax2 = 3  # 每一次小循环最大允许次数
ListMax = 10  # 列表长度
DelNum = 2  # 允许剔除的数量

class OpenEmail(unittest.TestCase):
    #脚本初始化,获取操作实例
    def setUp(self):
    #     desired_caps = {}
    #     desired_caps['platformName'] = 'Android'
    #     desired_caps['platformVersion'] = "5.1"
    #     desired_caps['deviceName'] = 'android'
    #     desired_caps['appPackage'] = 'cn.cj.pe'
    #     desired_caps['appActivity'] = 'com.mail139.about.LaunchActivity'
    #     desired_caps['newCommandTimeout'] = 7200
    #     desired_caps["unicodeKeyboard"] = "True"
    #     desired_caps["resetKeyboard"] = "True"
    #     self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    # #         self.driver.implicitly_wait(10)
        self.driver = Psam("5.1")

    #释放实例,释放资源
    def tearDown(self):
        self.driver.quit()
        
        time.sleep(5)
        # AppiumServer2().stop_server()
  
    def testCase(self):
        network = BaseAdb.getNetworkType()
        print('当前网络状态：%s' %network)
        
        # appPackage = "com.tencent.wstt.gt"  # 程序的package
        # appActivity = "com.tencent.wstt.gt.activity.SplashActivity"  # 程序的Activity
        #
        #
        # BaseAdb.adbStop(appPackage)
        # time.sleep(5)
        # BaseAdb.adbStartApp(appPackage, appActivity)
        time.sleep(3)

        BaseAdb.adbHome()
        time.sleep(3)

        # el = self.driver.uiautomator('new UiSelector().text("139邮箱")')
        # el = self.driver.find_element_by_android_uiautomator('new UiSelector().text("139邮箱")')
        #
        # print(el.is_displayed())
        #
        #
        # el = WebDriverWait(self.driver,10,1).until(EC.presence_of_element_located((By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("139邮箱")')))
        el = self.driver.element_wait(u"uiautomator=>139邮箱")

        print(el.is_displayed())
       
  
  
if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(OpenEmail('testCase'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


