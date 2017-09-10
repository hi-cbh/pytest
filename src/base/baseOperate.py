# urs/bin/python
# encoding:utf-8
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import time

class Element(object):
    
    def __init__(self):
        print('init Element')


    '''
    sample:
        waitForElement(driver, By.ID, 'cn.cj.pe/login')
    '''
    def waitForElement(self,driver, name,by, timeout = 60):
        try:
            el = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((name,by)))
        except TimeoutException:
            print("find %s out time" %by)
            return None
        except NoSuchElementException:
            print("can not find" + by)
            return None
        else:
            return el
    
    
    def swipeUp(self, driver):
        '''向上滑动'''
        width = driver.get_window_size()['width']
        height = driver.get_window_size()['height']        
        driver.swipe(width / 5, height * 4 / 5, width / 5, height / 5,
                500);
        time.sleep(2);

 
    def swipeDown(self,driver):
        '''向下滑动'''
        width = driver.get_window_size()['width']
        height = driver.get_window_size()['height']        
        driver.swipe(width / 5, height / 5, width / 5, height * 4 / 5,
                500);
        time.sleep(2);
    
    
    
Commom = Element()