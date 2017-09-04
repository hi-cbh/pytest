# urs/bin/python
# encoding:utf-8
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from base.variable import GetVariable as common
from selenium.webdriver.support import expected_conditions as EC
class Element:
    
    def __init__(self,driver):
        self.driver = driver


    def waitForElement(self,name,by):
        try:
            el = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((name,by)))
        except:
            print("can not find" + by)
        return el
    
    def waitForE(self, name,by):
        try:
            el = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((name,by)))
        except:
            print("can not find" + by)
        return el