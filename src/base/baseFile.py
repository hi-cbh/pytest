# urs/bin/python
# encoding:utf-8

'''文件操作'''

import operator,os,time
import subprocess

class BaseFile(object):

    def adb_find_file(self, path, file):
        '''查找文件时是否存在'''
        try:
            value = os.popen("adb shell ls "+path)
            for txt in value.readlines():
                if (file in txt) and ("No such file or directory"  not in txt) :
                    return True
                
            return False
        except BaseException as msg:
            print('msg: %r' %msg)
            return False    

            
 
    def adb_del_file(self, path, file):
        '''删除文件'''
        try:
            os.popen("adb shell rm "+path)
        except BaseException as msg:
            print('msg: %r' %msg)    
        
  
    def adb_touch_file(self, path, file):
        '''创建文件'''
        try:
            os.popen("adb shell touch "+path + file)
        except BaseException as msg:
            print('msg: %r' %msg)      

    def wait_for_file(self, path, file, timeout = 10):
        '''等待文件出现'''
        timeout = int(round(time.time() * 1000)) + timeout * 1000
        try:
            while (int(round(time.time() * 1000) < timeout)):
#                 print('wait.....')
                if(self.adb_find_file(path, file) == True):
#                     print('find it')
                    return True
                time.sleep(0.1)
        except BaseException as msg:
            print(msg)
        else:
            return False
     

    def adb_mkdir(self, path):
        '''创建文件夹'''
        try:
            os.popen("adb shell mkdir -p " + path)

        except BaseException as msg:
            print('msg: %r' %msg)      
       
    def adb_ls_file_size(self, path):
        '''创建文件夹'''
        try:
            value = os.popen("adb shell ls -l " + path)
            # print("adb shell ls -l " + path)
            # print("value %s" %value.readlines())
            txt = str(value.readlines()[0])
            # print("print txt %s" %txt)
            if "t.txt" in txt:
                rtime = txt.split(' ',9)[6]
                # print("find: %s" %rtime)
                return rtime
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
         
    def wait_for_file_modify(self, timeoutMillis):
        '''等待文件更新,单位为：秒'''
        try:
            path = "/mnt/sdcard/Android/data/com.cmcc.test/cache/t.txt"
            dirpath = "/mnt/sdcard/Android/data/com.cmcc.test/cache/"
            
            if self.adb_find_file(path, "t.txt") != True:
                print('文件存在')
                self.adb_mkdir(dirpath)
                self.adb_touch_file(path, '')
                time.sleep(1)
            
            if self.adb_find_file(path, "t.txt") != True:
                print('文件不存在')
                return False
            
            orgsize = self.adb_ls_file_size(path)
            print("org: %s" %orgsize)
            time.sleep(1)
            timeout = int(round(time.time() * 1000)) + timeoutMillis * 1000
            while (int(round(time.time() * 1000) < timeout)):
                print('wait.....')
                if(operator.ne(self.adb_ls_file_size(path), orgsize)):
                    print('文件更新了.....')
                    return True
                time.sleep(0.1)
            else:
                print('time out')
                return False
        except BaseException as msg:
            print('msg: %r' %msg)
            return False
 
    def adb_tail_file(self):
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
    

    def get_time(self):
        '''获取时间值'''
        try:
            content = self.adb_tail_file()
            time = 0
            
            if len(content) < 60 or (not content.find('\#') == -1) :
                return time
            
            l = content.split('#')[1]

            value_time = str(round((float(l)/1000.0), 3))
            print('时间差: %r'  %value_time)
            
            return value_time
        
        except BaseException:
            return time
    
BaseFile = BaseFile()


if __name__ == "__main__":
    BaseFile.adb_ls_file_size("/mnt/sdcard/Android/data/com.cmcc.test/cache/")
    # BaseFile.wait_for_file_modify(30)