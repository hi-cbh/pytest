# urs/bin/python
# encoding:utf-8
import sys
import time
import unittest
from base.baseConversion import BaseConversion as bc
from psam.psam import Psam

sys.path.append(r'D:\workspace\workspace_python3\appium_python\src')


from base.baseAdb import BaseAdb


class MyTestCase(unittest.TestCase):
    #脚本初始化,获取操作实例
    def setUp(self):
        BaseAdb.adbIntallUiautmator()        
        self.driver = Psam()

    #释放实例,释放资源
    def tearDown(self):   
        self.driver.quit()
  
    def testCase(self):
        time.sleep(5)
        BaseAdb.adbHome()
        time.sleep(2)
        print("测试")
        self.driver.click(u"name=>设置")
#         self.scroll(u"name=>单手操作")
        
    def scroll(self, txt):
        w = self.driver.get_window_size()['width']
        h = self.driver.get_window_size()['height']
        
        while True:
            
            el = self.driver.element_wait(txt, 2)
            if  el != None:
                y = el.location['y']
                if bc.round(float(y/h), 2) > 0.8 :
                    self.driver.swipe(w/2, y*0.8, w/2, y*0.5, 1000)
                break
            
            else:
                   
                self.driver.swipeUp()
  
  
if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(MyTestCase('testCase'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


