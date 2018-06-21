# urs/bin/python
# encoding:utf-8

import time
from src.base.baseAdb import BaseAdb
# from base.baseFile import BaseFile
from pyse import Pyse




class WebReceive(object):
    
    def __init__(self, username, pwd, receiver):
        self.username = username
        self.pwd = pwd
        self.receiver = receiver
    
    def sendEmail(self):
        start = time.time()
        driver = Pyse("chrome")
        try:
            # driver.max_window()
            print("打开请求登录页面")
            driver.open("http://webmail30.189.cn/w2/")

            time.sleep(3)
            print("切换frame")
            driver.switch_to_frame("id=>iframeLogin")
            # driver.click("id=>switcher_plogin")

            print("输入账号")
            driver.clear("id=>userName")
            driver.type("id=>userName", self.username)

            print("输入密码")
            driver.type("xpath=>//*[@id='password']", self.pwd)
            driver.click("xpath=>//*[@id='password']")

            print("等待页面加载完成")
            time.sleep(2)
            driver.click("xpath=>//*[@id='j-login']")

            print("等待页面")
            time.sleep(5)
            driver.element_wait("xpath=>//*[@id='search-input']",30)
            driver.element_wait("xpath=>//*[@id='j_mf_pannel_mail']/div[2]/div/div[1]/a",30)
            driver.click("xpath=>//*[@id='j_mf_pannel_mail']/div[2]/div/div[1]/a")
            time.sleep(5)

            print("输入收件人")
            driver.type("xpath=>//*[@id='J_wm_to_scrollbar']/div/input",self.receiver)

            print("输入主题")
            driver.type("xpath=>//*[@id='J_wm_subject']","TestMail189")

            print("点击发送")
            driver.click("xpath=>//*[@id='J_wm_post_mail']")

            start = time.time()
            time.sleep(2)

        except BaseException as e:
            print('运行出错！！！')
            
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
    
    def receiveAction(self):
        w = self.driver.get_window_size()['width']
        '''接收邮件时延'''
        r = WebReceive(self.username,self.pwd,self.receiver)
        print('=>接收邮件时延')
        start = r.sendEmail()
        self.driver.swipe_down()

        print('=>等待本域邮件出现')
        isReceived = self.waitforEmail()
        end = time.time()
        
        
        valueTime = str(round((end - start), 2))
        print('[接收本域邮件时延]: %r'  %valueTime)
        
        # 如果出现未读邮件，进行删除第一封邮件
        if isReceived:
            self.driver.swipe(self.driver.get_window_size()["width"] - 20, 450, 20, 450, 500)
            time.sleep(2)
            BaseAdb.adb_tap(1300/1440 * self.driver.get_window_size()["width"], 500/2560 * self.driver.get_window_size()["height"])
            time.sleep(2)

        time.sleep(5)
        return valueTime
    
    
    def waitforEmail(self, timeouts = 30):
        '''等待邮件出现'''
        timeout = int(round(time.time() * 1000)) + timeouts * 1000
        try:
            while (int(round(time.time() * 1000) < timeout)):
                print('wait.....')
                # if self.driver.get_element("xpath=>//android.view.View[contains(@content-desc,'TestMailQQ')]",1) != None :
                if self.driver.get_element(r"uiautomator=>TestMail189",1) != None :
                    print('find it')
                    return True
                else:
                    self.driver.swipe_down()
                
                time.sleep(0.1)
        except BaseException as msg:
            print(msg)
            self.driver.swipe_down()
        
        else:
#             print('time out')
            return False 


if __name__ == '__main__':

    
    for i in range(1):
        t1 = time.time()
        r = WebReceive('13427665104', 'yscs987654','13580491603@189.cn')
        start = r.sendEmail()
        time.sleep(1)
        print(start)
        t2 = time.time()
        valueTime = str(round((t2 - t1), 2))
        print('时间差: %r' %valueTime)