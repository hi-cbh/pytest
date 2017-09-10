# urs/bin/python
# encoding:utf-8

import time

class BaseTime(object):
    
    def currentTime(self):
        return time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) 
        
        
BaseTime = BaseTime()

if __name__ == "__main__":
    print(BaseTime().currentTime() )
