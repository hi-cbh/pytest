# urs/bin/python
# encoding:utf-8

import time
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
            # driver.implicitly_wait() # 添加了隐式等待，去除time.sleep显示等待
            # driver.max_window()
            print("打开请求登录页面")
            driver.open("http://mail.163.com/")

            time.sleep(3)
            print("切换frame")
            driver.switch_to_frame("xpath=>//iframe[@id='x-URS-iframe']")
            # driver.click("id=>switcher_plogin")

            print("输入账号")
            driver.clear("xpath=>//input[@class='j-inputtext dlemail']")
            driver.type("xpath=>//input[@class='j-inputtext dlemail']", self.username)

            print("输入密码")
            driver.type("xpath=>//input[@class='j-inputtext dlpwd']", self.pwd)
            driver.click("xpath=>//input[@class='j-inputtext dlpwd']")

            print("等待页面加载完成")
            time.sleep(2)
            driver.click("id=>dologin")

            print("切换frame")
            time.sleep(5)
            print("切换parent")
            driver.switch_to_parent_frame()
            driver.click("xpath=>//li[@class='js-component-component ra0 mD0']")
            time.sleep(5)

            print("输入收件人")
            driver.type("xpath=>//input[@class='nui-editableAddr-ipt']",self.receiver)

            print("输入主题")
            driver.type("xpath=>//input[@class='nui-ipt-input' and @maxlength='256']","TestMail163")

            print("点击发送")
            driver.click("xpath=>html/body/div[2]/div[1]/div[2]/header/div/div[1]/div/span[2]")

            start = time.time()
            time.sleep(1)

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
        
        print('=>等待本域邮件出现')
        isReceived = self.waitforEmail()
        end = time.time()
        
        
        valueTime = str(round((end - start), 2))
        print('[接收本域邮件时延]: %r'  %valueTime)
        
        # 如果出现未读邮件，进行删除第一封邮件
        if isReceived:

            # 删除邮件
            self.driver.swipe(self.driver.get_window_size()["width"] - 20, 450, 20, 450, 500)

            if self.driver.get_element("uiautomator=>删除") != None:
                self.driver.click("uiautomator=>删除")

        time.sleep(5)
        return valueTime
    
    
    def waitforEmail(self, timeouts = 30):
        '''等待邮件出现'''
        timeout = int(round(time.time() * 1000)) + timeouts * 1000
        try:
            while (int(round(time.time() * 1000) < timeout)):
                print('wait.....')
                # if self.driver.get_element("xpath=>//android.view.View[contains(@content-desc,'TestMailQQ')]",1) != None :
                if self.driver.get_element(r"id=>com.netease.mail:id/mail_list_item_state",1) != None :
                    print('find it')
                    return True
                else:
                    self.driver.swipeDown()
                
                time.sleep(0.1)
        except BaseException as msg:
            print(msg)
            self.driver.swipeDown()
        
        else:
#             print('time out')
            return False 


if __name__ == '__main__':

    
    for i in range(1):
        t1 = time.time()
        r = WebReceive('18718878590', 'yscs12345','13580491603@163.com')
        start = r.sendEmail()
        time.sleep(1)
        print(start)
        t2 = time.time()
        valueTime = str(round((t2 - t1), 2))
        print('时间差: %r' %valueTime)