# urs/bin/python
# encoding:utf-8

import unittest,os,sys
import time
p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print("path: %s" %p)

sys.path.append(p+"/")

from src.testcase.v722.easytimedelay import Timedelay
from src.testcase.v722.peakValue import PeakValue
from src.testcase.v722.openEmail_filter import OpenEmail
from src.testcase.v722.brushFlow import BrushFlow
from src.testcase.v722.loginFlow import LoginFlow
from src.testcase.v722.standByFlowPowerMem import StandByFlowPowerMem
from src.testcase.HTMLTestRunner import HTMLTestRunner
from src.testcase.v722.firstLogin import InitData


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(InitData("testCase"))
    suite.addTest(Timedelay("testCase"))
    suite.addTest(PeakValue("testCase"))
    suite.addTest(OpenEmail("testCase"))
    suite.addTest(BrushFlow("testCase"))
    suite.addTest(LoginFlow("testCase"))
    suite.addTest(StandByFlowPowerMem("testCase"))
    runner = unittest.TextTestRunner()



    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename = r'/Users/apple/git/pytest/report/' + now + '_result.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp,
                            title='Test Report',
                            description='Example with: ')
    runner.run(suite)
    fp.close()
