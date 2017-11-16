# urs/bin/python
# encoding:utf-8

import time
import unittest
from src.base.baseAdb import BaseAdb
from src.base.baseFile import BaseFile

class OpenDown(unittest.TestCase):
    
    def __init__(self,driver, path, filename):
        self.driver = driver
        self.path = path
        self.filename = filename
        
    def openAction(self):
        '''打开未读邮件时延'''
        print('休眠10秒')
        time.sleep(6)
        # 下拉
        print('下拉')
        self.driver.swipeDown()
        time.sleep(3)
        try:
            # 点击第一封
            print('=>点击第一封邮件')
            els = self.driver.get_sub_element(r"id=>android:id/list","class=>android.widget.LinearLayout")
            time.sleep(2)
            
            print('=>记录当前时间，并点击开始')
            start = time.time()
            els[0].click()

            print('=>查找控件，确认进入邮件详情页')
            self.assertTrue(self.driver.element_wait(r"id=>cn.cj.pe:id/circular_progress_container") != None , "测试邮件不存在!")
            self.driver.element_wait(r"class=>android.widget.GridView")
            self.driver.element_wait(r"class=>android.webkit.WebView")
            
            print('=>记录当前时间，控件已查找完成')
            end = time.time()
            valueTime = str(round((end - start), 2))
            print(u'[打开未读邮件时延]: %r'  %valueTime)

        except BaseException as e:
            print(e)
            print('打开未读邮件出错！！！')
            return 0

        else:
            time.sleep(2)
            return valueTime
        
        
        
    def downAction(self):
        '''下载文件时延'''
        try:
            # 清除
            print('=>清除下载的旧数据')
            if BaseFile.adbFindFile(self.path, self.filename):
                BaseFile.adbDeleteFile(self.path, self.filename)
                 
            time.sleep(3)
             
            # 点击全部下载
            print('=>点击全部下载')
            self.driver.click(r"id=>cn.cj.pe:id/message_detail_attachment_download")
            start = time.time()
             
            # 等待文件出现
            print('=>等待文件出现')
            BaseFile.waitforfile(self.path, self.filename, 120)
             
            end = time.time()
             
            valueTime = str(round((end - start), 2))
            print('[下载附件时延]: %r'  %valueTime)
            print('=>返回收件箱')
            BaseAdb.adbBack()
            BaseAdb.adbBack()
            time.sleep(2)
            return valueTime
        except BaseException:
            print('下载附件出错了！！！')
            BaseAdb.adbBack()
            return 0
         
    # 设置收件箱列表的邮件为未读邮件
    def setFirstEmail(self):
        
        width = self.driver.get_window_size()['width']
        
        # 第一封邮件
        print('=>第一封邮件')
        if self.driver.get_element("id=>android:id/list") != None:
            els = self.driver.get_sub_element("id=>android:id/list", "class=>android.widget.LinearLayout") 
            h = els[0].location['y']
            
        time.sleep(2)
        print('=>右滑')
        self.driver.swipe(width - 20, h, 20, h, 500)
        time.sleep(2)
        
        print('=>设置未读')
        if self.driver.get_element(u"uiautomator=>未读") != None:
            self.driver.click(u"uiautomator=>未读")
        else:
            self.driver.swipe(20, h, width - 20, h, 500) 
            
        time.sleep(2)   
            
            
        