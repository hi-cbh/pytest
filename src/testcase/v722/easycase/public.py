# urs/bin/python
# encoding:utf-8

import time

class PublicUtil(object):
    
    def loadEmail(self, driver):
        '''加载本地100封邮件'''
        timeout = int(round(time.time() * 1000)) + 5*60 * 1000
        starttime = int(round(time.time() * 1000)) + 2*60 * 1000
        # 找到“已没有更多邮件”结束
        while int(round(time.time() * 1000)) < timeout :
            
            el = driver.element_wait(u"name=>加载更多邮件",secs = 1)
            if el != None:
                print("滑动")
                driver.swipeUp()
                print("点击")
                el.click()
                
            print("滑动")    
            driver.swipeUp()
            print("滑动")
            driver.swipeUp()
            print("滑动")
            driver.swipeUp()
                        
            print("2分钟后，开始判断")
            if int(round(time.time() * 1000)) < starttime :
                continue
            print("判断是否结束")
            if driver.element_wait(u"name=>已没有更多邮件",secs = 1) != None :
                break

PublicUtil = PublicUtil()   