# urs/bin/python
# encoding:utf-8

import os
import sys
import time
import unittest

p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print("path: %s" %p)

sys.path.append(p+"/")

from src.testcase.v731.stand import StandBy
from src.testcase.HTMLTestRunner import HTMLTestRunner

if __name__ == "__main__":


    suite = unittest.TestSuite()
    suite.addTest(StandBy("testCase"))
    suite.addTest(StandBy("testCase"))
    suite.addTest(StandBy("testCase"))
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
