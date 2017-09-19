# urs/bin/python
# encoding:utf-8
import configparser as cparser
import os
import time
import unittest
from src.mail.mailOperation import EmailOperation
from src.psam.psam import Psam
from src.testcase.v722.easycase.login import Login
from src.testcase.v722.easycase.public import PublicUtil as pu

# sys.path.append(r'D:\workspace\workspace_python3\appium_python\src')

# ======== Reading user_db.ini setting ===========
base_dir = str(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
# base_dir = base_dir.replace('\\', '/')
file_path = base_dir + "/user_db.ini"
print(file_path)
cf = cparser.ConfigParser()
cf.read(file_path)

username = cf.get("userconf", "user1")
pwd = cf.get("userconf", "pwd1")

 
from src.base.baseAdb import BaseAdb

GetMax = 3  # 获取的组数量
RunMax = 11  # 大循环最大允许次数
RunMax2 = 3  # 每一次小循环最大允许次数
ListMax = 10  # 列表长度
DelNum = 2  # 允许剔除的数量

class MyTestCase(unittest.TestCase):
    #脚本初始化,获取操作实例
    def setUp(self):
        eo = EmailOperation(username+"@139.com", pwd)
        eo.moveForlder(["100","INBOX"])
        time.sleep(4)
        print("uiautomator")
        BaseAdb.adbIntallUiautmator()
        self.driver = Psam()

    #释放实例,释放资源
    def tearDown(self):
        eo = EmailOperation(username+"@139.com", pwd)
        eo.moveForlder(["INBOX","100"])
        self.driver.quit()
  
    def testCase(self):
        appPackage = "cn.cj.pe"  # 程序的package
        appActivity = "com.mail139.about.LaunchActivity"  # 程序的Activity
        
        login=Login(self.driver,username, pwd)
        login.loginAction()
        
        pu.loadEmail(self.driver)
        
        BaseAdb.adbStop(appPackage)
        time.sleep(5)
        BaseAdb.adbStartApp(appPackage, appActivity)
        time.sleep(3)

        print(u'运行杀进程启动：')
        ls = []
        global RunMax
        global GetMax
        for i in range(1,RunMax):
            ls = self.getDataList()

            print('第 %s 轮测试结果：' %(str(i)))
            print(ls)

            if i == GetMax:
                return
    
    def getTime(self):
        '''获取时间'''
        try:  
            BaseAdb.adbHome()
            time.sleep(1)
            BaseAdb.adbStop("cn.cj.pe")
            time.sleep(2)
              
            # 在桌面查找 139邮箱
            el = self.driver.get_element(u"name=>139邮箱")
            if el == None:
                print('找不到控件')
                return 0
             
            # 获取开始时间
            starttime = time.time()
              
            # 点击139邮箱
            el.click()
              
            # 等待页面存在 收件箱字段
            self.driver.element_wait(r"id=>cn.cj.pe:id/message_list_bottom_email")
            # 记录结束时间
            endtime = time.time()
            # 计算时间差
            calctime = round((endtime - starttime),2)
#             print(calctime)   
            return calctime
  
        except BaseException as error:
            return 0
    
    def getDataList(self):
        '''获取数据列表'''
        global ListMax
        global RunMax2
        global DelNum
        for j in range(RunMax2):
            dataList=[]
            for i in range(ListMax):
                dataList.append(self.getTime())
            
            if self.filtera(dataList, DelNum):
#                 print('测试数据，筛选结果符合')
#                 print(dataList)
                return dataList
            
            else:
                print('测试数据，筛选结果不符合')
                print(dataList)
                dataList.clear()
                dataList = []
        else:
            return None    

  
    # 筛选值  
    def filtera(self, ls, delNum):
        if not len(ls):
            return False
    
        davg = round(sum(ls)/len(ls), 2)
    #     print("avg: %s" %(str(davg)))
        dmax = davg * 1.2
    #     print("max: %s" %(str(dmax)))
        dmin = davg * 0.5
    #     print("min: %s" %(str(dmin)))
        
        # 列表加入值
        ls2 = [x for x in ls if x >= dmin and x <= dmax]
        
    #     print(ls2)
        
        if (len(ls) - len(ls2)) <= delNum :
            return True
        
        return False  
       
  
  
if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(MyTestCase('testCase'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


