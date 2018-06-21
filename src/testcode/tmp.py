# _*_ coding:utf-8 _*_
from appium import webdriver
import time
import unittest
from src.testcode.demo2 import getNotification
class Appium(unittest.TestCase):
    def setUp(self):
        desired_caps={}
        desired_caps['platformName']='Android'
        desired_caps['platformVersion']='4.4'
        desired_caps['deviceName']='Android Emulator'
        desired_caps['appPackage']='cn.cj.pe'
        desired_caps['appActivity']='com.mail139.about.LaunchActivity'
        desired_caps['unicodeKeyboard']='True'
        desired_caps['resetKeyboard']='True'
        self.driver=webdriver.Remote('http://localhost:4723/wd/hub',desired_caps)
        self.driver.implicitly_wait(8)
    def tearDown(self):
        self.driver.quit()

    """
    #登录139邮箱
    def test_login(self):
        self.driver.find_element_by_xpath('//android.widget.RelativeLayout/android.widget.ImageView').click()
        self.driver.find_element_by_id('cn.cj.pe:id/register_number').clear()
        self.driver.find_element_by_id('cn.cj.pe:id/register_number').send_keys('15876527487')
        self.driver.find_element_by_id('cn.cj.pe:id/register_password').send_keys('wu123456')
        self.driver.find_element_by_id('cn.cj.pe:id/login').click()
        time.sleep(2)
        title =self.driver.find_element_by_id('cn.cj.pe:id/actionbar_sub_title').text
        self.assertEqual(title,'收件箱','没有进入收件箱')
    """

    #发送邮件
    def test_sendEmail(self):
        self.driver.find_element_by_id('cn.cj.pe:id/actionbar_right_view').click()
        self.driver.find_element_by_xpath('//android.widget.RelativeLayout/child::android.view.View[1]').send_keys('15521151114@139.com')
        self.driver.find_element_by_xpath('//android.widget.LinearLayout/child::android.widget.EditText[1]').send_keys('发送测试邮件')
        self.driver.find_element_by_id('cn.cj.pe:id/txt_send').click()
        self.driver.find_element_by_id('cn.cj.pe:id/back_to_list').click()
        getNotification('发送邮件成功')
        time.sleep(2)

    """
    #退出登录
    def test_logout(self):
        self.driver.find_element_by_name('我的').click()
        self.driver.find_element_by_id('cn.cj.pe:id/set_txt').click()
        self.driver.find_element_by_id('cn.cj.pe:id/account_name').click()
        self.driver.find_element_by_id('cn.cj.pe:id/account_logoff').click()
        self.driver.find_element_by_id('cn.cj.pe:id/right').click()
        assert '注册139' in self.driver.page_source,'退出账号失败'
    """

if __name__=='__main__':
    unittest.main()


