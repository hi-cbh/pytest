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
            print("=>点击新建")
            self.driver.get_elements("id=>com.corp21cn.mail189:id/action_btn_view",10)[1].click()
            time.sleep(3)

            print("=>点击普通邮件")
            self.driver.click("id=>com.corp21cn.mail189:id/compose_email_action")

            print("=>输入收件人")
            self.driver.type("id=>com.corp21cn.mail189:id/to",self.username)

            print("=>主题")
            self.driver.type("id=>com.corp21cn.mail189:id/subject","TestEmail189")

            print("=>正文")
            self.driver.type("id=>com.corp21cn.mail189:id/message_content","123456789012345678901234567890")

            print("=>附件")
            self.driver.click("id=>com.corp21cn.mail189:id/attachment_add_icon_iv")

            print("=>点击文件")
            self.driver.click("id=>com.corp21cn.mail189:id/add_attachment_file")

            print("=>点击本地附件")
            self.driver.click("id=>com.corp21cn.mail189:id/add_attachment_local")

            print("=>找附件")
            self.driver.click("uiautomator=>0")
            self.driver.click("uiautomator=>0.")
            self.driver.click("uiautomator=>test2M.rar")
            self.driver.click(r"uiautomator=>确定")

            print("=>点击发送")
            self.driver.click(u"uiautomator=>发送")
            start_time = time.time()

            print("=>等待已发送")
            self.driver.element_wait(u"uiautomator=>已发送",20)
            end_time = time.time()

            value_time = str(round(end_time - start_time,2))
            print("发送邮件时延：%s" %value_time)
            print("=>点击关闭")
            self.driver.click("id=>com.corp21cn.mail189:id/attachment_share_close")

            time.sleep(5)

            return value_time
        except BaseException:
            print("发送出错")
            return 0

    # 为修改
    def send_action_peakValue(self):
        '''发送邮件获取内存、CPU峰值'''
        try:
            print("点击新建")
            self.driver.get_elements("id=>com.corp21cn.mail189:id/action_btn_view",10)[1].click()
            time.sleep(5)

            print("点击普通邮件")
            self.driver.click("id=>com.corp21cn.mail189:id/compose_email_action")

            print("输入收件人")
            self.driver.type("id=>com.corp21cn.mail189:id/to",self.username)

            print("主题")
            self.driver.type("id=>com.corp21cn.mail189:id/subject","TestEmail189")

            print("正文")
            self.driver.type("id=>com.corp21cn.mail189:id/message_content","123456789012345678901234567890")

            print("附件")
            self.driver.click("id=>com.corp21cn.mail189:id/attachment_add_icon_iv")

            print("点击文件")
            self.driver.click("id=>com.corp21cn.mail189:id/add_attachment_file")

            print("点击本地附件")
            self.driver.click("id=>com.corp21cn.mail189:id/add_attachment_local")

            print("找附件")
            self.driver.click("uiautomator=>0")
            self.driver.click("uiautomator=>0.")
            self.driver.click("uiautomator=>test2M.rar")
            self.driver.click(r"uiautomator=>确定")


            print("等待5秒")
            time.sleep(5)

            gt = GTTest("com.corp21cn.mail189")
            gt.startGT()

            print("等待5秒")
            time.sleep(5)

            print("=>点击发送")
            self.driver.click(u"uiautomator=>发送")
            start_time = time.time()

            print("=>等待已发送")
            self.driver.element_wait(u"uiautomator=>已发送",20)
            end_time = time.time()

            value_time = str(round(end_time - start_time,2))
            print("发送邮件时延：%s" %value_time)

            print("=>点击关闭")
            self.driver.click("id=>com.corp21cn.mail189:id/attachment_share_close")

            time.sleep(5)
            isTrue = self.waitfor_email()


            data = gt.endGT()
            # print(data)

            if isTrue:
                # 删除邮件
                self.driver.swipe(self.driver.get_window_size()["width"] - 20, 450, 20, 450, 500)
                time.sleep(2)

                BaseAdb.adb_tap(1300/1440 * self.driver.get_window_size()["width"], 500/2560 * self.driver.get_window_size()["height"])
                time.sleep(2)
            time.sleep(5)

            return data
        except BaseException:
            print('发送邮件出错了！！！')
            return 0


    def waitfor_email(self):
        '''等待邮件加载完成'''
        stat = False
        time_out = int(round(time.time() * 1000)) + 1 * 60 * 1000
        while int(round(time.time() * 1000)) < time_out:

            if self.driver.get_element(r"uiautomator=>TestEmail189",1) != None:
                stat = True
                break
            else:
                self.driver.swipe_down()

            time.sleep(0.1)

        return stat
