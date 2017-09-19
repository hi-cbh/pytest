# urs/bin/python
# encoding:utf-8

'''文件操作'''


import operator
# urs/bin/python
# encoding:utf-8
import os
import subprocess
import time


class BaseFile(object):

     
    def adbFindFile(self, path, file):
        '''查找文件时是否存在'''
        try:
            value = os.popen("adb shell ls "+path)
#             txt = value.readlines()
#             print('value: %r' %txt)
            for txt in value.readlines():
#                 print('value: %r' %txt)
                if (file in txt) and ("No such file or directory"  not in txt) :
#                     print('文件存在 ：%r' %file)
                    return True
                
            return False
        except BaseException as msg:
            print('msg: %r' %msg)
            return False    

            
 
    def adbDeleteFile(self, path, file):
        '''删除文件'''
        try:
            os.popen("adb shell rm "+path)

        except BaseException as msg:
            print('msg: %r' %msg)    
        
  
    def adbTouchFile(self, path, file):
        '''创建文件'''
        try:
            os.popen("adb shell touch "+path + file)

        except BaseException as msg:
            print('msg: %r' %msg)      
        
          
    def waitforfile(self, path, file, timeout = 10):
        '''等待文件出现'''
        timeout = int(round(time.time() * 1000)) + timeout * 1000
        try:
            while (int(round(time.time() * 1000) < timeout)):
#                 print('wait.....')
                if(self.adbFindFile(path, file) == True):
#                     print('find it')
                    return True;
                time.sleep(0.1)
        except BaseException as msg:
            print(msg)
        
        else:
#             print('time out')
            return False 
     

    def adbMkdirDir(self, path):
        '''创建文件夹'''
        try:
            os.popen("adb shell mkdir -p " + path)

        except BaseException as msg:
            print('msg: %r' %msg)      
       
    def adbLsFileSize(self, path):
        '''创建文件夹'''
        try:
            value = os.popen("adb shell ls -l " + path)
#             txt = value.readlines()
#             print('value: %r' %txt)
            for txt in value.readlines():
                if txt not in [None, '\n']:
#                     print(txt)
#                     print(txt.split(' ',13))
#                     print(txt.split(' ',13)[9])
                    return txt.split(' ',13)[9]
                '''使用正则表达式
                    s = "sdfdsfis123123#4342#"
                    result = re.findall(r".*#(.*)#.*",s)
                    for x in result:
                        print(x)
                    print(result)
                    '''
        except BaseException as msg:
            print('msg: %r' %msg)
            return None
         
    def waitForFileModify(self, timeoutMillis):
        '''等待文件更新,单位为：秒'''
        try:
#             path = "/mnt/sdcard/0/0./t.txt"
#             dirpath = "/mnt/sdcard/0/0./"
            path = "/mnt/sdcard/Android/data/com.cmcc.test/cache/t.txt"
            dirpath = "/mnt/sdcard/Android/data/com.cmcc.test/cache/"
            
            if self.adbFindFile(path, "t.txt") != True:
                print('文件存在')
                self.adbMkdirDir( dirpath)
                self.adbTouchFile(path, '')
                time.sleep(1)
            
            if self.adbFindFile(path, "t.txt") != True:
                print('文件不存在')
                return False
            
            
            orgsize = self.adbLsFileSize(path)
            
            timeout = int(round(time.time() * 1000)) + timeoutMillis * 1000
            
            while (int(round(time.time() * 1000) < timeout)):
#                 print('wait.....')
                if(operator.ne(self.adbLsFileSize(path),orgsize)):
                    print('文件更新了.....')
                    return True;
                time.sleep(0.1)
            else:
                print('time out')
                return False
        except BaseException as msg:
            print('msg: %r' %msg)
            return False
 
    def adbTailFile(self):
        '''使用 adb shell tail -n 1 查找固定目录下的文件，倒数第一行'''
        path = "/mnt/sdcard/Android/data/com.cmcc.test/cache/t.txt"
        try:
            value = subprocess.Popen("adb shell tail -n 1 " + path, shell=True,stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            value.wait()
            output = value.stdout.read().decode()
            if output not in ['',None]:
                
                print ("%s" % output)
                return output
            else:
                return None
        except BaseException as msg:
            print('msg: %r' %msg)
            return None
    

    def getTime(self):
        try:
            '''获取时间值'''
            content = self.adbTailFile()
            time = 0
            
            if len(content) < 60 or (not content.find('\#') == -1) :
                return time
            
            l = content.split('#')[1]
#             print("times：%s" %l)
    
            valueTime = str(round((float(l)/1000.0), 3))
            print('时间差: %r'  %valueTime)
            
            return valueTime
        
        except BaseException:
            return time
    
BaseFile = BaseFile()
        