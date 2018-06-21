# urs/bin/python
# encoding:utf-8
import time
from src.base.baseAdb import BaseAdb as ba
from src.base.baseConversion import BaseConversion as bc
class PowerAction(object):
    
    def __init__(self, driver):
        self.driver = driver

        
    def exec_preset(self):
        '''重置，并启动'''
        ba.adb_clear("edu.umich.PowerTutor")
        time.sleep(2)
        
        ba.adb_start_app("edu.umich.PowerTutor", "edu.umich.PowerTutor.ui.UMLogger")
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
        ba.adb_back()
        
        #点击开始记录按钮
        self.driver.click("id=>edu.umich.PowerTutor:id/servicestartbutton")
        
        time.sleep(2)
        
        #点击开始记录按钮
        self.driver.click("id=>edu.umich.PowerTutor:id/servicestartbutton")
        
        ba.adb_home()
        time.sleep(2)
        
    def exec_record(self, find_text, is_clear = True):
        try:
            '''记录数据'''
            ba.adb_home()
            time.sleep(2)

            ba.adb_start_app("edu.umich.PowerTutor", "edu.umich.PowerTutor.ui.UMLogger")
            time.sleep(2)

            # 点击application viewer
            print("application viewer")
            self.driver.click("id=>edu.umich.PowerTutor:id/appviewerbutton")
            time.sleep(5)
            # 滑动屏幕找到目标


            # 获取电量值
            print("获取电量值")
            t = r"xpath=>//android.widget.TextView[contains(@text,'%s')]" % find_text
            power_txt = self.driver.get_attribute(t, "text")
            print(power_txt)


            # 返回上一层
            ba.adb_back()

            # 清除数据
            if is_clear:
                #点击开始记录按钮
                self.driver.click("id=>edu.umich.PowerTutor:id/servicestartbutton")

            ba.adb_home()

            # 获取数值
            l = bc.find_digit(power_txt)
            powervalue = l[-1]

            # 单位统一
            if "mJ" in power_txt:
                powervalue = round((float(powervalue)/1000), 3)
            else:
                powervalue = float(powervalue)

            print(powervalue)
            return powervalue
        except BaseException :
            print("获取电量出错-返回0")
            return 0

        
        
        
        
        
        
        
        