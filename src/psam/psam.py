# coding=utf-8

import time
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from base.baseAdb import BaseAdb
from base.baseFile import BaseFile
from base.baseImage import BaseImage

class Psam(object):
    
    def __init__(self, version="6.0",apk='cn.cj.pe',ativity='com.mail139.about.LaunchActivity'):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = version
        desired_caps['deviceName'] = 'android'
        desired_caps['appPackage'] = apk
        desired_caps['appActivity'] = ativity
        desired_caps['newCommandTimeout'] = 7200
        desired_caps["unicodeKeyboard"] = "True"
        desired_caps["resetKeyboard"] = "True"
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
#         self.driver.implicitly_wait(10)
    
    def element_wait(self, css, secs = 10):
        '''
        Waiting for an element to display.

        Usage:
        driver.element_wait("css=>#el",10)
        '''
        if "=>" not in css:
            raise NameError("Positioning syntax errors, lack of '=>'.")

        by = css.split("=>")[0]
        value = css.split("=>")[1]
#         print('[%s] finding it！' %value)
#         print("等待秒数：%d" %secs )
        
        el = None
        try:
            if by == "id":
                el = WebDriverWait(self.driver,secs,1).until(EC.presence_of_element_located((By.ID, value)))
            elif by == "name":
                el = WebDriverWait(self.driver,secs,1).until(EC.presence_of_element_located((By.NAME, value)))
            elif by == "class":
                el = WebDriverWait(self.driver,secs,1).until(EC.presence_of_element_located((By.CLASS_NAME, value)))
            elif by == "link_text":
                el = WebDriverWait(self.driver,secs,1).until(EC.presence_of_element_located((By.LINK_TEXT, value)))
            elif by == "xpath":
                el = WebDriverWait(self.driver,secs,1).until(EC.presence_of_element_located((By.XPATH, value)))
            elif by == "css":
                el = WebDriverWait(self.driver,secs,1).until(EC.presence_of_element_located((By.CSS_SELECTOR, value)))
            elif by == "uiautomator":
                el = WebDriverWait(self.driver,10,1).until(EC.presence_of_element_located((By.ANDROID_UIAUTOMATOR, u'new UiSelector().text("%s")' %value)))
            else:
                raise NameError("Please enter the correct targeting elements,'id','name','class','link_text','xpath','css', 'uiautomator'.")
            return el
        except BaseException as e:
            print('[%s] can not find it！' %value)
            return None    
        
    
    def get_element(self,css, secs=30):
        
        self.element_wait(css, secs)
        '''
        Judge element positioning way, and returns the element.
        '''
        if "=>" not in css:
            raise NameError("Positioning syntax errors, lack of '=>'.")

        by = css.split("=>")[0]
        value = css.split("=>")[1]
        try:
            if by == "id":
                element = self.driver.find_element_by_id(value)
            elif by == "name":
                element = self.driver.find_element_by_name(value)
            elif by == "class":
                element = self.driver.find_element_by_class_name(value)
            elif by == "link_text":
                element = self.driver.find_element_by_link_text(value)
            elif by == "xpath":
                element = self.driver.find_element_by_xpath(value)
            elif by == "css":
                element = self.driver.find_element_by_css_selector(value)
            elif by == "uiautomator":
                element = self.driver.find_element_by_android_uiautomator(u'new UiSelector().text("%s")' %value)
            else:
                raise NameError("Please enter the correct targeting elements,'id','name','class','link_text','xpath','css'.")
            return element
        except BaseException as error:
            return None 


    def get_elements(self,css,secs=30 ):
             
        self.element_wait(css, secs)
        '''
        Judge element positioning way, and returns the element.
        '''
        if "=>" not in css:
            raise NameError("Positioning syntax errors, lack of '=>'.")

        by = css.split("=>")[0]
        value = css.split("=>")[1]
        try:
            if by == "id":
                elements = self.driver.find_elements_by_id(value)
            elif by == "name":
                elements = self.driver.find_elements_by_name(value)
            elif by == "class":
                elements = self.driver.find_elements_by_class_name(value)
            elif by == "link_text":
                elements = self.driver.find_elements_by_link_text(value)
            elif by == "xpath":
                elements = self.driver.find_elements_by_xpath(value)
            elif by == "css":
                elements = self.driver.find_elements_by_css_selector(value)
            elif by == "uiautomator":
                elements = self.driver.find_elements_by_android_uiautomator(u'new UiSelector().text("%s")' %value)
            else:
                raise NameError("Please enter the correct targeting elements,'id','name','class','link_text','xpath','css'.")
            return elements
        
        except BaseException as error:
            return None      
    
    def get_sub_element(self, css1, css2, secs=20):
        '''实现查找子控件'''
        self.element_wait(css2, secs)
        
        element = self.get_element(css1, secs)

        if "=>" not in css2:
            raise NameError("Positioning syntax errors, lack of '=>'.")

        by = css2.split("=>")[0]
        value = css2.split("=>")[1]
        
        try:
            if by == "id":
                elements = element.find_elements_by_id(value)
            elif by == "name":
                elements = element.find_elements_by_name(value)
            elif by == "class":
                elements = element.find_elements_by_class_name(value)
            elif by == "link_text":
                elements = element.find_elements_by_link_text(value)
            elif by == "xpath":
                elements = element.find_elements_by_xpath(value)
            elif by == "css":
                elements = element.find_elements_by_css_selector(value)
            elif by == "uiautomator":
                elements = self.driver.find_element_by_android_uiautomator(u'new UiSelector().text("%s")' %value)
            else:
                raise NameError("Please enter the correct targeting elements,'id','name','class','link_text','xpath','css'.")
            return elements
        except BaseException as error:
            return None   

    def type(self, css, text):
        '''
        Operation input box.

        Usage:
        driver.type("css=>#el","selenium")
        '''
        self.element_wait(css)
        el = self.get_element(css)
        el.send_keys(text)

    def set_value(self, css, text):
        '''
        Operation input box. appium 1.6

        Usage:
        driver.type("css=>#el","selenium")
        '''
        self.element_wait(css)
        el = self.get_element(css)
        el.set_value(text)



    def clear(self, css):
        '''
        Clear the contents of the input box.

        Usage:
        driver.clear("css=>#el")
        '''
        self.element_wait(css)
        el = self.get_element(css)
        el.clear()

    def click(self, css,secs=10 ):
        '''
        It can click any text / image can be clicked
        Connection, check box, radio buttons, and even drop-down box etc..

        Usage:
        driver.click("css=>#el")
        '''
        self.element_wait(css,secs)
        el = self.get_element(css,secs)
        if el == None:
            print("%s 元素为None" %css)
            return
        el.click()    

    def get_attribute(self, css, attribute):
        '''
        Gets the value of an element attribute.

        Usage:
        driver.get_attribute("css=>#el","type")
        '''
        el = self.get_element(css)
        return el.get_attribute(attribute)

    def get_text(self, css):
        '''
        Get element text information.

        Usage:
        driver.get_text("css=>#el")
        '''
        self.element_wait(css)
        el = self.get_element(css)
        return el.text

    def get_display(self, css):
        '''
        Gets the element to display,The return result is true or false.

        Usage:
        driver.get_display("css=>#el")
        '''
        self.element_wait(css)
        el = self.get_element(css)
        return el.is_displayed()

    def reset(self):
        '''
                    重置 app
        '''
        self.driver.reset()
 

    def swipeUp(self):
        '''向上滑动'''
        width = self.driver.get_window_size()['width']
        height = self.driver.get_window_size()['height']        
        self.driver.swipe(width / 5, height * 4 / 5, width / 5, height / 5,
                500)
        time.sleep(1)

 
    def swipeDown(self):
        '''向下滑动'''
        width = self.driver.get_window_size()['width']
        height = self.driver.get_window_size()['height']        
        self.driver.swipe(width / 5, height / 5, width / 5, height * 4 / 5,
                500)
        time.sleep(2)

    def swipeRight(self):
        '''向右滑动'''
        width = self.driver.get_window_size()['width']
        height = self.driver.get_window_size()['height']
        self.driver.swipe(width - 50, height / 2, 50, height /2 ,
                          500)
        time.sleep(1)

    def get_window_size(self):
        width = self.driver.get_window_size()['width']
        height = self.driver.get_window_size()['height']
        return {'width':width, 'height':height}

    def quit(self):
        '''
        Quit the driver and close all the windows.

        Usage:
        driver.quit()
        '''
        self.driver.quit()        
        

    def swipe(self,start_x, start_y, end_x, end_y, duration):
        '''滑动'''
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)

    
    def screenshot(self,filename):
        '''截屏'''
        self.driver.save_screenshot(filename)

    def implicitly_wait(self, secs = 10):
        '''隐式等待'''
        self.driver.implicitly_wait(secs)

    def uiautomator(self,uia_string):
        return self.driver.find_element_by_android_uiautomator(uia_string)
        # self.driver.find_element_by_android_uiautomator('new UiSelector().description("%s")' %uia_string)


    def page_source(self):
        return self.driver.page_source

    def login_action(self):
        # driver.reset()
        time.sleep(6)


        driver.swipeRight()
        driver.swipeRight()
        driver.swipeRight()

        driver.click("class=>android.widget.Button")

        time.sleep(2)

        driver.get_elements("class=>android.widget.ImageView")[0].click()

        time.sleep(5)

        # driver.click("name=>帐号密码登录")
        BaseAdb.adb_tap(500,510)
        BaseAdb.adb_input_text("2915673336")

        BaseAdb.adb_tap(500,700)
        BaseAdb.adb_input_text("ctctest2014")

        BaseAdb.adb_tap(500,890)
        start_time = time.time()

        print("等待完成出现")
        driver.element_wait("xpath=>//android.widget.Button[contains(@text,'完成')]", 60)
        # driver.element_wait(u"uiautomator=>完成", 60)
        value_time = str(round(time.time() - start_time, 2))
        print("登录时延：%s" %value_time)

        driver.click("class=>android.widget.Button")
        # driver.click(u"uiautomator=>完成")

        time.sleep(2)




    def send(self):
        print("点击收件箱")
        driver.click("xpath=>//android.widget.TextView[contains(@text,'收件箱')]")

        print("点击新建")
        driver.click("xpath=>//android.widget.ImageButton[@content-desc='写邮件']")

        print("2915673336@qq.com")
        BaseAdb.adb_input_text("2915673336@qq.com")
        BaseAdb.adb_tap(600,600)

        BaseAdb.adb_tap(300,600)
        BaseAdb.adb_input_text("TestMail")


        BaseAdb.adb_tap(300, 900)
        BaseAdb.adb_input_text("123456789012345678901234567890")


        print("点击添加附件")
        driver.click("xpath=>//android.widget.Button[@content-desc='附件操作']")

        print("选择文件在")
        driver.click("xpath=>//android.widget.ImageButton[@content-desc='从文件浏览器选择文件']")


        print("获取路径")
        txt = driver.get_attribute("id=>com.tencent.androidqqmail:id/k","text")
        print("获取路径txt: %s" %txt)

        # 目录路径不对
        if not txt.__contains__("/0/0./"):
            driver.click("id=>com.tencent.androidqqmail:id/ru")
            driver.click("id=>com.tencent.androidqqmail:id/ru")
            driver.click(r"xpath=>//android.widget.TextView[contains(@text,'0.')]")

        print("选择文件")
        driver.click("xpath=>//android.widget.TextView[contains(@text,'test2M.rar')]")
        driver.click("xpath=>//android.widget.Button[contains(@text,'添加到邮件')]")

        time.sleep(5)
        print("点击发送")
        driver.click("xpath=>//android.widget.Button[contains(@text,'发送')]")
        start_time = time.time()


        time.sleep(3)
        time_out = int(round(time.time() * 1000)) + 1*60 * 1000

        # 获取邮件发送成功，退出；否则返回超时
        while int(round(time.time() * 1000)) < time_out :

            if BaseAdb.dumpsys_notification("邮件发送成功"):
                break

            time.sleep(0.1)

        end_time = time.time()

        value_time = str(round(end_time - start_time, 2))

        print("邮件发送时延：%s" %value_time)

        time.sleep(5)


    def down_file(self):
        print("点击收件箱")
        driver.click("xpath=>//android.widget.TextView[contains(@text,'收件箱')]")

        print("点击第一封邮件")
        ele_list = driver.get_elements("class=>android.widget.RelativeLayout")
        # 点击第第一封邮件
        ele_list[3].click()
        start_time = time.time()


        driver.element_wait("class=>android.webkit.WebView")
        end_time = time.time()

        value_time = str(round(end_time - start_time, 2))
        print("打开未读邮件时延：%s" %value_time)

        file_path = "/mnt/sdcard/Download/QQMail/test2M.*"
        file_name = "test2M"
        print("查找文件")
        if BaseFile.adb_find_file(file_path, file_name):
            print("清除文件")
            BaseFile.adb_del_file(file_path, file_name)

        print("点击更多")
        BaseAdb.adb_tap_per(driver, 940/1080, 1590/1920)

        print("保存文件")
        driver.click("xpath=>//android.widget.TextView[contains(@text,'保存文件')]")

        print("在download目录")
        if not driver.get_attribute("id=>com.tencent.androidqqmail:id/ru","text").__contains__("Download"):
            driver.click("id=>com.tencent.androidqqmail:id/ru")

        print("点击保存")
        driver.click("xpath=>//android.widget.Button[contains(@text,'保存')]")
        start_time = time.time()

        print("等待邮件出现")
        BaseFile.wait_for_file(file_path,file_name)

        end_time = time.time()

        value_time = str(round(end_time - start_time, 2))
        print("下载附件时延：%s" %value_time)


        print("查找文件")
        if BaseFile.adb_find_file(file_path, file_name):
            print("清除文件")
            BaseFile.adb_del_file(file_path, file_name)


        time.sleep(5)
        BaseAdb.adb_back()

if __name__ == '__main__':

    driver = Psam(version="5.1",apk="com.tencent.androidqqmail",ativity="com.tencent.qqmail.launcher.desktop.LauncherActivity")

    driver.login_action()

    # driver.send()
    print("点击收件箱")
    driver.click("xpath=>//android.widget.TextView[contains(@text,'收件箱')]")

    txt = driver.get_element("xpath=>//android.view.View[contains(@content-desc,'TestMailQQ')]")
    txt.click()

    time.sleep(4)















