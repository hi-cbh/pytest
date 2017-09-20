# urs/bin/python
# encoding:utf-8

import time
from base.baseAdb import BaseAdb
from base.baseFile import BaseFile
from base.baseOperate import Commom as c
from selenium.webdriver.common.by import By


class OpenDown(object):
    
    def __init__(self,driver, path, filename):
        self.driver = driver
        self.path = path
        self.filename = filename
        
    def openAction(self):
        '''打开未读邮件时延'''
        print('休眠5秒')
        time.sleep(5)
        
        # 下拉
        print('下拉')
        c.swipeDown(self.driver)
        
        try:
            # 点击第一封
            print('点击第一封邮件')
            ls = c.waitForElement(self.driver, By.ID, "android:id/list", 5)
            els = ls.find_elements_by_class_name("android.widget.LinearLayout")
            time.sleep(2)
            
            start = time.time()
            els[0].click()
            
            print('查找控件，确认进入邮件详情页')
            c.waitForElement(self.driver, By.ID, "cn.cj.pe:id/circular_progress_container",10)
    #         c.waitForElement(self.driver, By.ID, "android.widget.GridView",10)
    #         c.waitForElement(self.driver, By.ID, "android.webkit.WebView",10)
            
            end = time.time()
            valueTime = str(round((end - start), 2))
            print('时间差: %r'  %valueTime)
            
            time.sleep(2)
            return valueTime
    
        except BaseException:
            print('下载附件出错了！！！')
            return 0
        
        
        
    def downAction(self):
        '''下载文件时延'''
        
        try:
            # 清除
            print('清除下载的旧数据')
            if BaseFile.adbFindFile(self.path, self.filename):
                BaseFile.adbDeleteFile(self.path, self.filename)
    #             print('delete')
                
            time.sleep(3)
            
            # 点击全部下载
            print('点击全部下载')
            c.waitForElement(self.driver, By.ID, "cn.cj.pe:id/message_detail_attachment_download", 5).click()
            start = time.time()
            
            # 等待文件出现
            print('等待文件出现')
            BaseFile.waitforfile(self.path, self.filename, 120)
            
            end = time.time()
            
            valueTime = str(round((end - start), 2))
            print('时间差: %r'  %valueTime)
            BaseAdb.adbBack()
            return valueTime
        except BaseException:
            print('下载附件出错了！！！')
            BaseAdb.adbBack()
            return 0
        
        
        
        