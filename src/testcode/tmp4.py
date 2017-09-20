# urs/bin/python
# encoding:utf-8
import os
import unittest
from appium import webdriver
from base.baseAdb import BaseAdb
from time import sleep


class AndroidWebViewTests(unittest.TestCase):

    def setUp(self):
        os.popen("adb shell pm clear com.hujiang.normandy")
        
        BaseAdb.adbIntallUiautmator()
        
        
        # 清除缓存
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '6.0'
        desired_caps['deviceName'] = 'android'
        desired_caps['appPackage'] = 'com.hujiang.normandy'
        desired_caps['appActivity'] ='com.hujiang.normandy.SplashActivity'
        desired_caps['newCommandTimeout'] = '360'
        desired_caps["unicodeKeyboard"] = "True"
        desired_caps["resetKeyboard"] = "True"
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def test_webview(self):
        # 等待启动
        sleep(10)
        print("开始运行脚本")
        loginBtn = self.driver.find_element_by_id('com.hujiang.normandy:id/login')
        loginBtn.click()
        # 等待切换
        sleep(2)
        
        
        print("点击网页控件")
        # 查找用户名
        self.adbTap(500, 778)
        self.adbInputText("12345")
        sleep(2)

        # 查找密码项
        self.adbTap(500, 1100)
        self.adbInputText("12345")
        sleep(2)
        # 点击登录
        self.adbTap(500, 1600)
        sleep(2)
        
    def adbInputText(self,txt):
        '''通过命令行，输入字段'''
        os.popen('adb shell input text %s' %txt)
        
    def adbTap(self, x,y):
        '''通过坐标，点击屏幕'''
        os.popen("adb shell input tap %s %s " %(str(x), str(y)))  

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AndroidWebViewTests)
    unittest.TextTestRunner(verbosity=2).run(suite)