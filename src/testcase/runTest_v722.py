# urs/bin/python
# encoding:utf-8

import unittest,os,sys

p = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
print(p)

sys.path.append(p+r"/")

from src.testcase.v722.easytimedelay import Timedelay
from src.testcase.v722.peakValue import PeakValue
from src.testcase.v722.openEmail_filter import OpenEmail
from src.testcase.v722.brushFlow import BrushFlow
from src.testcase.v722.loginFlow import LoginFlow
from src.testcase.v722.standByFlowPowerMem import StandByFlowPowerMem


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(Timedelay("testCase"))
    suite.addTest(PeakValue("testCase"))
    suite.addTest(OpenEmail("testCase"))
    suite.addTest(BrushFlow("testCase"))
    suite.addTest(LoginFlow("testCase"))
    suite.addTest(StandByFlowPowerMem("testCase"))
    runner = unittest.TextTestRunner()
    runner.run(suite)