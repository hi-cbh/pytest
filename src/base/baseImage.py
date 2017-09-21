# urs/bin/python
# encoding:utf-8

import os
from src.base.baseTime import BaseTime

base_dir = str(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
base_dir = base_dir.replace('\\', '/')
PCpath = base_dir + "/pics/"

class BaseImage(object):
    
    def screenshot(self, driver, picName):
        '''截屏，保存在根目录下的pics文件夹下，已时间戳命名'''
        try:
            
            filename = picName + "-"+ BaseTime.currentTime() + ".png" 
            filepath = PCpath + filename
            driver.screenshot(filepath)
            
        except BaseException as e:
            print(e)
            print("截屏失败！！！")
            
            
BaseImage = BaseImage()