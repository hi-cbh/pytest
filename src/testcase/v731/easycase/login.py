# urs/bin/python
# encoding:utf-8

import time
from src.base.baseAdb import BaseAdb


class Login(object):
    
    def __init__(self,driver, username, pwd):
        self.username = username
        self.pwd = pwd
        self.driver = driver
        
    def loginAction(self, firstLogin=False):
        '''最基础的登录'''
        self.driver.reset()

        self.driver.click(u"uiautomator=>开始使用")

        time.sleep(4)
        if firstLogin == True:
            self.driver.click(u"uiautomator=>允许")
            time.sleep(4)

        self.driver.swipeRight()
        self.driver.swipeRight()
        # self.driver.swipeRight()
        # self.driver.swipeRight()
        print("点击坐标")
        # BaseAdb.adbTap(700, 2200)  # vivo 1603  w * 0.5, h * 0.885

        w = self.driver.get_window_size()['width']
        h = self.driver.get_window_size()['height']

        BaseAdb.adb_tap(w / 2, int(h * 0.94))
        # BaseAdb.adb_tap(w / 2, int(h * 0.889))
        # BaseAdb.adbTap(500, 1700) #其他手机需要调试

        time.sleep(4)
        
        print('=>选择139邮箱')
        self.driver.click(r"xpath=>//android.widget.ImageView[@index='0']")
        
        
        # 输入
        els = self.driver.get_elements("id=>cn.cj.pe:id/input")
        
        if els == None:
            raise "没有进入登录 页面"
                    
        print('=>输入用户名')
        # els[0].send_keys(self.username) # appium 1.4
        els[0].set_value(self.username)
        
         
        print('=>输入密码')
        # els[1].send_keys(self.pwd) # appium 1.4
        els[1].set_value(self.pwd)   # appium 1.6

        print('=>点击登录')
        loginButton = self.driver.get_element("id=>cn.cj.pe:id/login")

        print('=>记录当前时间、点击登录')
        start = time.time()
        loginButton.click()

        if firstLogin == True:
            self.driver.click(u"uiautomator=>允许")
            time.sleep(1)


        print('=>等待体验按钮出现，并记录当前时间')
        self.driver.get_element("id=>cn.cj.pe:id/message_list_bottom_email")
        end = time.time()
         
        valueTime = str(round((end - start), 2))
        print('[登录时延]: %r'  %valueTime)
        return valueTime

        
        # 用于记录时延的登录操作
    def loginActionTime(self):
        
        logintime = self.loginAction()   
        
        # 下拉
        time.sleep(4)
        self.driver.swipeDown()
        time.sleep(4)
        
        # 邮件设置
        self.setEmailOption(False, True)
    
        time.sleep(2)
        
        
        return logintime
         
        # 用于记录CPU、内存峰值
    def loginActionPeakValue(self):    
                
        self.loginAction()   
        
        # 邮件设置
        self.setEmailOption(True, False)
    
        time.sleep(2)
        
    def loginActionLoginFlow(self):    
        '''用于首次登录流量'''        
        self.loginAction()  
        
    
    def setEmailOption(self, isNotice, isSetting):
        '''邮件设置'''
        # 点击我的
        print('=>点击我的')
        self.driver.click("id=>cn.cj.pe:id/message_list_bottom_mine")
        
        # 点击设置
        print('=>点击设置')
        # self.driver.click(u"name=>设置") # appium 1.4
        self.driver.click(u"uiautomator=>设置") # appium 1.6
        
        
        
        if isNotice:
            print('==>通知设置')
            self.setEmailNotice()
        
        
        if isSetting:
            print('==>下载图片设置')
            self.setEmailSetting()          
        
        print('=>返回设置页面')
        BaseAdb.adb_back()
#         time.sleep(2)
        print('=>返回收件箱')
        self.driver.click("id=>cn.cj.pe:id/message_list_bottom_email")
        
        #设置邮件提示设置
    def setEmailNotice(self):
        # time.sleep(1) appium 1.4
        # self.driver.click(u"name=>邮件提示设置")
        # time.sleep(1)
        # self.driver.click(u"name=>显示邮件发送页")
        # time.sleep(1)
        # self.driver.click(u"name=>显示邮件通知")
#         time.sleep(1)
        time.sleep(1)
        self.driver.click(u"uiautomator=>邮件提示设置")
        #         time.sleep(1)
        self.driver.click(u"uiautomator=>显示邮件发送页")
        #         time.sleep(1)
        self.driver.click(u"uiautomator=>显示邮件通知")
        #         time.sleep(1)
        BaseAdb.adb_back()
        
        
        # 开启收邮件设置：自动下载邮件图片
    def setEmailSetting(self):
#         time.sleep(1) appium 1.4
#         self.driver.click(u"name=>收取邮件设置")
# #         time.sleep(1)
#         self.driver.click(u"name=>数据网络下自动下载邮件图片")
# #         time.sleep(1)
        time.sleep(1)
        self.driver.click(u"uiautomator=>收取邮件设置")
#         time.sleep(1)
        self.driver.click(u"uiautomator=>数据网络下自动下载邮件图片")
#         time.sleep(1)
        self.driver.click(r"id=>cn.cj.pe:id/hjl_headicon")
        time.sleep(2)     