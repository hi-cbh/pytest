import sys
sys.path.append('../db')
try:
    from mysql_db import DB
except ImportError:
    from .mysql_db import DB

class SQLHelper(object):
    
    '''插入版本信息'''
    def InsertPro(self, datas):
    #     datas = {'productName': '139','versionID':'72234','versionName':"非固包",'tdesc':"测试数据"}
        db = DB()
        db.insert("tb_app_prot",datas)
        db.close()
    
    def InsertTimedelay(self, datas):
        '''插入时延数据'''
    #     datas = {'productName' : '139','versionID':"72234",'networkType':"4G",'nowTime':"2017-08-11 18:05:06", \
    #              'logintime':2.3,'receivetime':2.1, 'readtime':2.3,\
    #              'downtime':2.3, 'sendtime':2.3,'groupId':"1"}
        db = DB()
        db.insert("tb_app_data_timedelay",datas)
        db.close()
    
    def InsertCPUMEM(self, datas):
        '''插入CPU、内存峰值'''
    #     datas = {'productName' : '139','versionID':"72234",'networkType':"4G",'nowTime':"2017-08-11 18:05:06", \
    #              'avgcpu':2.3,'maxcpu':2.1, 'avgmem':2.3,\
    #              'maxmem':2.3, 'groupId':"1"}
        db = DB()
        db.insert("tb_app_cpu_mem",datas)
        db.close()
     
    def Insertflowlogin(self, datas):
        '''插入首次登陆流量'''
    #     datas = {'productName' : '139','versionID':"72234",'networkType':"4G",'nowTime':"2017-08-11 18:05:06", \
    #          'upflow':2.3,'downflow':2.1, 'allflow':2.3, 'groupId':"1"}
        db = DB()
        db.insert("tb_app_flow_login",datas)
        db.close()
     
    def Insertflowother(self, datas):
        '''插入空刷流量'''
    #     datas = {'productName' : '139','versionID':"72234",'networkType':"4G",'nowTime':"2017-08-11 18:05:06", \
    #          'upflow':2.3,'downflow':2.1, 'allflow':2.3, 'groupId':"1"}
        db = DB()
        db.insert("tb_app_flow_brush",datas)
        db.close() 
     
    def Insertkill(self, datas):
        '''插入杀进程启动时延'''
    #     datas = {'productName' : '139','versionID':"72234",'networkType':"4G",'nowTime':"2017-08-11 18:05:06", \
    #          'time0':2.3,'time1':2.1, 'time2':2.3, 'time3':2.3, 'time4':2.3, 'time5':2.3, \
    #          'time6':2.3, 'time7':2.3, 'time8':2.3, 'time9':2.3, 'groupId':"1"}
        db = DB()
        db.insert("tb_app_start_time",datas)
        db.close() 
     
    def Insertstandyno(self, datas):
        '''插入待机无邮件流量、内存、电量消耗'''
    #     datas = {'productName' : '139','versionID':"72234",'networkType':"4G",'nowTime':"2017-08-11 18:05:06", \
    #          'electric':2.3,'upflow':2.1, 'downflow':2.3, \
    #          'allflow':2.3,'avgmem':2.3,'groupId':"1"}
        db = DB()
        db.insert("tb_app_standy_no",datas)
        db.close() 
     
    def Insertstandyemail(self, datas):
        '''插入待机有邮件流量、内存、电量消耗'''
    #     datas = {'productName' : '139','versionID':"72234",'networkType':"4G",'nowTime':"2017-08-11 18:05:06", \
    #          'electric':2.3,'upflow':2.1, 'downflow':2.3, \
    #          'allflow':2.3,'emailcount':3,'groupId':"1"}
        db = DB()
        db.insert("tb_app_standy_email",datas)
        db.close()
    
SQLHelper = SQLHelper()


if __name__ == '__main__':
    
#     InsertTimedelay()
#     Insertflowlogin()
#     Insertflowother()
#     Insertkill()
#     Insertstandyno()
#     Insertstandyemail()
    datas = {'productName': '139','versionID':'72234','versionName':"非固包",'tdesc':"测试数据"}
    SQLHelper.InsertPro(datas)
    
