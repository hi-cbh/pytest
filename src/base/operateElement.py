# urs/bin/python
# encoding:utf-8

from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from base.variable import GetVariable as common
from selenium.webdriver.support import expected_conditions as EC
import time


class OperateElement():
    
    # 构造方法，传入driver,默认为空，如果为空，会运行错误
    def __init__(self, driver = ""):
        self.driver = driver
    
    # 等待元素出现,默认30秒
    def waitforElement(self,mOperate , timeout = common.WAIT_TIME):

        '''等待元素出现，返回元素对象'''
        try:
            el = WebDriverWait(self.driver, timeout).until(lambda x: elements_by(mOperate, self.driver))
        except TimeoutException:
            print('查找元素，等待超时...')
            return None
        except NoSuchElementException:
            print("元素查找失败....")
            return None
        else:
            print('元素查找成功...')
            return el

    # 等待元素出现,默认30秒
    def waitforE(self,by ,name, timeout = common.WAIT_TIME):

        '''等待元素出现，返回元素对象'''
        try:
            el = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((name,by)))
        except TimeoutException:
            print('查找元素，等待超时...')
            return None
        except NoSuchElementException:
            print("元素查找失败....")
            return None
        else:
            print('元素查找成功...')
            return el
   
# 此脚本主要用于查找元素是否存在，操作页面元素
class OperateElement2():
    def __init__(self, driver=""):
        self.driver = driver
    def findElement(self, mOperate):
        '''
        查找元素.mOperate是字典
        operate_type：对应的操作
        element_info：元素详情
        find_type: find类型
        '''
        try:
            WebDriverWait(self.driver, common.WAIT_TIME).until(lambda x: elements_by(mOperate, self.driver))
            return True
        except TimeoutException:
            return False
        except NoSuchElementException:
            print("找不到数据")
            return False


    def operate_element(self,  mOperate):
        if self.findElement(mOperate):
            elements = {
                common.CLICK: lambda: operate_click(mOperate, self.driver),
                # GetVariable.TAP: lambda: operate_tap(mOperate["find_type"], self.driver,  mOperate["element_info"], arg),
                common.SEND_KEYS: lambda: send_keys(mOperate, self.driver),
                common.SWIPELEFT: lambda : opreate_swipe_left(mOperate, self.driver),
                common.SEND_CODE: lambda : send_code()
            }
            return elements[mOperate["operate_type"]]()
        return False

# 如果要输入验证码，暂停10秒钟，手动去输入
def send_code():
    time.sleep(10)
# 点击事件
def operate_click(mOperate,cts):
    if mOperate["find_type"] == common.find_element_by_id or mOperate["find_type"] == common.find_element_by_name or mOperate["find_type"] == common.find_element_by_xpath:
        elements_by(mOperate, cts).click()
    if mOperate["find_type"] == common.find_elements_by_id or mOperate["find_type"] == common.find_elements_by_name:
        elements_by(mOperate, cts)[mOperate["index"]].click()
    # 记录运行过程中的一些系统日志，比如闪退会造成自动化测试停止
    if common.SELENIUM_APPIUM == common.APPIUM:
        # errorLog.get_error(log=mOperate["log"], devices=mOperate["devices"])
        pass
# 左滑动
def opreate_swipe_left(mOperate, cts):
    time.sleep(1)
    width = cts.get_window_size()["width"]
    height = cts.get_window_size()["height"]
    for i in range(mOperate["time"]):
        cts.swipe(width/4*3, height / 2, width / 4 *1, height / 2, 500)
        time.sleep(1)
# start_x,start_y,end_x,end_y

# 轻打x轴向右移动x单位，y轴向下移动y单位
# def operate_tap(elemen_by,driver,element_info, xy=[]):
#     elements_by(elemen_by, driver, element_info).tap(x=xy[0], y=xy[1])

def send_keys(mOperate,cts):
    elements_by(mOperate, cts).send_keys(mOperate["text"])


# 封装常用的标签
def elements_by(mOperate, cts):
    elements = {
        common.find_element_by_id : lambda :cts.find_element_by_id(mOperate["element_info"]),
        common.find_elements_by_id : lambda :cts.find_elements_by_id(mOperate["element_info"]),
        common.find_element_by_xpath: lambda :cts.find_element_by_xpath(mOperate["element_info"]),
        common.find_element_by_name: lambda :cts.find_element_by_name(mOperate['name']),
        common.find_elements_by_name: lambda :cts.find_elements_by_name(mOperate['name'])[mOperate['index']],
        common.find_element_by_class_name: lambda :cts.find_element_by_class_name(mOperate['element_info']),
        common.find_elements_by_class_name: lambda :cts.find_elements_by_class_name(mOperate['element_info'])[mOperate['index']]
    }
    return elements[mOperate["find_type"]]()    
