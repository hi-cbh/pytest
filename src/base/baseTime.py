# urs/bin/python
# encoding:utf-8

import time

class BaseTime(object):
    
    def current_time(self):
        '''用于写入文件，或文件格式'''
        return time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) 
     
    def get_current_time(self):
        '''用于写入数据库'''    
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 


    def get_time_pro(self):
        '''写入产品ID'''
        return time.strftime("%m%d", time.localtime())

BaseTime = BaseTime()

if __name__ == "__main__":
    print(BaseTime.get_time_pro())
