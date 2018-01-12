import time
from src.base.baseAdb import BaseAdb
from src.otherApk.gt.gtutil import GTTest


class Send(object):

    def __init__(self,driver, username):
        self.driver = driver
        self.username = username



    def send_action(self):
        '''发送邮件基础方法'''
        try:
            print("点击收件箱")
            self.driver.click("xpath=>//android.widget.TextView[contains(@text,'收件箱')]")

            print("点击新建")
            self.driver.click("xpath=>//android.widget.ImageButton[@content-desc='写邮件']")

            time.sleep(2)

            print("输入发送者：%s" %self.username)
            BaseAdb.adb_input_text(self.username)

            print("输入主题")
            BaseAdb.adb_tap(300,600)
            BaseAdb.adb_input_text("QQMailSelf")

            print("输入正文")
            BaseAdb.adb_tap(300, 900)
            BaseAdb.adb_input_text("123456789012345678901234567890")


            print("点击添加附件")
            self.driver.click("xpath=>//android.widget.Button[@content-desc='附件操作']")

            print("选择文件在")
            self.driver.click("xpath=>//android.widget.ImageButton[@content-desc='从文件浏览器选择文件']")


            print("获取路径")
            txt = self.driver.get_attribute("id=>com.tencent.androidqqmail:id/k","text")
            print("获取路径txt: %s" %txt)

            # 目录路径不对
            if not txt.__contains__("/0/0./"):
                self.driver.click("id=>com.tencent.androidqqmail:id/ru")
                self.driver.click("id=>com.tencent.androidqqmail:id/ru")
                self.driver.click(r"xpath=>//android.widget.TextView[contains(@text,'0.')]")

            print("选择文件")
            self.driver.click("xpath=>//android.widget.TextView[contains(@text,'test2M.rar')]")
            self.driver.click("xpath=>//android.widget.Button[contains(@text,'添加到邮件')]")

            time.sleep(5)
            print("点击发送")
            self.driver.click("xpath=>//android.widget.Button[contains(@text,'发送')]")
            start_time = time.time()


            time.sleep(3)
            time_out = int(round(time.time() * 1000)) + 1*60 * 1000

            # 获取邮件发送成功，退出；否则返回超时
            while int(round(time.time() * 1000)) < time_out :

                if BaseAdb.dumpsys_notification("邮件发送成功"):
                    break

                time.sleep(0.1)

            end_time = time.time()

            value_time = str(round(end_time - start_time, 2))

            print("邮件发送时延：%s" %value_time)

            time.sleep(5)

            return value_time
        except BaseException:
            print('发送邮件出错了！！！')
            return 0


    def send_action_peakValue(self):
        '''发送邮件获取内存、CPU峰值'''
        try:
            print("点击收件箱")
            self.driver.click("xpath=>//android.widget.TextView[contains(@text,'收件箱')]")

            print("点击新建")
            self.driver.click("xpath=>//android.widget.ImageButton[@content-desc='写邮件']")

            time.sleep(2)

            print("输入发送者：%s" %self.username)
            BaseAdb.adb_input_text(self.username)

            print("输入主题")
            BaseAdb.adb_tap(300,600)
            BaseAdb.adb_input_text("QQMailSelf")

            print("输入正文")
            BaseAdb.adb_tap(300, 900)
            BaseAdb.adb_input_text("123456789012345678901234567890")


            print("点击添加附件")
            self.driver.click("xpath=>//android.widget.Button[@content-desc='附件操作']")

            print("选择文件在")
            self.driver.click("xpath=>//android.widget.ImageButton[@content-desc='从文件浏览器选择文件']")


            print("获取路径")
            txt = self.driver.get_attribute("id=>com.tencent.androidqqmail:id/k","text")
            print("获取路径txt: %s" %txt)

            # 目录路径不对
            if not txt.__contains__("/0/0./"):
                self.driver.click("id=>com.tencent.androidqqmail:id/ru")
                self.driver.click("id=>com.tencent.androidqqmail:id/ru")
                self.driver.click(r"xpath=>//android.widget.TextView[contains(@text,'0.')]")

            print("选择文件")
            self.driver.click("xpath=>//android.widget.TextView[contains(@text,'test2M.rar')]")
            self.driver.click("xpath=>//android.widget.Button[contains(@text,'添加到邮件')]")

            time.sleep(5)
            time.sleep(5)
            gt = GTTest("com.tencent.androidqqmail")
            gt.startGT()

            print("点击发送")
            self.driver.click("xpath=>//android.widget.Button[contains(@text,'发送')]")
            start_time = time.time()

            time.sleep(3)
            time_out = int(round(time.time() * 1000)) + 1*60 * 1000

            # 获取邮件发送成功，退出；否则返回超时
            while int(round(time.time() * 1000)) < time_out :

                if BaseAdb.dumpsys_notification("邮件发送成功"):
                    break

                time.sleep(0.1)

            end_time = time.time()
            value_time = str(round(end_time - start_time, 2))
            print("邮件发送时延：%s" %value_time)

            time.sleep(8)

            is_stat =  self.waitfor_email()


            data = []
            data = gt.endGT()
            # print(data)
            time.sleep(2)


            if is_stat:
                # 删除邮件
                self.driver.swipe(self.driver.get_window_size()["width"] - 20, 650, 20, 650, 500)

                if self.driver.get_element("xpath=>//android.widget.TextView[contains(@text,'删除')]") != None:
                    self.driver.click("xpath=>//android.widget.TextView[contains(@text,'删除')]")

            return data
        except BaseException:
            print('发送邮件出错了！！！')
            return 0


    def waitfor_email(self):
        '''等待邮件加载完成'''
        stat = False
        time_out = int(round(time.time() * 1000)) + 1 * 60 * 1000
        while int(round(time.time() * 1000)) < time_out:
            txt = self.driver.get_attribute("id=>com.tencent.androidqqmail:id/k","text")
            if txt.__contains__("收件箱(1)​"):
                stat = True
                break
            else:
                self.driver.swipeDown()

            time.sleep(0.1)


        return stat
