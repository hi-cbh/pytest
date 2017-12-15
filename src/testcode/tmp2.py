# urs/bin/python
# encoding:utf-8
import os
import unittest
from appium import webdriver
from base.baseAdb import BaseAdb
from time import sleep


class AndroidWebViewTests(unittest.TestCase):

    def setUp(self):
        BaseAdb.adb_intall_uiautmator()
        # 清除缓存
        os.popen("adb shell pm clear io.selendroid.testapp")
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '6.0'
        desired_caps['deviceName'] = 'android'
        desired_caps['appPackage'] = 'io.selendroid.testapp'
        desired_caps['appActivity'] ='.HomeScreenActivity'
        desired_caps['newCommandTimeout'] = '360'
        desired_caps["unicodeKeyboard"] = "True"
        desired_caps["resetKeyboard"] = "True"
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def test_webview(self):

        button = self.driver.find_element_by_accessibility_id('buttonStartWebviewCD')
        button.click()
        
        input_field = self.driver.find_element_by_class_name("android.widget.EditText")
        input_field.click()
        sleep(2)
        # 光标移到末尾
        os.popen("adb shell input keyevent 123")
        sleep(2)
        
        # 删除文字
        for i in range(22):
            os.popen("adb shell input keyevent 67")
            sleep(0.1)
            
        sleep(1)
        
        input_field.send_keys('Appium User')
 
        submit = self.driver.find_element_by_xpath(r"//android.widget.Button[@content-desc='Send me your name!']")
        submit.click()

        source = self.driver.page_source
        self.assertNotEqual(-1, source.find('This is my way of saying hello'))
        self.assertNotEqual(-1, source.find('Appium User'))

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AndroidWebViewTests)
    unittest.TextTestRunner(verbosity=2).run(suite)