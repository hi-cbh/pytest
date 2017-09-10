# urs/bin/python
# encoding:utf-8

import time,re
from base.baseAdb import BaseAdb
from base.baseImage import BaseImage
from base.baseConversion import BaseConversion as bc
class FlowRecord360Action(object):
    
    def __init__(self, driver):
        self.driver = driver
    
    def executePreset(self):
        '''记录流量前，运行360记录流量做准备，预置环境'''
        
        network = BaseAdb.getNetworkType()
        # 清除缓存
        BaseAdb.adbClear("com.qihoo360.mobilesafe")
        time.sleep(2)
        # 启动360卫士
        BaseAdb.adbStartApp("com.qihoo360.mobilesafe",
                    "com.qihoo360.mobilesafe.ui.index.AppEnterActivity")
        time.sleep(3)
        # 点击取消
        self.driver.click(r"id=>com.qihoo360.mobilesafe:id/btn_privacy_confirm")
       
        # 点击左按钮
        if self.driver.element_wait(r"id=>com.qihoo360.mobilesafe:id/common_btn_left") != None:
            self.driver.click(r"id=>com.qihoo360.mobilesafe:id/common_btn_left")
       
#         time.sleep(2)
        
        self.closeSuspension()
        
        # 点击话费与流量
        self.driver.click(u"name=>话费•流量")
        # 点击软件流量管理
        self.driver.click(u"name=>软件流量管理")
        # 点击 2G/3G/4G消耗
        self.driver.click(r"name=>2G/3G/4G消耗")
        
        self.clickNetWork(network)
        
        time.sleep(1)
        BaseAdb.adbBack()

        # 点击设置按钮
        self.driver.click(r"id=>com.qihoo360.mobilesafe:id/common_img_setting")
        
        self.clickClearButton()
        
        time.sleep(1)
        BaseAdb.adbBack()
        BaseAdb.adbBack()
        BaseAdb.adbHome()
        time.sleep(1)
    
    def executeRecord(self, findtxt, network, isImage,isClear=True):
        '''记录流量值,添加是否截图参数，记录后清除数据'''
        BaseAdb.adbStartApp("com.qihoo360.mobilesafe",
                "com.qihoo360.mobilesafe.ui.index.AppEnterActivity")
        
        # 点击话费与流量
        self.driver.click(u"name=>话费•流量")
        # 点击软件流量管理
        self.driver.click(u"name=>软件流量管理")
        
        self.clickFlowStype()
        
        self.clickNetWork(network)
        
        if isImage:
            BaseImage.screenshot(self.driver, "FlowPic")
        
        print("获取流量值：")
        strflowtotal = self.getFlowMessage(findtxt)
        
        time.sleep(2)
        BaseAdb.adbBack()

        if isClear:
            # 点击设置按钮
            self.driver.click(r"id=>com.qihoo360.mobilesafe:id/common_img_setting")
            
            self.clickClearButton()
        
            time.sleep(2)
            BaseAdb.adbBack()
            
        BaseAdb.adbBack()
        BaseAdb.adbHome()
        time.sleep(1)
        return strflowtotal
    
    
    def clickFlowStype(self):
        '''点击 监控消耗类型'''
        els = self.driver.get_sub_element(r"id=>com.qihoo360.mobilesafe:id/common_popbtns", "class=>android.widget.TextView")
        els[1].click()
    
    
    def clickNetWork(self,network):
        '''选择监控的网络类型'''
        button = self.driver.get_elements(r"id=>com.qihoo360.mobilesafe:id/common_row_title")
        if network == '4G':
            button[0].click()
        else:
            button[1].click()
    
    
    # 点击清空流量统计数据
    def clickClearButton(self):
        self.driver.click(u"name=>清空流量统计数据")
        self.driver.click(u"name=>确定")
    
    # 获取流量值
    def getFlowMessage(self, findtxt):
        ite = self.driver.get_element("name=>%s" %findtxt)
        
        # 这里存在风险，python scroll封装不完善
        if ite == None:
            self.driver.swipeDown()
        
        print("点击列表中的139")
        totalXpath = r"//android.widget.TextView[contains(@text,'%s')]/following-sibling::android.widget.TextView[1]" %findtxt
        self.driver.click("xpath=>%s" %totalXpath)
        
        # 总流量
        print("获取总流量")
        strflowtotal = self.driver.get_attribute("xpath=>%s" %totalXpath, "text")
        print('all: %s' %strflowtotal)
        
        flowupdown = ""
        if self.driver.element_wait(r"id=>com.qihoo360.mobilesafe:id/upload_value") != None:
            up = self.driver.get_attribute(r"id=>com.qihoo360.mobilesafe:id/upload_value","text")
            down = self.driver.get_attribute(r"id=>com.qihoo360.mobilesafe:id/load_value","text")
            
            flowupdown = up + "#" + down
            
        flowStr ={}
        l = bc.valueFlowToK(flowupdown + "#" +strflowtotal)
        flowStr['up'] = l[0]
        flowStr['down'] = l[1]
        flowStr['all'] = l[2]
        
        print(flowStr)
        return flowStr
    
    # 关闭360悬浮球
    def closeSuspension(self):
        self.driver.click(u"name=>隐私保护")
        
        self.driver.click(u"name=>卫士设置")
        
        self.driver.click(u"name=>悬浮窗")
        
        self.driver.click(u"name=>开启内存清理悬浮窗")
        
        time.sleep(2)
        
        BaseAdb.adbBack()
        
        BaseAdb.adbBack()
        
        self.driver.click(u"name=>常用功能")
    
    
    
    def findDigit(self, st):
        '''查找字符串中的数值'''
        return re.findall(r"\d+\.?\d*",st)
    
        