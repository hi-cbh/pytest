import unittest,time,os
import configparser as cparser
from src.psam.psam import Psam
from src.base.baseAdb import BaseAdb
from src.base.baseTime import BaseTime
from src.otherApk.record360.flowRecord import FlowRecord360Action as flow360
from src.db.sqlhelper import SQLHelper


appPackage360 = "com.qihoo360.mobilesafe"
appActivity360 = "com.qihoo360.mobilesafe.ui.index.AppEnterActivity"

# ======== Reading user_db.ini setting ===========
base_dir = str(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
file_path = base_dir + "/user_db.ini"

cf = cparser.ConfigParser()
cf.read(file_path)

username = cf.get("userconf", "user1")
pwd = cf.get("userconf", "pwd1")
versionID = cf.get("verconf", "versionid")

class BrushFlow(unittest.TestCase):
    '''竞品使用简单的模式 + 手工进行测试 = 快速测试'''


    def setUp(self):
        try:
            BaseAdb.adb_intall_uiautmator()
            self.driver = Psam(version="6.0",apk=appPackage360,ativity=appActivity360)
        except BaseException :
            print("setUp启动出错！")


    #释放实例,释放资源
    def tearDown(self):
        self.driver.quit()


    def testCase(self):
        '''
        1、运行前，把各个邮箱进入邮件列表，在运行脚本


        :return:
        '''
        qq_apk="com.tencent.androidqqmail"
        qq_ativity="com.tencent.qqmail.launcher.desktop.LauncherActivity"

        net_apk="com.netease.mail"
        net_ativity="com.netease.mobimail.activity.LaunchActivity"

        corp_apk="com.corp21cn.mail189"
        corp_ativity="com.corp21cn.mailapp.activity.ClientIntroducePage"

        appPackage = "cn.cj.pe"  # 程序的package
        appActivity = "com.mail139.about.LaunchActivity"  # 程序的Activity

        # self.brush_flow_test("QQ邮箱", "QQ邮箱",qq_apk,qq_ativity)
        # self.brush_flow_test("网易邮箱大师", "网易邮箱大师",net_apk,net_ativity)
        self.brush_flow_test("189邮箱", "189邮箱",corp_apk,corp_ativity)
        # self.brush_flow_test("139邮箱", "139邮箱",appPackage,appActivity)

    def brush_flow_test(self,mail,contents, app_pkg, app_activity):
        '''空刷测试'''

        network = BaseAdb.get_network_type()
        width = self.driver.get_window_size()['width']
        height = self.driver.get_window_size()['height']
        print('当前网络状态：%s' %network)

        runtimes = 11

        fw = flow360(self.driver)

        try:
            # BaseAdb.adb_stop(app_pkg)
            # time.sleep(5)
            # BaseAdb.adb_start_app(app_pkg, app_activity)
            # time.sleep(3)
            BaseAdb.adb_home()
            time.sleep(3)
            fw.exec_preset()
            for x in range(1,runtimes):
                BaseAdb.adb_home()
                time.sleep(2)
                print('启动139')
                BaseAdb.adb_start_app(app_pkg, app_activity)
                time.sleep(10)
                stime = time.time()

                print('下拉')
                self.driver.swipe(width/2, 350, width/2, height - 100, 500)
                time.sleep(10)

                BaseAdb.adb_home()
                time.sleep(3)

                result = fw.exec_record(contents, network, False)
                print("流量：%s" %result)

                etime = time.time()
                valueTime = str(round((etime - stime), 2))
                print('[获取流量时间]: %r'  %valueTime)

                datas = {'productName' : '189',"versionID":versionID,'networkType':network,'nowTime':BaseTime.get_current_time(), \
                         'upflow':result["up"],'downflow':result["down"], 'allflow':result["all"], 'groupId':x}

                SQLHelper.insert_flow_other(datas)

        except BaseException:
            print("空刷错误！！")


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(BrushFlow('testCase'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)



