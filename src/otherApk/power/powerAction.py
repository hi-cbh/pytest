# urs/bin/python
# encoding:utf-8
import time
from src.base.baseAdb import BaseAdb as ba
from src.base.baseConversion import BaseConversion as bc
class PowerAction(object):
    
    def __init__(self, driver):
        self.driver = driver

        
    def executePreset(self):
        '''重置，并启动'''
        ba.adbClear("edu.umich.PowerTutor")
        time.sleep(2)
        
        ba.adbStartApp("edu.umich.PowerTutor","edu.umich.PowerTutor.ui.UMLogger")
        time.sleep(2)
        
        #重置app后，首次进入，点击按钮
        self.driver.click("uiautomator=>Ok")
        self.driver.click("uiautomator=>Agree")
        
        #点击开始记录按钮
        self.driver.click("id=>edu.umich.PowerTutor:id/servicestartbutton")
        
        
        # 点击application viewer
        self.driver.click("id=>edu.umich.PowerTutor:id/appviewerbutton")
        
        # 点击取消 LCD、wifi、3G监控
        self.driver.click("uiautomator=>LCD")
        self.driver.click("uiautomator=>Wifi")
        self.driver.click("uiautomator=>3G")
        
        time.sleep(2)
        ba.adbBack()
        
        #点击开始记录按钮
        self.driver.click("id=>edu.umich.PowerTutor:id/servicestartbutton")
        
        time.sleep(2)
        
        #点击开始记录按钮
        self.driver.click("id=>edu.umich.PowerTutor:id/servicestartbutton")
        
        ba.adbHome()
        time.sleep(2)
        
    def executeRecord(self, findText, isClear = True):    
        '''记录数据'''
        ba.adbHome()
        time.sleep(2)
        
        ba.adbStartApp("edu.umich.PowerTutor","edu.umich.PowerTutor.ui.UMLogger")
        time.sleep(2)
        
        # 点击application viewer
        print("application viewer")
        self.driver.click("id=>edu.umich.PowerTutor:id/appviewerbutton")  
        time.sleep(5)
        # 滑动屏幕找到目标
        
        
        # 获取电量值
        print("获取电量值")
        t = r"xpath=>//android.widget.TextView[contains(@text,'%s')]" %findText
        powerTxt = self.driver.get_attribute(t, "text")
        print(powerTxt)
        
        
        # 返回上一层
        ba.adbBack()
        
        # 清除数据
        if isClear:
            #点击开始记录按钮
            self.driver.click("id=>edu.umich.PowerTutor:id/servicestartbutton")
        
        ba.adbHome()
        
        # 获取数值      
        l = bc.findDigit(powerTxt)
        powervalue = l[-1]
        
        # 单位统一
        if "mJ" in powerTxt:
            powervalue = round((float(powervalue)/1000), 3)
        else:
            powervalue = float(powervalue)
    
        print(powervalue)
        return powervalue
        
        
        
        
        
        
        
        
        