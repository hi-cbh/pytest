# coding=utf-8

import time
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from src.base.baseAdb import BaseAdb
from src.base.baseFile import BaseFile
from src.base.baseImage import BaseImage

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
 

    def swipe_up(self):
        '''向上滑动'''
        width = self.driver.get_window_size()['width']
        height = self.driver.get_window_size()['height']        
        self.driver.swipe(width / 2, height * 4 / 5, width / 2, height / 5,
                500)
        time.sleep(1)

 
    def swipe_down(self):
        '''向下滑动'''
        width = self.driver.get_window_size()['width']
        height = self.driver.get_window_size()['height']        
        self.driver.swipe(width / 2, height / 5, width / 2, height * 4 / 5,
                500)
        time.sleep(1)

    def swipe_right(self):
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

        try:
            print("重置")
            driver.reset()
            time.sleep(5)
            print("点击直接登录")
            driver.click("id=>com.corp21cn.mail189:id/login_189account_txt")

            time.sleep(2)
            d = driver.get_window_size()

            print("点击坐标")
            BaseAdb.adb_tap(d["width"]*760/1080 , d["height"]* 1660 / 1920)
            time.sleep(2)

            print("输入用户名")
            BaseAdb.adb_tap(d["width"]/2, d["height"]*400/1920)
            BaseAdb.adb_input_text("13427665104")
            time.sleep(2)

            print("输入密码")
            BaseAdb.adb_tap(d["width"]/2, d["height"]*520/1920)
            BaseAdb.adb_input_text("yscs987654")
            time.sleep(2)

            start_time = time.time()
            print("点击登录")
            BaseAdb.adb_tap(d["width"]/2,d["height"]*820/1920)

            print("等待弹窗")
            driver.element_wait("id=>com.corp21cn.mail189:id/prompt_tips_socialmail", 20)

            end_time = time.time()

            value_time = str(round(end_time - start_time, 2))
            print("登录时延： %s" %value_time)

            driver.click("id=>com.corp21cn.mail189:id/prompt_tips_socialmail")

            time.sleep(4)

        except BaseException:
            print("登录错误")
            return 0

    def send(self):
        try:
            print("点击新建")
            driver.get_elements("id=>com.corp21cn.mail189:id/action_btn_view",10)[1].click()
            time.sleep(5)

            print("点击普通邮件")
            driver.click("id=>com.corp21cn.mail189:id/compose_email_action")

            print("输入收件人")
            driver.type("id=>com.corp21cn.mail189:id/to","13427665104@189.cn")

            print("主题")
            driver.type("id=>com.corp21cn.mail189:id/subject","subject")

            print("正文")
            driver.type("id=>com.corp21cn.mail189:id/message_content","123456789012345678901234567890")

            print("附件")
            driver.click("id=>com.corp21cn.mail189:id/attachment_add_icon_iv")

            print("点击文件")
            driver.click("id=>com.corp21cn.mail189:id/add_attachment_file")

            print("点击本地附件")
            driver.click("id=>com.corp21cn.mail189:id/add_attachment_local")

            print("找附件")
            driver.click("uiautomator=>0.")
            driver.click("uiautomator=>test2M.rar")
            driver.click(r"uiautomator=>确定")

            print("点击发送")
            driver.click(u"uiautomator=>发送")

            print("等待已发送")
            driver.element_wait(u"uiautomator=>已发送",20)

            print("点击关闭")
            driver.click("id=>com.corp21cn.mail189:id/attachment_share_close")
        except BaseException:
            print("发送出错")

    def down_file(self):

        try:
            print("点击第一封邮件")
            readlist = driver.get_elements("id=>com.corp21cn.mail189:id/mailListItem",10)
            readlist[0].click()
            start_time = time.time()

            print("等待附件图标")
            driver.element_wait("id=>com.corp21cn.mail189:id/att_icon")
            driver.element_wait("class=>android.widget.ScrollView")


            end_time = time.time()

            value_time = str(round(end_time - start_time, 2))

            print("打开时延：%s" %value_time)



            path="/mnt/sdcard/com.corp21cn.mail189/attachement/test2M*.rar"
            file_name = "test2M"

            print("清除文件")
            if BaseFile.adb_find_file(path,file_name):
                BaseFile.adb_del_file(path, file_name)

            start_time = time.time()
            print("点击附件，更多")
            driver.click("id=>com.corp21cn.mail189:id/attachment_operation")

            print("点击保存至本地")
            driver.click("uiautomator=>保存至本地")

            print("点击确定")
            driver.click("uiautomator=>确定")

            BaseFile.wait_for_file(path, file_name,60)

            end_time = time.time()

            value_time = str(round(end_time - start_time, 2))

            print("下载时延：%s" %value_time)

            time.sleep(5)

            print("清除文件")
            if BaseFile.adb_find_file(path,file_name):
                BaseFile.adb_del_file(path, file_name)


            BaseAdb.adb_back()

        except BaseException:
            print("打开或下载附件")


        time.sleep(5)

if __name__ == '__main__':

    driver = Psam(version="5.1",apk="com.corp21cn.mail189",ativity="com.corp21cn.mailapp.activity.ClientIntroducePage")

    driver.login_action()

    # driver.send()

    driver.down_file()















