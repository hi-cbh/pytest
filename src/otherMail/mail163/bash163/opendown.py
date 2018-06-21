import time
from src.base.baseFile import BaseFile
from src.base.baseAdb import BaseAdb
from src.base.baseImage import BaseImage


class OpenDown(object):

    def __init__(self, driver):
        self.driver = driver

    def open_mail(self):
        '''打开邮件时延'''
        try:
            print("点击第一封邮件")
            emaillist = self.driver.get_elements("id=>com.netease.mail:id/mail_list_item_content")
            emaillist[0].click()
            start_time = time.time()
            print("打开邮件")
            # self.driver.element_wait("id=>com.netease.mail:id/mail_list_item_content")
            # self.driver.element_wait("id=>com.netease.mail:id/conversation_item_attachment_divider")
            # self.driver.element_wait("id=>com.netease.mail:id/attachment_info")
            timeout = int(round(time.time() * 1000)) + 1 * 10 * 1000
            while int(round(time.time() * 1000)) < timeout:
                if BaseImage.is_true_pixel_163(self.driver):
                    break
                time.sleep(0.1)


            end_time = time.time()

            value_time = str(round(end_time - start_time, 2))
            print("打开邮件时延： %s" %value_time)

            return value_time
        except BaseException:
            print("打开邮件")
            return 0


    def down_file(self):
        '''下载附件时延'''
        try:

            print("点击更多")
            self.driver.click("id=>com.netease.mail:id/attachment_more")

            print("点击保存")
            self.driver.click("id=>com.netease.mail:id/file_operate_save")

            print("清除")
            path="/mnt/sdcard/Download/test2M*"
            file="test2M"
            if BaseFile.adb_find_file(path,file):
                BaseFile.adb_del_file(path,file)

            time.sleep(5)

            print("点击确定")
            self.driver.click("id=>com.netease.mail:id/tv_done")
            start_time = time.time()

            print("等待邮件出现")
            BaseFile.wait_for_file(path,file)

            end_time = time.time()
            value_time = str(round(end_time - start_time, 2))
            print("下载附件时延：%s" %value_time)

            print("查找文件")
            if BaseFile.adb_find_file(path, file):
                print("清除文件")
                BaseFile.adb_del_file(path, file)

            BaseAdb.adb_back()
            time.sleep(5)

            return value_time
        except BaseException:
            print("下载附件")
            return 0
