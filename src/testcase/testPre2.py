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


#======== Reading user_db.ini setting ===========
base_dir = str(os.path.dirname(os.path.dirname(__file__)))
file_path = base_dir + "/user_db.ini"
print("test")



##====================


class KillOpen(unittest.TestCase):

    def setUp(self):

        self.driver = Psam("5.1.1")
        # 点击允许


    #释放实例,释放资源
    def tearDown(self):
        self.driver.quit()
        print("运行结束")
        time.sleep(5)


    def testCaseKill(self):
        '''辅助工具初始化'''
        BaseAdb.adb_home()
        print("检查经常出错的辅助工具，是否可用")
        # BaseAdb.adb_stop("cn.cj.pe")
        # time.sleep(3)
        # BaseAdb.adb_start_app("cn.cj.pe", "com.mail139.about.LaunchActivity")
        #
        # el = self.driver.element_wait(r"id=>cn.cj.pe:id/tv_launch_count",3)
        # start = 0
        # if el != None:
        #     el.click()
        #     start = time.time()
        #
        # self.driver.element_wait(r"id=>cn.cj.pe:id/message_list_bottom_email")
        #
        # if start != 0:
        #     valueTime = str(round((time.time() - start), 2))
        #     print('[时间]: %r'  %valueTime)
        #
        #
        # time.sleep(1)
    #
    # def testCase(self):
    #     for i in range(10):
    #         self.kill()


if __name__ == "__main__":


    suite = unittest.TestSuite()
    suite.addTest(KillOpen('testCaseKill'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)