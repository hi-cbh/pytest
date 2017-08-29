# urs/bin/python
# encoding:utf-8

import os
import unittest
import time
from appium import webdriver
from selenium.webdriver.common.by import By
from base.operateElement import OperateElement as oe

PATH = lambda p:os.path.abspath(
    os.path.join(os.path.dirname(__file__),p)
    )

class Timedelay(unittest.TestCase):
    
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '6.0'
        desired_caps['deviceName'] = 'android'
        desired_caps['appPackage'] = 'cn.cj.pe'
        desired_caps['appActivity'] = 'com.mail139.about.LaunchActivity'
        desired_caps["unicodeKeyboard"] = "True"
        desired_caps["resetKeyboard"] = "True"
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.e = oe.__init__(self, driver = self.driver)
    
    #释放实例,释放资源
    def tearDown(self):
        #os.popen("adb shell pm clear cn.cj.pe")
        self.driver.quit()

    def openEmail(self):
        # print("stop")
        # 杀进程
        os.popen("adb shell am force-stop cn.cj.pe")
        time.sleep(4)
        
        # 在桌面查找 139邮箱
        el = self.e.waitforE(self,By.NAME,u"139邮箱")
        
        # 获取开始时间
        starttime = time.time()
        
        # 点击139邮箱
        el.click();
        
        # 等待页面存在 收件箱字段
        self.e.waitforE(self,By.NAME,u"收件箱")
        # 记录结束时间
        endtime = time.time()
        # 计算时间差
        calctime = round((endtime - starttime),2)
        print(calctime)   

    def contorlEmail(self):
        print("start")
        for i in range(5):
            self.openEmail();


    
if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(Timedelay('contorlEmail'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)