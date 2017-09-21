# urs/bin/python
# encoding:utf-8
import sys
import time
import unittest
from base.baseConversion import BaseConversion as bc
from psam.psam import Psam

import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)
sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])

print(rootPath)