

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

            time.sleep(4)
            print("输入账号")
            self.driver.type("id=>com.netease.mail:id/editor_email","13427665104@163.com")

            print("输入密码")
            self.driver.type("id=>com.netease.mail:id/editor_password","yscs12345")

            print("点击登录")
            self.driver.click("id=>com.netease.mail:id/register_button_next")
            start_time = time.time()

            print("等待控件出现")
            self.driver.element_wait("id=>com.netease.mail:id/button_next", 60)

            end_time = time.time()

            print("点击 下一步")
            self.driver.click("id=>com.netease.mail:id/button_next")


            value_time = str(round(end_time - start_time, 2))
            print("登录时延：%s" %value_time)

            print("进入邮箱")
            self.driver.click("id=>com.netease.mail:id/enter_mail")

            print("点击跳过")
            self.driver.click(u"uiautomator=>跳过")
            time.sleep(2)

        except BaseException:
            print("登录错误")
            return 0
