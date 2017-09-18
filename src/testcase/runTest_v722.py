# urs/bin/python
# encoding:utf-8

import unittest
from testcase.v722.easytimedelay import Timedelay
from testcase.v722.peakValue import PeakValue
from testcase.v722.openEmail_filter import MyTestCase
from testcase.v722.brushFlow import BrushFlow
from testcase.v722.loginFlow import LoginFlow
from testcase.v722.standByFlowPowerMem import StandByFlowPowerMem


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(Timedelay("testCase"))
    suite.addTest(PeakValue("testCase"))
    suite.addTest(MyTestCase("testCase"))
    suite.addTest(BrushFlow("testCase"))
    suite.addTest(LoginFlow("testCase"))  
#     suite.addTest(StandByFlowPowerMem("testCase"))                    
    runner = unittest.TextTestRunner()
    runner.run(suite)