# urs/bin/python
# encoding:utf-8
# 导入内置方法
import os,time,unittest,sys
import configparser as cparser
file_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(file_dir)
# print(base_dir)
# 导入外部方法
from src.base.baseAdb import BaseAdb
from src.psam.psam import Psam
from src.otherApk.gt.gtutil import GTTest
from src.testcase.v731.easycase.login import Login


#

#======== Reading user_db.ini setting ===========
base_dir = str(os.path.dirname(os.path.dirname(__file__)))
file_path = base_dir + "/user_db.ini"
print("test")


cf = cparser.ConfigParser()
cf.read(file_path)

username = cf.get("userconf", "user1")
pwd = cf.get("userconf", "pwd1")
username2 = cf.get("userconf", "user2")
pwd2 = cf.get("userconf", "pwd2")
filename = cf.get("userconf", "filename")
path = r'/mnt/sdcard/139PushEmail/download/%s@139.com/*%s.rar'  %(username, filename)

versionID = cf.get("verconf", "versionid")

##====================





class InitData(unittest.TestCase):

    def setUp(self):

        time.sleep(10)
        BaseAdb.adb_intall_uiautmator()
        self.driver = Psam()
        # 点击允许
        self.driver.click(u"uiautomator=>允许")
        time.sleep(4)


    #释放实例,释放资源
    def tearDown(self):
        self.driver.quit()
        print("运行结束")
        time.sleep(5)


    def testCaseOtherApk(self):
        '''辅助工具初始化'''
        BaseAdb.adb_home()
        print("检查经常出错的辅助工具，是否可用")
        BaseAdb.adb_stop("com.cmcc.test")
        time.sleep(3)
        BaseAdb.adb_start_app("com.cmcc.test", "com.cmcc.test.MainActivity")

        if self.driver.get_element("id=>com.cmcc.test:id/textView1",10) == None :
            self.driver.type("id=>com.cmcc.test:id/editText1",u"发送邮件成功")
            self.driver.click(u"uiautomator=>添加")

        time.sleep(2)
        BaseAdb.adb_home()

        print("GT初始化")
        BaseAdb.adb_stop("com.tencent.wstt.gt")
        time.sleep(2)
        BaseAdb.adb_start_app("com.tencent.wstt.gt", "com.tencent.wstt.gt.activity.SplashActivity")
        time.sleep(4)
        self.driver.click(u"uiautomator=>允许")
        time.sleep(1)
        self.driver.click(u"uiautomator=>允许")
        time.sleep(1)
        self.driver.click(u"uiautomator=>允许")
        time.sleep(1)
        BaseAdb.adb_home()

        print("开始测试GT是否可用")
        gt = GTTest("cn.cj.pe")
        gt.startGT()
        time.sleep(10)
        gt.endGT()




    def testCasePre(self):
        '''首次登陆，点击权限'''

        network = BaseAdb.get_network_type()
        print('当前网络状态：%s' %network)

        try:
            stat = u'开始登录时延测试'
            Login(self.driver,username, pwd).loginAction(firstLogin=True)

        except BaseException as be:
            print("运行到：%s 运行出错" %stat)
            print(be)

    def testCaseRun(self):
        '''测试环境，运行一次基本用例'''


if __name__ == "__main__":

    apkpath = r"/Users/apple/Downloads/V7.4.0-20171217_26667-apm__10000.apk"
    try:
        if len(sys.argv) > 1:
            apkpath = sys.argv[1]
            if apkpath not in [None, ""]:
                print("获得的路径为：%s" %apkpath)
            else:
                print("安装包路径有问题....")
        else:
            print("外部传参路径有问题！，使用默认apk")


        '''卸载旧包'''
        if BaseAdb.adb_apk_exist("cn.cj.pe") == True:
            print('delete new apk')
            BaseAdb.uninstall_app("cn.cj.pe")
            time.sleep(8)

        if apkpath != None:
            # 安装新包
            print('install new apk')
            BaseAdb.install_app(apkpath)
            print(u'等待10秒')
            time.sleep(20)
            print(u"等待完成")

        if BaseAdb.adb_apk_exist("cn.cj.pe") == False:
            print("安装包失败，不运行后续步骤，直接退出")
            os._exit(0)
    except BaseException as e:
        print(e)


    suite = unittest.TestSuite()
    # suite.addTest(InitData('testCaseOtherApk'))
    suite.addTest(InitData('testCasePre'))
    # suite.addTest(InitData('testCaseRun'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)