import unittest,time,os
import configparser as cparser
from src.psam.psam import Psam
from src.base.baseAdb import BaseAdb
from src.base.baseTime import BaseTime
from src.otherMail.mail163.bash163.login import Login
from src.otherApk.record360.flowRecord import FlowRecord360Action as flow360
from src.db.sqlhelper import SQLHelper
qq_apk="com.netease.mail"
qq_ativity="com.netease.mobimail.activity.LaunchActivity"

base_dir = str(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
file_path = base_dir + "/user_db.ini"

cf = cparser.ConfigParser()
cf.read(file_path)

username = cf.get("netconf", "user1")
pwd = cf.get("netconf", "pwd1")
username2 = cf.get("netconf", "user2")
pwd2 = cf.get("netconf", "pwd2")

versionID = cf.get("verconf", "versionid")


class LoginFlow(unittest.TestCase):
    '''竞品使用简单的模式 + 手工进行测试 = 快速测试'''


    def setUp(self):
        try:
            BaseAdb.adb_intall_uiautmator()
            self.driver = Psam(version="6.0",apk=qq_apk,ativity=qq_ativity)
        except BaseException :
            print("setUp启动出错！")


    #释放实例,释放资源
    def tearDown(self):
        self.driver.quit()

    def testCase(self):

        try:
            print("======运行首次登录流量开始======")
            # 前期准备
            time.sleep(5)
            fw = flow360(self.driver)
            fw.exec_preset()

            BaseAdb.adb_home()
            time.sleep(2)
            BaseAdb.adb_stop(qq_apk)
            time.sleep(2)
            BaseAdb.adb_clear(qq_apk)
            time.sleep(5)
            # 准备完成

            network = BaseAdb.get_network_type()
            print('当前网络状态：%s' %network)

            runtimes = 12
            for x in range(1,runtimes):
                print("运行首次等次数：%d" %x)
                try:
                    login=Login(self.driver,username, pwd)
                    login.login_action()


                    # 等待未读邮件出现
                    print('等待未读邮件出现.....20封')
                    is_staue = self.waitfor_email()

                    if is_staue:
                        print('记录流量值')
                        result = fw.exec_record(u"网易邮箱大师", network, False)
                        time.sleep(5)
                        BaseAdb.adb_home()
                        time.sleep(2)
                        BaseAdb.adb_stop(qq_apk)
                        time.sleep(2)
                        BaseAdb.adb_clear(qq_apk)
                        time.sleep(5)
                        datas = {'productName' : '163','versionID':versionID,'networkType':network,'nowTime':BaseTime.get_current_time(), \
                                 'upflow':result["up"],'downflow':result["down"], 'allflow':result["all"],'groupId':x}
                        print(datas)
                        SQLHelper.insert_flow_login(datas)
                        time.sleep(2)
                except BaseException:
                    print("运行首次等次数：%d 出错，当次数据不入数据库!" %x)

        except BaseException as be:
            print("运行出错")
            print(be)
        finally:
            print("======运行首次登录流量结束======")


    def waitfor_email(self):
        '''等待邮件加载完成'''
        try:
            time_out = int(round(time.time() * 1000)) + 1 * 60 * 1000
            while int(round(time.time() * 1000)) < time_out:
                txt = self.driver.get_attribute("id=>com.netease.mail:id/tv_mail_list_filter","text")
                if txt.__contains__("20"):
                    return True

                time.sleep(0.1)
            else:
                # 超时了
                return False
        except BaseException:
            print("加载中出现错误，返回False")
            return False



if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(LoginFlow('testCase'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)