# # urs/bin/python
# # encoding:utf-8
# 
# import os
# import unittest
# import time
# from appium import webdriver
# from selenium.webdriver.common.by import By
# from testcase.v722.case.login import Login
# from testcase.v722.case.send import Send
# from testcase.v722.case.openDown import OpenDown
# from testcase.v722.case.receive import Receive
# 
# PATH = lambda p:os.path.abspath(
#     os.path.join(os.path.dirname(__file__),p)
#     )
# 
# class Timedelay(unittest.TestCase):
#     
#     def setUp(self):
#         desired_caps = {}
#         desired_caps['platformName'] = 'Android'
#         desired_caps['platformVersion'] = '6.0'
#         desired_caps['deviceName'] = 'android'
#         desired_caps['appPackage'] = 'cn.cj.pe'
#         desired_caps['appActivity'] = 'com.mail139.about.LaunchActivity'
#         desired_caps['newCommandTimeout'] = '360'
#         desired_caps["unicodeKeyboard"] = "True"
#         desired_caps["resetKeyboard"] = "True"
#         self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
#     
#     #释放实例,释放资源
#     def tearDown(self):
#         #os.popen("adb shell pm clear cn.cj.pe")
#         self.driver.quit()
# 
#     def testCase(self):
#         username = '13580491603'
#         pwd = 'chinasoft123'
#         username2 = '13697485262'
#         
#         filename = 'test2M'
#         path = r'/mnt/sdcard/139PushEmail/download/%s@139.com/*%s.rar'  %(username, filename)
#         
#         logintime = 0
#         opentime = 0
#         downtime = 0
#         sendtime = 0
#         receivetime = 0
#         
#         
#         login=Login(self.driver,username, pwd)
#         
#         logintime = login.loginAction()
#         
#         re = Receive(self.driver,username2, pwd, username+"@139.com")
#         receivetime = re.receiveAction()
#         
# #         od = OpenDown(self.driver, path, filename)
# #         
# #         opentime = od.openAction()
# #         
# #         downtime = od.downAction()
# #         send = Send(self.driver,'13580491603@139.com')
# #         sendtime = send.sendAction()
#         
#         result = {'login': logintime, 'open': opentime, 'down':downtime, 'send':sendtime, 'receive':receivetime}
#         print(result)
#         
#         
# 
#     
# if __name__ == "__main__":
#     suite = unittest.TestSuite()
#     suite.addTest(Timedelay('testCase'))
#     runner = unittest.TextTestRunner(verbosity=2)
#     runner.run(suite)