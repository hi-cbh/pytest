# urs/bin/python
# encoding:utf-8

import time
from src.base.baseAdb import BaseAdb
from src.base.baseFile import BaseFile
from src.otherApk.gt.gtutil import GTTest


class Send(object):
    
    def __init__(self,driver, username):
        self.username = username
        self.driver = driver
        
    def sendActionPeakValue(self, firstLogin=False):
        '''记录CPU、MEM'''
        width = self.driver.get_window_size()['width']
        try:
            # 点击写邮件按钮
            print('=>点击写邮件按钮')
            self.driver.click(r"id=>cn.cj.pe:id/actionbar_right_view")
            # 收件人输入内容
            print('=>收件人输入内容')
            self.driver.set_value(r"id=>cn.cj.pe:id/to_wrapper",self.username)
            # 点击空白地方
            print('=>点击空白地方')
            self.driver.click(r"id=>cn.cj.pe:id/actionbar_title_sub")
            
            # 输入主题
            print('=>输入主题') # testReceive
            self.driver.set_value(r"id=>cn.cj.pe:id/subject",'testReceive')

            # 输入邮件内容
            print('=>输入邮件内容')
            self.driver.set_value(r"id=>cn.cj.pe:id/message_content",'123456789012345678901234567890')
              
            # 添加附件
            print('=>添加附件')
            self.driver.click(r"id=>cn.cj.pe:id/add_attachment")
            self.driver.click(u"uiautomator=>本地文件夹")
            self.driver.click(r"uiautomator=>0")
            self.driver.click(r"uiautomator=>0.")
            self.driver.click(r"uiautomator=>test2M.rar")
            self.driver.click(r"id=>cn.cj.pe:id/check_button")
         
            time.sleep(5)
            gt = GTTest("cn.cj.pe")
            gt.startGT()
         
            # 点击发送按钮
            print('=>点击发送按钮，开始计时')
            el = self.driver.get_element("id=>cn.cj.pe:id/txt_send")
            BaseAdb.adb_broadcast()
            el.click()

            print('等待文件更新')
            bl = BaseFile.wait_for_file_modify(30)
            time.sleep(3)
            print('查找页面是否出现新邮件')
            bl2 = self.driver.element_wait('uiautomator=>testReceive')

            if (bl2==None) or (bl == False) :
                self.driver.swipeDown()
            
            time.sleep(8)
            
            data = []
            data = gt.endGT()
#             print(data)
            time.sleep(2)
     
            if self.driver.element_wait('uiautomator=>testReceive') != None:
                h = 400
                print('=>查找第一封邮件位置')
                if self.driver.get_element("id=>android:id/list") != None:
                    els = self.driver.get_sub_element("id=>android:id/list","class=>android.widget.LinearLayout")
                    h = els[0].location['y']
                    
                self.driver.swipe(width - 20, h, 20, h, 500)
                print("=>右滑删除")
                time.sleep(2)
                
                print('=>点击删除')
                self.driver.click("id=>cn.cj.pe:id/item_view_back_four")    
            

        except BaseException as error:
            print(error)
            print('发送邮件出错了！！！')
            return 0

        else:
            time.sleep(2)
            return data

    def sendAction(self):
        '''正常的发送邮件'''
        try:
            # 点击写邮件按钮
            print('=>点击写邮件按钮')
            self.driver.click(r"id=>cn.cj.pe:id/actionbar_right_view")
            # 收件人输入内容
            print('=>收件人输入内容')
            self.driver.set_value(r"id=>cn.cj.pe:id/to_wrapper",self.username) # appium 1.6
            # 点击空白地方
            print('=>点击空白地方')
            self.driver.click(r"id=>cn.cj.pe:id/actionbar_title_sub")
            
            # 输入主题
            print('=>输入主题')
            self.driver.set_value(r"id=>cn.cj.pe:id/subject",'test') # appium 1.6

            # 输入邮件内容
            print('=>输入邮件内容')
            self.driver.set_value(r"id=>cn.cj.pe:id/message_content",'123456789012345678901234567890') # appium 1.6
              
            # 添加附件
            print('=>添加附件')
            self.driver.click(r"id=>cn.cj.pe:id/add_attachment")
            self.driver.click(u"uiautomator=>本地文件夹") # appium 1.6
            self.driver.click(r"uiautomator=>0")
            self.driver.click(r"uiautomator=>0.")
            self.driver.click(r"uiautomator=>test2M.rar")
            self.driver.click(r"id=>cn.cj.pe:id/check_button")
         
         
            # 点击发送按钮
            print('=>点击发送按钮，开始计时')
            el = self.driver.get_element("id=>cn.cj.pe:id/txt_send")
            start = time.time()
            
            el.click()
            
            print('=>等待已完成出现，并记录时间')
            self.driver.element_wait(u"uiautomator=>已完成",120) # appium 1.6
            end = time.time()
            
            valueTime = str(round((end - start), 2))
            print('[发送邮件时延]: %r'  %valueTime)
            
            print('返回收件箱')
            BaseAdb.adb_back()
            time.sleep(2)
            return valueTime
        except BaseException:
            print('发送邮件出错了！！！')
            return 0   

        