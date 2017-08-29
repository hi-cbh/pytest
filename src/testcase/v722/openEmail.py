# urs/bin/python
# encoding:utf-8
import time
import os
import unittest
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class MyTestCase(unittest.TestCase):
    #脚本初始化,获取操作实例
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '5.1'
        desired_caps['deviceName'] = 'android'
        desired_caps['appPackage'] = 'cn.cj.pe'
        desired_caps['appActivity'] = 'com.mail139.about.LaunchActivity'
        desired_caps["unicodeKeyboard"] = "True"
        desired_caps["resetKeyboard"] = "True"
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

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
        el = Element.waitForElement(self,By.NAME,u"139邮箱")
        
        # 获取开始时间
        starttime = time.time()
        
        # 点击139邮箱
        el.click();
        
        # 等待页面存在 收件箱字段
        Element.waitForElement(self,By.NAME,u"收件箱")
        # 记录结束时间
        endtime = time.time()
        # 计算时间差
        calctime = round((endtime - starttime),2)
        print(calctime)   

    def contorlEmail(self):
        print("start")
        for i in range(5):
            self.openEmail();


class Element:
    def __init__(self,name, by):
        self.name = name
        self.by = by
     
    @staticmethod
    def waitForElement(self,name,by):
        try:
            el = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((name,by)))
        except:
            print("can not find" + by)
        return el
     


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(MyTestCase('contorlEmail'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)