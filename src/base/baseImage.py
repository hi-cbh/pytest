# urs/bin/python
# encoding:utf-8

import os
from src.base.baseTime import BaseTime

base_dir = str(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
PCpath = base_dir + "/pics/"

class BaseImage(object):
    
    def screenshot(self, driver, pic_name):
        '''截屏，保存在根目录下的pics文件夹下，已时间戳命名'''
        try:
            
            filename = pic_name + "-" + BaseTime.current_time() + ".png"
            filepath = PCpath + filename
            driver.screenshot(filepath)
            
        except BaseException as e:
            print(e)
            print("截屏失败！！！")
            
            
BaseImage = BaseImage()