
from src.base.baseAdb import BaseAdb

import time

class Login(object):

    def __init__(self,driver, username, pwd):
        self.driver = driver
        self.username = username
        self.pwd = pwd

    def login_action(self):
        try:
            print("=>重置")
            self.driver.reset()
            time.sleep(5)
            print("=>点击直接登录")
            self.driver.click("id=>com.corp21cn.mail189:id/add_account_tx")

            print("=>点击189邮箱")
            self.driver.get_elements("id=>com.corp21cn.mail189:id/mailsetselect_item_iv")[0].click()


            time.sleep(2)
            d = self.driver.get_window_size()

            print("=>点击坐标")
            # BaseAdb.adb_tap(d["width"]*760/1080 , d["height"]* 1660 / 1920)
            BaseAdb.adb_tap(1000 , 2174)
            time.sleep(2)

            print("=>输入用户名")
            BaseAdb.adb_tap(d["width"]/2, 460)
            BaseAdb.adb_input_text(self.username)
            time.sleep(2)

            print("=>输入密码")
            BaseAdb.adb_tap(d["width"]/2, 660)
            BaseAdb.adb_input_text(self.pwd)
            time.sleep(2)

            start_time = time.time()
            print("=>点击登录")
            BaseAdb.adb_tap(d["width"]/2,1060,True)

            print("=>等待弹窗")
            self.driver.element_wait("id=>com.corp21cn.mail189:id/prompt_tips_socialmail", 20)

            end_time = time.time()

            value_time = str(round(end_time - start_time, 2))
            print("=>登录时延： %s" %value_time)

            self.driver.click("id=>com.corp21cn.mail189:id/prompt_tips_socialmail")

            time.sleep(4)
            print("=>点击关闭")
            self.driver.click("id=>com.corp21cn.mail189:id/cancel_btn")
            time.sleep(4)
            # print("=>点击关闭广告")
            # self.driver.click("id=>com.corp21cn.mail189:id/advert_close")

            return value_time
        except BaseException:
            print("登录错误")
            return 0
