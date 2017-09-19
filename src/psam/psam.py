# coding=utf-8

import time
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Psam(object):
    
    def __init__(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '6.0'
        desired_caps['deviceName'] = 'android'
        desired_caps['appPackage'] = 'cn.cj.pe'
        desired_caps['appActivity'] = 'com.mail139.about.LaunchActivity'
        desired_caps['newCommandTimeout'] = '360'
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
            else:
                raise NameError("Please enter the correct targeting elements,'id','name','class','link_text','xpath','css'.")
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
#                 element = self.driver.find_element_by_android_uiautomator("text("+value+")")
            elif by == "class":
                element = self.driver.find_element_by_class_name(value)
            elif by == "link_text":
                element = self.driver.find_element_by_link_text(value)
            elif by == "xpath":
                element = self.driver.find_element_by_xpath(value)
            elif by == "css":
                element = self.driver.find_element_by_css_selector(value)
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
                500);
        time.sleep(1);

 
    def swipeDown(self):
        '''向下滑动'''
        width = self.driver.get_window_size()['width']
        height = self.driver.get_window_size()['height']        
        self.driver.swipe(width / 5, height / 5, width / 5, height * 4 / 5,
                500);
        time.sleep(2);

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
        self.driver.find_element_by_android_uiautomator(uia_string)

#     def scrollTo(self):
#         self.driver.scroll(origin_el, destination_el)



if __name__ == '__main__':
#     devices = {'appPackage': 'cn.cj.pe', 'appActivity': 'com.mail139.about.LaunchActivity'}
    
    driver = Psam()
    driver.testCase()
            