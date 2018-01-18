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

        try:
            print("重置")
            driver.reset()

            time.sleep(4)
            print("输入账号")
            driver.type("id=>com.netease.mail:id/editor_email","13427665104@163.com")

            print("输入密码")
            driver.type("id=>com.netease.mail:id/editor_password","yscs12345")

            print("点击登录")
            driver.click("id=>com.netease.mail:id/register_button_next")
            start_time = time.time()

            print("等待控件出现")
            driver.element_wait("id=>com.netease.mail:id/button_next", 60)

            end_time = time.time()

            print("点击 下一步")
            driver.click("id=>com.netease.mail:id/button_next")


            value_time = str(round(end_time - start_time, 2))
            print("登录时延：%s" %value_time)

            print("进入邮箱")
            driver.click("id=>com.netease.mail:id/enter_mail")

            print("点击跳过")
            driver.click(u"uiautomator=>跳过")
            time.sleep(2)

        except BaseException:
            print("登录错误")
            return 0

    def send(self):
        try:
            print("点击新建")
            driver.click("id=>com.netease.mail:id/iv_mail_list_plus")

            print("点击写邮件")
            driver.click("id=>com.netease.mail:id/tv_write_mail")

            print("输入账号")
            driver.type("id=>com.netease.mail:id/mailcompose_address_input","13427665104@163.com")

            print("输入主题")
            driver.type("id=>com.netease.mail:id/mailcompose_subject_textedit","pwd")

            print("正文")
            driver.type("id=>com.netease.mail:id/mailcompose_content","123456789012345678901234567890")

            print("点击附件")
            driver.click("id=>com.netease.mail:id/add_attachment_icon")

            print("点击 本地文件")
            driver.click("id=>com.netease.mail:id/vertical_file")

            print("查找文件")
            driver.click(r"uiautomator=>0.")

            print("点击test2M.rar")
            driver.click(r"uiautomator=>test2M.rar")

            print("点击完成")
            driver.click("id=>com.netease.mail:id/complete")

            print("点击发送")
            driver.click("id=>com.netease.mail:id/tv_done")

            start_time = time.time()

            time_out = int(round(time.time() * 1000)) + 1*60 * 1000

            # 获取邮件发送成功，退出；否则返回超时
            while int(round(time.time() * 1000)) < time_out :

                if BaseAdb.dumpsys_notification("邮件发送成功"):
                    break

                time.sleep(0.1)

            end_time = time.time()

            value_time = str(round(end_time - start_time, 2))
            print("发送邮件时延：%s" %value_time)

            time.sleep(5)

        except BaseException:
            print("发送出错")

    def down_file(self):

        try:
            print("点击第一封邮件")
            emaillist = driver.get_elements("id=>com.netease.mail:id/mail_list_item_content")
            emaillist[0].click()
            start_time = time.time()
            print("打开邮件")
            driver.element_wait("id=>com.netease.mail:id/mail_list_item_content")
            driver.element_wait("id=>com.netease.mail:id/conversation_item_attachment_divider")
            driver.element_wait("id=>com.netease.mail:id/attachment_info")
            end_time = time.time()


            value_time = str(round(end_time - start_time, 2))
            print("打开邮件时延： %s" %value_time)

            print("点击更多")
            driver.click("id=>com.netease.mail:id/attachment_more")


            print("点击保存")
            driver.click("id=>com.netease.mail:id/file_operate_save")

            print("清除")
            path="/mnt/sdcard/Download/test2M*"
            file="test2M"
            if BaseFile.adb_find_file(path,file):
                BaseFile.adb_del_file(path,file)

            time.sleep(5)

            print("点击确定")
            driver.click("id=>com.netease.mail:id/tv_done")
            start_time = time.time()

            print("等待邮件出现")
            BaseFile.wait_for_file(path,file)

            end_time = time.time()
            value_time = str(round(end_time - start_time, 2))
            print("下载附件时延：%s" %value_time)

            print("查找文件")
            if BaseFile.adb_find_file(path, file):
                print("清除文件")
                BaseFile.adb_del_file(path, file)


        except BaseException:
            print("打开或下载附件")


        time.sleep(5)

if __name__ == '__main__':

    driver = Psam(version="5.1",apk="com.netease.mail",ativity="com.netease.mobimail.activity.LaunchActivity")

    driver.login_action()

    # 删除邮件
    driver.swipe(driver.get_window_size()["width"] - 20, 450, 20, 450, 500)

    if driver.get_element("uiautomator=>删除") != None:
        driver.click("uiautomator=>删除")



        # driver.send()

    # driver.down_file()















