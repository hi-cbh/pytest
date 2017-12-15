# urs/bin/python
# encoding:utf-8
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Element(object):
    
    def __init__(self):
        print('init Element')


    '''
    sample:
        waitForElement(driver, By.ID, 'cn.cj.pe/login')
    '''
    def wait_for_element(self, driver, name, by, timeout = 60):
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

    
    
    
Commom = Element()