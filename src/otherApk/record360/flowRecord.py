# urs/bin/python
# encoding:utf-8

import re
import time
from src.base.baseAdb import BaseAdb
from src.base.baseConversion import BaseConversion as bc
from src.base.baseImage import BaseImage


class FlowRecord360Action(object):
    
    def __init__(self, driver):
        self.driver = driver
    
    def exec_preset(self):
        '''记录流量前，运行360记录流量做准备，预置环境'''
        
        network = BaseAdb.get_network_type()
        # 清除缓存
        BaseAdb.adb_clear("com.qihoo360.mobilesafe")
        time.sleep(2)
        # 启动360卫士
        BaseAdb.adb_start_app("com.qihoo360.mobilesafe",
                    "com.qihoo360.mobilesafe.ui.index.AppEnterActivity")
        time.sleep(3)
        # 点击取消
        self.driver.click(r"id=>com.qihoo360.mobilesafe:id/btn_privacy_confirm")
       
        # 点击左按钮
        if self.driver.element_wait(r"id=>com.qihoo360.mobilesafe:id/common_btn_left",5) != None:
            self.driver.click(r"id=>com.qihoo360.mobilesafe:id/common_btn_left")

        # 点击左按钮
        if self.driver.element_wait(r"id=>com.qihoo360.mobilesafe:id/common_btn_left",5) != None:
            self.driver.click(r"id=>com.qihoo360.mobilesafe:id/common_btn_left")

        self.close_suspension()
        
        # 点击话费与流量
        self.driver.click(u"uiautomator=>话费•流量")
        # 点击软件流量管理
        self.driver.click(u"uiautomator=>软件流量管理")
        # 点击 2G/3G/4G消耗
        self.driver.click(r"uiautomator=>2G/3G/4G消耗")
        
        self.click_network(network)
        
        time.sleep(1)
        BaseAdb.adb_back()

        # 点击设置按钮
        self.driver.click(r"id=>com.qihoo360.mobilesafe:id/common_img_setting")
        
        self.click_clearbtn()
        
        time.sleep(1)
        BaseAdb.adb_back()
        BaseAdb.adb_back()
        BaseAdb.adb_home()
        time.sleep(1)
    
    def exec_record(self, findtxt, network, is_image, is_clear=True):
        try:
            '''记录流量值,添加是否截图参数，记录后清除数据'''
            BaseAdb.adb_start_app("com.qihoo360.mobilesafe",
                    "com.qihoo360.mobilesafe.ui.index.AppEnterActivity")

            time.sleep(5)

            # 点击话费与流量
            self.driver.click(u"id=>com.qihoo360.mobilesafe:id/exam_selected_tool_item_2")
            # 点击软件流量管理
            self.driver.click(u"uiautomator=>软件流量管理")

            self.click_flow_stype()

            self.click_network(network)

            if is_image:
                BaseImage.screenshot(self.driver, "FlowPic")

            print("获取流量值：")
            strflowtotal = self.get_flow_message(findtxt)

            time.sleep(2)
            BaseAdb.adb_back()

            if is_clear:
                # 点击设置按钮
                self.driver.click(r"id=>com.qihoo360.mobilesafe:id/common_img_setting")

                self.click_clearbtn()

                time.sleep(2)
                BaseAdb.adb_back()

            BaseAdb.adb_back()
            BaseAdb.adb_home()
            time.sleep(1)
            return strflowtotal
        except BaseException as e:
            print("记录数据出错了")
            BaseAdb.adb_back()
            BaseAdb.adb_back()
            BaseAdb.adb_home()
            time.sleep(1)
            return None
    
    def click_flow_stype(self):
        '''点击 监控消耗类型'''
        els = self.driver.get_sub_element(r"id=>com.qihoo360.mobilesafe:id/common_popbtns", "class=>android.widget.TextView")
        els[1].click()
    
    
    def click_network(self, network):
        '''选择监控的网络类型'''
        button = self.driver.get_elements(r"id=>com.qihoo360.mobilesafe:id/common_row_title")
        if network == '4G':
            button[0].click()
        else:
            button[1].click()
    
    
    # 点击清空流量统计数据
    def click_clearbtn(self):
        self.driver.click(u"uiautomator=>清空流量统计数据")
        self.driver.click(u"uiautomator=>确定")
    
    # 获取流量值
    def get_flow_message(self, findtxt):
        ite = self.driver.get_element("uiautomator=>%s" %findtxt)
        
        # 这里存在风险，python scroll封装不完善
        if ite == None:
            self.driver.swipeDown()
        
        print("点击列表中的139")
        total_xpath = r"//android.widget.TextView[contains(@text,'%s')]/following-sibling::android.widget.TextView[1]" %findtxt
        self.driver.click("xpath=>%s" %total_xpath)
        
        # 总流量
        print("获取总流量")
        strflowtotal = self.driver.get_attribute("xpath=>%s" %total_xpath, "text")
        print('all: %s' %strflowtotal)
        
        flowupdown = ""
        if self.driver.element_wait(r"id=>com.qihoo360.mobilesafe:id/upload_value") != None:
            up = self.driver.get_attribute(r"id=>com.qihoo360.mobilesafe:id/upload_value","text")
            down = self.driver.get_attribute(r"id=>com.qihoo360.mobilesafe:id/load_value","text")
            
            flowupdown = up + "#" + down
            
        flow_str ={}
        l = bc.value_flow_k(flowupdown + "#" + strflowtotal)
        flow_str['up'] = l[0]
        flow_str['down'] = l[1]
        flow_str['all'] = l[2]
        
        print(flow_str)
        return flow_str
    
    # 关闭360悬浮球
    def close_suspension(self):
        self.driver.click(u"uiautomator=>隐私保护")
        
        self.driver.click(u"uiautomator=>卫士设置")
        
        self.driver.click(u"uiautomator=>悬浮窗")
        
        self.driver.click(u"uiautomator=>开启内存清理悬浮窗")
        
        time.sleep(2)
        
        BaseAdb.adb_back()
        
        BaseAdb.adb_back()
        
        self.driver.click(u"uiautomator=>常用功能")

    
    
    def find_digit(self, st):
        '''查找字符串中的数值'''
        return re.findall(r"\d+\.?\d*",st)
    
        