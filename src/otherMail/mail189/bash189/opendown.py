import time
from src.base.baseFile import BaseFile
from src.base.baseAdb import BaseAdb
class OpenDown(object):

    def __init__(self, driver):
        self.driver = driver

    def open_mail(self):
        '''打开邮件时延'''
        try:
            print("点击第一封邮件")
            readlist = self.driver.get_elements("id=>com.corp21cn.mail189:id/mailListItem",10)
            readlist[0].click()
            start_time = time.time()

            print("等待附件图标")
            self.driver.element_wait("id=>com.corp21cn.mail189:id/att_icon")
            self.driver.element_wait("class=>android.widget.ScrollView")

            end_time = time.time()
            value_time = str(round(end_time - start_time, 2))

            print("打开时延：%s" %value_time)
            return value_time
        except BaseException:
            print("打开邮件")
            return 0


    def down_file(self):
        '''下载附件时延'''
        try:

            path="/mnt/sdcard/com.corp21cn.mail189/attachement/test2M*.rar"
            file_name = "test2M"

            print("清除文件")
            if BaseFile.adb_find_file(path,file_name):
                BaseFile.adb_del_file(path, file_name)

            start_time = time.time()
            print("点击附件，更多")
            self.driver.click("id=>com.corp21cn.mail189:id/attachment_operation")

            print("点击保存至本地")
            self.driver.click("uiautomator=>保存至本地")

            print("点击确定")
            self.driver.click("uiautomator=>确定")

            BaseFile.wait_for_file(path, file_name,60)

            end_time = time.time()

            value_time = str(round(end_time - start_time, 2))

            print("下载时延：%s" %value_time)

            time.sleep(5)

            print("清除文件")
            if BaseFile.adb_find_file(path,file_name):
                BaseFile.adb_del_file(path, file_name)


            BaseAdb.adb_back()

            return value_time
        except BaseException:
            print("下载附件")
            return 0
