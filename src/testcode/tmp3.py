# urs/bin/python
# encoding:utf-8
import os
import unittest
from appium import webdriver
from base.baseAdb import BaseAdb
from time import sleep


class AndroidWebViewTests(unittest.TestCase):

    def setUp(self):
        BaseAdb.adbIntallUiautmator()
        # 清除缓存
        os.popen("adb shell pm clear io.selendroid.testapp")
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

        contexts = self.driver.contexts
        print(contexts)
        
        self.driver.switch_to.context('WEBVIEW_com.hujiang.normandy')
        sleep(5)
        
        print("点击网页控件")
        # 查找用户名
        loginUserNameBox = self.driver.find_element_by_css_selector(r"#hp-login-normal > div.hp-input.hp-input-username > input")
        loginUserNameBox.click()
        loginUserNameBox.send_keys("12345")

        # 查找密码项
        loginUserPwd = self.driver.find_element_by_xpath(r"//*[@id='hp-login-normal']/div[3]/input")
        loginUserPwd.send_keys('1234')
        # 点击登录
        loginBtnOk = self.driver.find_element_by_xpath(r"//*[@id='hp-login-normal']/button")
        loginBtnOk.click()


    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AndroidWebViewTests)
    unittest.TextTestRunner(verbosity=2).run(suite)