
from src.base.baseAdb import BaseAdb

import time

class Login(object):

    def __init__(self,driver, username, pwd):
        self.driver = driver
        self.username = username
        self.pwd = pwd

    def login_action(self):
        try:
            print("重置")
            self.driver.reset()
            time.sleep(5)
            print("点击直接登录")
            self.driver.click("id=>com.corp21cn.mail189:id/login_189account_txt")

            time.sleep(2)
            d = self.driver.get_window_size()

            print("点击坐标")
            BaseAdb.adb_tap(d["width"]*760/1080 , d["height"]* 1660 / 1920)
            time.sleep(2)

            print("输入用户名")
            BaseAdb.adb_tap(d["width"]/2, d["height"]*400/1920)
            BaseAdb.adb_input_text(self.username)
            time.sleep(2)

            print("输入密码")
            BaseAdb.adb_tap(d["width"]/2, d["height"]*520/1920)
            BaseAdb.adb_input_text(self.pwd)
            time.sleep(2)

            start_time = time.time()
            print("点击登录")
            BaseAdb.adb_tap(d["width"]/2,d["height"]*820/1920)

            print("等待弹窗")
            self.driver.element_wait("id=>com.corp21cn.mail189:id/prompt_tips_socialmail", 20)

            end_time = time.time()

            value_time = str(round(end_time - start_time, 2))
            print("登录时延： %s" %value_time)

            self.driver.click("id=>com.corp21cn.mail189:id/prompt_tips_socialmail")

            time.sleep(4)
            print("点击关闭广告")
            self.driver.click("id=>com.corp21cn.mail189:id/advert_close")


        except BaseException:
            print("登录错误")
            return 0
