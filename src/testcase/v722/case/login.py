# urs/bin/python
# encoding:utf-8

import time
from base.baseOperate import Commom as c
from selenium.webdriver.common.by import By


class Login(object):
    
    def __init__(self,driver, username, pwd):
        self.username = username
        self.pwd = pwd
        self.driver = driver
        
    def loginAction(self):
        
        try:
        
            self.driver.reset()
            
            time.sleep(8)
            
            c.waitForElement(self.driver, By.XPATH, r"//android.widget.ImageView[@index='0']").click()
                # 输入
            els = self.driver.find_elements_by_id('cn.cj.pe:id/input')
            print('输入')
            els[0].send_keys(self.username)
            
            print('输入')
            els[1].send_keys(self.pwd)
            
            print('点击登录')
            loginButton = c.waitForElement(self.driver,By.ID, 'cn.cj.pe:id/login')
            
            print('开始计时和点击登录')
            start = time.time()
            loginButton.click()
            
            print('wait for Element')
            c.waitForElement(self.driver,By.ID, 'cn.cj.pe:id/submit')
            end = time.time()
            
    #         c.waitForElement(self.driver,By.ID, 'cn.cj.pe:id/check')
    #         print('点击')
    #         els2 = self.driver.find_elements_by_id('cn.cj.pe:id/check')
    #         print('点击')
    #         els2[0].click()
    #         print('点击')
    #         els2[1].click()
            print('点击')
            c.waitForElement(self.driver, By.ID, 'cn.cj.pe:id/submit').click()
            
            valueTime = str(round((end - start), 2))
            print('时间差: %r'  %valueTime)
            return valueTime
        except BaseException:
            print('首次登录出错！！！')
            return 0
        
        
        
        
        
        