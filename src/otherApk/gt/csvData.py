# urs/bin/python
# encoding:utf-8

import csv
import os
import re
from src.base.baseConversion import BaseConversion as bc


class GetCSVData(object):
    
    def __init__(self,path,pkg):
        self.path = path
        self.pkg = pkg
    
    # 获取文件名
    def getFileName(self, tp):
        if not len(self.pkg):
            print("包名不能为空")
            return None
        
        p = ""
        if tp == "cpu":
            p = r"Pcp[0-5]_"+self.pkg+"_([0-9])+.csv"
        else :
            p = r"Pr[0-5]_"+self.pkg+"_([0-9])+.csv"
            
        
        # 如果文件不存在
        ls = []    
        if os.path.exists(self.path):
            ls = self.getFileList(self.path)
        else:
            return None
        
        # 查找匹配的文件
        for x in ls:
            if len(re.findall(p, x, flags = 0)):
                return x
        else:
            return None
    
    # 搜索目录下的文件        
    def getFileList_window(self, p):
        p = str( p )
        if p=="":
            return [ ]
        p = p.replace( "/","\\")
        if p[-1] != "\\":
            p = p+"\\"
        a = os.listdir( p )
        b = [ x   for x in a if os.path.isfile( p + x ) ]
        return b

        # 搜索目录下的文件
    def getFileList(self, p):
        p = str( p )
        if p=="":
            return [ ]
        a = os.listdir( p )
        b = [ x   for x in a if os.path.isfile( p + x ) ]
        return b

    def getData(self,ty):
        '''获取数据'''
        data = []
        filename = self.getFileName( ty)
        if filename == None:
            return None
        with open(self.path+filename,"r",encoding="utf-8") as csvfile:
            read = csv.reader(csvfile)
            for i in read:
                if ('min' in i) or ('max' in i) or ('avg' in i):
                    data.append(i)
        return data

    def getCPUValue(self):
        '''获取CPU最大、最小、平均'''
        
        data = []
        cpu = {}
        data = self.getData('cpu')
        
        if data != None:
            cpu['min'] = data[0][1]
            cpu['max'] = data[1][1]
            cpu['avg'] = data[2][1]
        else:
            return None
        
        return cpu
    
    def getMEMValue(self):
        '''返回主线程内存最大、最小、平均值'''
        
        data = []
        mem = {}
        data = self.getData('mem')
        print(data)
#         print(data)
        if data != None:
            mem['min'] = bc.round(float(data[0][1])/1024, 1)
            mem['max'] = bc.round(float(data[1][1])/1024, 1)
            mem['avg'] = bc.round(float(data[2][1])/1024, 1)
        else:
            return None
        
        return mem
            
        
        
if __name__ == "__main__":
    filepath = r"/Users/apple/git/pytest/logs/2017-09-04_18-28-34/"
    d = GetCSVData(filepath, 'cn.cj.pe')
    
    data = d.getMEMValue()         
    print(data)