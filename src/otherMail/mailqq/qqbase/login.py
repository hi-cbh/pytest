
import  time
from src.base.baseAdb import BaseAdb

class Login(object):

    def __init__(self,driver, username, pwd):
        self.username = username
        self.pwd = pwd
        self.driver = driver

    def login_action(self):
        '''登录基础方法'''
        try:
            print("重置app")
            self.driver.reset()

            print("等待")
            time.sleep(6)

            print("右滑动")
            self.driver.swipeRight()
            self.driver.swipeRight()
            self.driver.swipeRight()

            print("点击体验")
            self.driver.click("class=>android.widget.Button")

            time.sleep(2)

            print("点击QQ邮箱")
            self.driver.get_elements("class=>android.widget.ImageView")[0].click()
            time.sleep(8)

            print("输入账号")
            BaseAdb.adb_tap(500,510)
            BaseAdb.adb_input_text(self.username)

            print("输入密码")
            BaseAdb.adb_tap(500,700)
            BaseAdb.adb_input_text(self.pwd)

            print("点击登录")
            BaseAdb.adb_tap(500,890)
            start_time = time.time()

            print("等待完成出现")
            self.driver.element_wait("xpath=>//android.widget.Button[contains(@text,'完成')]", 60)
            value_time = str(round(time.time() - start_time, 2))
            print("登录时延：%s" %value_time)

            self.driver.click("class=>android.widget.Button")


            time.sleep(2)
            return value_time
        except BaseException:
            print("账号登录出错")
            return 0



