# urs/bin/python
# encoding:utf-8

import time
from selenium.webdriver.common.by import By
from base.baseOperate import Commom as c
from base.baseAdb import BaseAdb
class Send(object):
    
    def __init__(self,driver, username):
        self.username = username
        self.driver = driver
        
    def sendAction(self):
        try:
            # 点击写邮件按钮
            c.waitForElement(self.driver, By.ID, "cn.cj.pe:id/actionbar_right_view").click()
            # 收件人输入内容
            c.waitForElement(self.driver, By.ID, "cn.cj.pe:id/to_wrapper").send_keys(self.username)
            # 点击空白地方
            c.waitForElement(self.driver, By.ID, "cn.cj.pe:id/actionbar_title_sub").click()
            
            # 输入主题
            el = c.waitForElement(self.driver, By.ID, "cn.cj.pe:id/subject")
            el.click()
            el.send_keys('test')
            
    
            # 输入邮件内容
            el = c.waitForElement(self.driver, By.ID, "cn.cj.pe:id/message_content")
            el.click()
            el.send_keys('123456789012345678901234567890')               
            
            # 添加附件
            c.waitForElement(self.driver, By.ID, "cn.cj.pe:id/add_attachment").click()
            c.waitForElement(self.driver, By.NAME, "本地文件夹").click()
            c.waitForElement(self.driver, By.NAME, "0").click()        
            c.waitForElement(self.driver, By.NAME, "0.").click()
            c.waitForElement(self.driver, By.NAME, "test2M.rar").click()
            c.waitForElement(self.driver, By.ID, "cn.cj.pe:id/check_button").click()
            
            # 点击发送按钮
            el = c.waitForElement(self.driver, By.ID, "cn.cj.pe:id/txt_send")
            start = time.time()
            el.click()
            
            c.waitForElement(self.driver,By.NAME, '已完成', 120)
            end = time.time()
            
            valueTime = str(round((end - start), 2))
            print('时间差: %r'  %valueTime)
            
            BaseAdb.adbBack()
            time.sleep(2)
            return valueTime
    
        except BaseException:
            print('下载附件出错了！！！')
            return 0   
        