# urs/bin/python
# encoding:utf-8

import re



class BaseConversion(object):
    '''单位换算'''
    
    def findDigit(self, st):
        '''查找字符串中的数值'''
        return re.findall(r"\d+\.?\d*",st)


    def valueFlowToK(self,tx):
        '''读取360流量字段，将单位统一为K'''

        srcl = re.findall(r"\d+\.?\d*[BKM]",tx)
        
        results = []
        for le in srcl:
            value = self.findDigit(le)[0]
            
            if "B" in le:
                value = round((float(value)/1024), 3)
            elif "M" in le:
                value = float(value) * 1024
            else:
                value = float(value)  
                
            results.append(value)
#         print(results)
        return results
    
    def round(self, num1, num):
        '''返回小数点
        
            sample:rount(1.3333,2) => 1.33
        '''
#         print(num1)
        return round(float(num1), 2)

        
BaseConversion = BaseConversion()       