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
            print("点击新建")
            self.driver.get_elements("id=>com.corp21cn.mail189:id/action_btn_view",10)[1].click()
            time.sleep(5)

            print("点击普通邮件")
            self.driver.click("id=>com.corp21cn.mail189:id/compose_email_action")

            print("输入收件人")
            self.driver.type("id=>com.corp21cn.mail189:id/to",self.username)

            print("主题")
            self.driver.type("id=>com.corp21cn.mail189:id/subject","subject")

            print("正文")
            self.driver.type("id=>com.corp21cn.mail189:id/message_content","123456789012345678901234567890")

            print("附件")
            self.driver.click("id=>com.corp21cn.mail189:id/attachment_add_icon_iv")

            print("点击文件")
            self.driver.click("id=>com.corp21cn.mail189:id/add_attachment_file")

            print("点击本地附件")
            self.driver.click("id=>com.corp21cn.mail189:id/add_attachment_local")

            print("找附件")
            self.driver.click("uiautomator=>0.")
            self.driver.click("uiautomator=>test2M.rar")
            self.driver.click(r"uiautomator=>确定")

            print("点击发送")
            self.driver.click(u"uiautomator=>发送")

            print("等待已发送")
            self.driver.element_wait(u"uiautomator=>已发送",20)

            print("点击关闭")
            self.driver.click("id=>com.corp21cn.mail189:id/attachment_share_close")

        except BaseException:
            print("发送出错")
            return 0

    # 为修改
    def send_action_peakValue(self):
        '''发送邮件获取内存、CPU峰值'''
        try:
            print("点击新建")
            self.driver.click("id=>com.netease.mail:id/iv_mail_list_plus")

            print("点击写邮件")
            self.driver.click("id=>com.netease.mail:id/tv_write_mail")

            print("输入账号")
            self.driver.type("id=>com.netease.mail:id/mailcompose_address_input","13427665104@163.com")

            print("输入主题")
            self.driver.type("id=>com.netease.mail:id/mailcompose_subject_textedit","pwd")

            print("正文")
            self.driver.type("id=>com.netease.mail:id/mailcompose_content","123456789012345678901234567890")

            print("点击附件")
            self.driver.click("id=>com.netease.mail:id/add_attachment_icon")

            print("点击 本地文件")
            self.driver.click("id=>com.netease.mail:id/vertical_file")

            print("查找文件")
            self.driver.click(r"uiautomator=>0.")

            print("点击test2M.rar")
            self.driver.click(r"uiautomator=>test2M.rar")


            print("点击完成")
            self.driver.click("id=>com.netease.mail:id/complete")

            print("等待5秒")
            time.sleep(5)

            gt = GTTest("com.netease.mail")
            gt.startGT()

            print("等待5秒")
            time.sleep(5)

            print("点击发送")
            self.driver.click("id=>com.netease.mail:id/tv_done")

            start_time = time.time()

            time_out = int(round(time.time() * 1000)) + 1*60 * 1000

            # 获取邮件发送成功，退出；否则返回超时
            while int(round(time.time() * 1000)) < time_out :

                if BaseAdb.dumpsys_notification("邮件发送成功"):
                    break

                time.sleep(0.1)

            end_time = time.time()

            value_time = str(round(end_time - start_time, 2))
            print("发送邮件时延：%s" %value_time)


            self.waitfor_email()

            data = gt.endGT()
            # print(data)


            # 删除邮件
            self.driver.swipe(self.driver.get_window_size()["width"] - 20, 450, 20, 450, 500)

            if self.driver.get_element("uiautomator=>删除") != None:
                self.driver.click("uiautomator=>删除")



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

            if self.driver.get_element("id=>com.netease.mail:id/mail_list_item_state",1) != None:
                stat = True
                break
            else:
                self.driver.swipeDown()

            time.sleep(0.1)


        return stat
