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
    
    def sendEmail(self, subject="cctv"):
        start = time.time()
        try:
            driver = Pyse("chrome")
            # driver.implicitly_wait() # 添加了隐式等待，去除time.sleep显示等待
            # driver.max_window()
            driver.open("http://mail.10086.cn/")
            
            time.sleep(3)
            driver.element_wait(r"name=>UserName", 10)
            driver.element_wait(r"id=>loginBtn", 10)
            
            driver.clear("name=>UserName")
            driver.type("name=>UserName", self.username)
            
            driver.type("id=>txtPass", self.pwd)
            driver.click("id=>loginBtn")
            
            time.sleep(1)
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

            time.sleep(2)
            print('输入收件人: %r' %driver.get_display(r"xpath=>//*[@id='toContainer']/div/div[2]/div[2]/input"))
            driver.type(r"xpath=>//*[@id='toContainer']/div/div[2]/div[2]/input", self.receiver)

            time.sleep(3)
            print('输入主题: %r' %driver.get_display(r"xpath=>//input[@id='txtSubject']"))
            # driver.click(r"xpath=>//input[@id='txtSubject']")
            driver.type(r"xpath=>//input[@id='txtSubject']", subject)


            print('点击发送')
            driver.click("id=>topSend")
            
#             print('等待完成')
#             driver.element_wait(r"xpath=>//*[@id='snedStatus']", 10)
            start = time.time()
            time.sleep(1)

        except BaseException as e:
            print('运行出错！！！')
            
            # driver.get_windows_img(r"D:\%s.jpg " %(start))
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
    
    def receiveAction(self, subject="cctv"):
        w = self.driver.get_window_size()['width']
        '''接收邮件时延'''
        r = WebReceive(self.username,self.pwd,self.receiver)
        print('=>接收邮件时延')
        start = r.sendEmail(subject=subject)
        # BaseAdb.adb_entry2(subject)
        # print("下拉")
        self.driver.swipe_down()

        print('=>等待本域邮件出现')
        isReceived = self.waitforEmail(subject,120)
        end = time.time()

        # BaseAdb.adb_entry3(subject)
        valueTime = str(round((end - start), 2))
        print('[接收本域邮件时延]: %r'  %valueTime)
        
        # 如果出现未读邮件，进行删除第一封邮件
        if isReceived:
            
            time.sleep(8)
            h = 400
            print('=>查找第一封邮件位置')
            if self.driver.get_element("id=>android:id/list") != None:
                els = self.driver.get_sub_element("id=>android:id/list","class=>android.widget.LinearLayout")
                h = els[0].location['y']
                
            self.driver.swipe(w - 20, h, 20, h, 500)
            print("=>右滑删除")
            time.sleep(2)
            
            print('=>点击删除')
            self.driver.click("id=>cn.cj.pe:id/item_view_back_four")    
            time.sleep(2)
        
        return valueTime
    
    
    def waitforEmail(self, subject="cctv",timeouts = 30):
        '''等待邮件出现'''
        timeout = int(round(time.time() * 1000)) + timeouts * 1000
        try:

            while (int(round(time.time() * 1000) < timeout)):
                print('wait.....')
                if self.driver.get_element("uiautomator=>"+subject,1) != None :
                    print('find it')
                    return True
                else:
                    self.driver.swipe_down()
                    pass
                
                time.sleep(0.1)
        except BaseException as msg:
            print(msg)
            self.driver.swipe_down()
        
        else:
            # self.driver.swipeDown() # 超时 下拉
#             print('time out')
            return False 


if __name__ == '__main__':

    
    for i in range(1):
        t1 = time.time()
        r = WebReceive('13697485262', 'chinasoft123','13580491603@139.com')
        start = r.sendEmail()
        time.sleep(1)
        print(start)
        t2 = time.time()
        valueTime = str(round((t2 - t1), 2))
        print('时间差: %r' %valueTime)