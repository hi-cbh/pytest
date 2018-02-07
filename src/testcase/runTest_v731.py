# urs/bin/python
# encoding:utf-8

import os
import sys
import time
import unittest

p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print("path: %s" %p)

sys.path.append(p+"/")

from src.testcase.v731.timedelay import Timedelay
from src.testcase.v731.peakValue import PeakValue
from src.testcase.v731.openEmail_filter import OpenEmail
from src.testcase.v731.brushFlow import BrushFlow
from src.testcase.v731.loginFlow import LoginFlow


from src.testcase.v731.standByFlowPowerMem import StandByFlowPowerMem
from src.testcase.HTMLTestRunner import HTMLTestRunner

if __name__ == "__main__":


    suite = unittest.TestSuite()
    # suite.addTest(InitData("testCase"))
    # suite.addTest(Timedelay("testCase"))
    # suite.addTest(PeakValue("testCase"))
    # suite.addTest(OpenEmail("testCase"))
    # suite.addTest(BrushFlow("testCase"))
    # suite.addTest(LoginFlow("testCase"))
    suite.addTest(StandByFlowPowerMem("testCase"))
    suite.addTest(StandByFlowPowerMem("testCase")) # 重复两次
    # suite.addTest(StandByFlowPowerMem("testCase"))
    # suite.addTest(StandByFlowPowerMem("testCase"))
    # suite.addTest(StandByFlowPowerMem("testCase"))
    # suite.addTest(StandByFlowPowerMem("testCase"))

    runner = unittest.TextTestRunner()



    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename = r'/Users/apple/git/pytest/report/' + now + '_result.html'
    # filename = r'/Users/apple/git/pytest/report/index.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp,
                            title='Test Report',
                            description='Example with: ')
    runner.run(suite)
    fp.close()
