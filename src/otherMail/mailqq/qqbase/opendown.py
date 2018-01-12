
import time
from src.base.baseAdb import BaseAdb
from src.base.baseFile import BaseFile
from src.base.baseImage import BaseImage
class OpenDown(object):

    def __init__(self, driver):
        self.driver = driver

    def open_mail(self):
        '''打开邮件'''
        try:
            print("点击收件箱")
            self.driver.click("xpath=>//android.widget.TextView[contains(@text,'收件箱')]")

            print("点击第一封邮件")
            ele_list = self.driver.get_elements("class=>android.widget.RelativeLayout")
            # 点击第第一封邮件
            ele_list[3].click()
            start_time = time.time()
            print("等待加载完成")
            timeout = int(round(time.time() * 1000)) + 1 * 10 * 1000
            while int(round(time.time() * 1000)) < timeout:
                if BaseImage.is_true_pixel(self.driver):
                    break
                time.sleep(0.1)

            end_time = time.time()
            print("加载完成")
            time.sleep(4)
            value_time = str(round(end_time - start_time, 2))
            print("打开未读邮件时延：%s" %value_time)

            return value_time
        except BaseException:
            print("打开邮件出错")
            return 0



    def down_file(self):
        '''下载附件'''
        try:

            file_path = "/mnt/sdcard/Download/QQMail/test2M.*"
            file_name = "test2M"
            print("查找文件")
            if BaseFile.adb_find_file(file_path, file_name):
                print("清除文件")
                BaseFile.adb_del_file(file_path, file_name)

            print("点击更多")
            BaseAdb.adb_tap_per(self.driver, 940/1080, 1590/1920)

            print("保存文件")
            self.driver.click("xpath=>//android.widget.TextView[contains(@text,'保存文件')]")

            print("在download目录")
            if not self.driver.get_attribute("id=>com.tencent.androidqqmail:id/ru","text").__contains__("Download"):
                self.driver.click("id=>com.tencent.androidqqmail:id/ru")

            print("点击保存")
            self.driver.click("xpath=>//android.widget.Button[contains(@text,'保存')]")
            start_time = time.time()

            print("等待邮件出现")
            BaseFile.wait_for_file(file_path,file_name)

            end_time = time.time()
            value_time = str(round(end_time - start_time, 2))
            print("下载附件时延：%s" %value_time)

            print("查找文件")
            if BaseFile.adb_find_file(file_path, file_name):
                print("清除文件")
                BaseFile.adb_del_file(file_path, file_name)


            time.sleep(5)
            BaseAdb.adb_back()
            return value_time
        except BaseException:
            print("下载附件错误")
            return 0