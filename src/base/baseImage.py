# urs/bin/python
# encoding:utf-8

import os
from PIL import Image
from src.base.baseTime import BaseTime

base_dir = str(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
PCpath = base_dir + "/pics/"

class BaseImage(object):
    
    def screenshot(self, driver, pic_name = "",is_tmp=False):
        '''截屏，保存在根目录下的pics文件夹下，已时间戳命名'''
        '''is_tmp为True，保存临时的图片'''
        try:
            if is_tmp:
                filename = 'tmp.jpg'
            else:
                filename = pic_name + "-" + BaseTime.current_time() + ".png"

            filepath = PCpath + filename
            driver.screenshot(filepath)
            print("截图路径：%s " %filepath)
        except BaseException as e:
            print(e)
            print("截屏失败！！！")

    def getpixel(self):
        '''获取邮件详情的下载像素点'''
        try:
            im = Image.open(PCpath+"tmp.jpg")
            rgb_im = im.convert('RGB')

            width = im.size[0]
            height = im.size[1]

            # 输出图片的像素值
            t= rgb_im.getpixel((176/1080 * width, 1592/1920 * height))

            print(t)
            return t
        except BaseException:
            print("获取像素点失败")
            return (0,0,0)

    def getpixel_189(self):
        '''获取邮件详情的下载像素点'''
        try:
            im = Image.open(PCpath+"tmp.jpg")
            rgb_im = im.convert('RGB')

            width = im.size[0]
            height = im.size[1]

            # 输出图片的像素值
            t= rgb_im.getpixel((1159/1488 * width, 1513/2560 * height))

            print(t)
            return t
        except BaseException:
            print("获取像素点失败")
            return (0,0,0)

    def getpixel_163(self):
        '''获取邮件详情的下载像素点'''
        try:
            im = Image.open(PCpath+"tmp.jpg")
            rgb_im = im.convert('RGB')
            #
            # width = im.size[0]
            # height = im.size[1]

            # 输出图片的像素值
            t= rgb_im.getpixel((376, 1779))

            print(t)
            return t
        except BaseException:
            print("获取像素点失败")
            return (0,0,0)

    def is_true_pixel(self, driver):
        '''下载图标附件的像素，默认为蓝色'''
        self.screenshot(driver,is_tmp=True)
        if self.getpixel() == (82, 166, 225):
            return True
        else:
            return False

    def is_true_pixel_189(self, driver):
        '''下载图标附件的像素，默认为黄色'''
        self.screenshot(driver,is_tmp=True)
        if self.getpixel_189() == (203, 172, 130):
            return True
        else:
            return False

    def is_true_pixel_163(self, driver):
        '''下载图标附件的像素，默认为'''
        self.screenshot(driver,is_tmp=True)
        if self.getpixel_163() == (8, 171, 247):
            return True
        else:
            return False
            
BaseImage = BaseImage()