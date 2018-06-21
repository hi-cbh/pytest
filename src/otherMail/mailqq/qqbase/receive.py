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
        try:
            driver = Pyse("chrome")
            # driver.implicitly_wait() # 添加了隐式等待，去除time.sleep显示等待
            # driver.max_window()
            print("打开请求登录页面")
            driver.open("https://mail.qq.com/")

            time.sleep(20)
            print("=>切换frame")
            driver.switch_to_frame("xpath=>//iframe[@id='login_frame']")
            driver.click("id=>switcher_plogin")

            print("=>输入账号")
            driver.clear("name=>u")
            driver.type("name=>u", self.username)

            print("=>输入密码")
            driver.type("id=>p", self.pwd)
            driver.click("id=>login_button")

            print("=>等待页面加载完成")
            time.sleep(10)
            driver.element_wait("id=>subject",10)

            print("=>点击写邮件")
            time.sleep(1)
            driver.click("xpath=>.//*[@id='composebtn']")

            print("=>切换frame")
            driver.switch_to_frame("id=>mainFrame")
            driver.element_wait("xpath=>//td[@class='qmEditorContent']/iframe")

            print("=>输入收件人")
            driver.type("xpath=>//div[@id='toAreaCtrl']/div[@class='addr_text']/input",self.receiver)

            print("=>输入主题")
            driver.type("xpath=>//td[@class='content_title']/div/div/div/input[@id='subject']","TestMailQQ")

            print("=>点击发送")
            driver.click("xpath=>//a[@class='btn_gray btn_space']")

            start = time.time()
            time.sleep(1)

            return start
        except BaseException as e:
            print('运行出错！！！')
            return start
        finally:
            driver.quit()



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
        isReceived = False

        time_out = int(round(time.time() * 1000)) + 1*60 * 1000

        # 获取邮件发送成功，退出；否则返回超时
        while int(round(time.time() * 1000)) < time_out :

            if BaseAdb.dumpsys_notification("TestMailQQ"):
                isReceived = True
                break

            time.sleep(0.1)


        end = time.time()
        
        valueTime = str(round((end - start), 2))
        print('[接收本域邮件时延]: %r'  %valueTime)

        time.sleep(3)

        # 如果出现未读邮件，进行删除第一封邮件
        if isReceived:

            self.driver.swipe(self.driver.get_window_size()["width"] - 20, 650, 20, 650, 500)

            if self.driver.get_element("xpath=>//android.widget.TextView[contains(@text,'删除')]") != None:
                self.driver.click("xpath=>//android.widget.TextView[contains(@text,'删除')]")

        time.sleep(5)

        return valueTime
    
    
    def waitforEmail(self, timeouts = 30):
        '''等待邮件出现'''
        timeout = int(round(time.time() * 1000)) + timeouts * 1000
        try:
            while (int(round(time.time() * 1000) < timeout)):
                print('wait.....')
                # if self.driver.get_element("xpath=>//android.view.View[contains(@content-desc,'TestMailQQ')]",1) != None :
                if self.driver.get_element(r"uiautomator=>收件箱(1)​",1) != None :
                # if BaseAdb.dumpsys_notification("TestMailQQ") :
                    print('find it')
                    return True
                # else:
                #     self.driver.swipeDown()
                
                time.sleep(0.1)
        except BaseException as msg:
            print(msg)
            self.driver.swipe_down()
            return False
        else:
#             print('time out')
            return False 


if __name__ == '__main__':

    
    for i in range(1):
        t1 = time.time()
        r = WebReceive('3495834281', 'chinasoft123','2915673336@qq.com')
        start = r.sendEmail()
        time.sleep(1)
        print(start)
        t2 = time.time()
        valueTime = str(round((t2 - t1), 2))
        print('时间差: %r' %valueTime)