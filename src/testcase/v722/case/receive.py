# urs/bin/python
# encoding:utf-8

import time
from selenium.webdriver.common.by import By
from base.baseOperate import Commom as c
# from base.baseAdb import BaseAdb
# from base.baseFile import BaseFile
from pyse import Pyse

class WebReceive(object):
    
    def __init__(self, username, pwd, receiver):
        self.username = username
        self.pwd = pwd
        self.receiver = receiver
    
    def sendEmail(self):
        start = time.time()
        try:
            
            driver = Pyse("chrome")
            driver.max_window()
            driver.open("http://mail.10086.cn/")
            
#             time.sleep(3)
            driver.element_wait(r"name=>UserName", 10)
            driver.element_wait(r"id=>loginBtn", 10)
            
            driver.clear("name=>UserName")
            driver.type("name=>UserName", self.username)
            
            driver.type("id=>txtPass", self.pwd)
            driver.click("id=>loginBtn")
            
#             time.sleep(3)
            driver.click("name=>mailbox_1")
            
            # 收件箱
            driver.element_wait(r"xpath=>//*[@id='divTab']/ul/li[1]/span", 10)
            driver.element_wait(r"xpath=>//*[@id='sub']", 10)
            
            
            
            time.sleep(3)
            print("点击写信页: %r" %driver.get_display(r"xpath=>//a[@id='btn_compose']"))
            driver.click(r"xpath=>//a[@id='btn_compose']")
            
            time.sleep(3)
            print('切换frame: %r' %driver.get_display(r"xpath=>//*[@id='compose_preload' and @class='main-iframe']"))
            driver.switch_to_frame(r"xpath=>//*[@id='compose_preload' and @class='main-iframe']")
            
            time.sleep(3)
            print('输入主题: %r' %driver.get_display(r"xpath=>//input[@id='txtSubject']"))
            driver.click(r"xpath=>//input[@id='txtSubject']")
            driver.type(r"xpath=>//input[@id='txtSubject']", "testReceive")
            
#             time.sleep(2)
            
            print('输入收件人: %r' %driver.get_display(r"xpath=>//*[@id='toContainer']/div/div[2]/div[2]/input"))
#             driver.click("xpath=>//*[@id='toContainer']/div/div[2]/div[2]/input")
            driver.type(r"xpath=>//*[@id='toContainer']/div/div[2]/div[2]/input", self.receiver)
            
            print('点击发送')
            driver.click("id=>topSend")
            
#             print('等待完成')
#             driver.element_wait(r"xpath=>//*[@id='snedStatus']", 10)
            start = time.time()
            time.sleep(1)

        except BaseException as e:
            print('运行出错！！！')
            
            driver.get_windows_img(r"D:\%s.jpg " %(start))
            print(e)
        finally:
            driver.quit()
            return start


class Receive(object):
    
    def __init__(self,driver,username, pwd, receiver):
        self.driver = driver
        self.username = username
        self.pwd = pwd
        self.receiver = receiver
    
    # 未完成
    def receiveAction(self):
        '''接收邮件时延'''
        r = WebReceive(self.username,self.pwd,self.receiver)
        start = r.sendEmail()
    
        isReceived = self.waitforEmail()
        
        end = time.time()
        valueTime = str(round((end - start), 2))
        print('时间差: %r'  %valueTime)
        
        if isReceived:
            c.waitForElement(self.driver, By.ID, "android:id/list", 10)
            
            h = 400
            # 这里没有完成
            if c.waitForElement(self.driver,  By.ID, "android:id/list", 10) != None:
                el = c.waitForElement(self.driver,  By.ID, "android:id/list", 10)
                els = el.find_elements_by_class_name('android.widget.LinearLayout')
                h = els[0].get_window_size()
            
            
        
        
        return valueTime
    
    
    def waitforEmail(self, timeouts = 10):
        '''等待邮件出现'''
        timeout = int(round(time.time() * 1000)) + timeouts * 1000
        try:
            while (int(round(time.time() * 1000) < timeout)):
#                 print('wait.....')
                if(c.waitForElement(self.driver, By.NAME, "testReceive", 1)):
#                     print('find it')
                    return True;
                else:
                    c.swipeDown(self.driver)
                
                time.sleep(0.1)
        except BaseException as msg:
            print(msg)
            c.swipeDown(self.driver)
        
        else:
#             print('time out')
            return False 


if __name__ == '__main__':

    
    for i in range(0,9):
        t1 = time.time()
        r = WebReceive('13697485262', 'chinasoft123','13580491603@139.com')
        start = r.sendEmail()
        time.sleep(1)
#         print(start)
        t2 = time.time()
        valueTime = str(round((t2 - t1), 2))
        print('时间差: %r'  %valueTime)