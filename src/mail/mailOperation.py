#!/usr/bin/python  
# -*- coding: utf-8 -*- 

import pyzmail
import time
from imapclient import IMAPClient


class EmailOperation(object):
    
    def __init__(self, userName, pwd):
        print("使用imapclient，操作邮件...")
        self.server = IMAPClient('imap.139.com', use_uid=True, ssl=False)
        self.username = userName
        self.password = pwd
        
    
    def logout(self):
        self.server.logout()
        
    # 删除邮件
    def _del(self, messages):
#         print('del message')
        self.server.delete_messages(messages)
        self.server.expunge()
    
    def _mv(self, message, folder):
        self.server.copy(message, folder)
        time.sleep(1)
        self._del(message)
    
    def _into(self, box):
        # 'INBOX','草稿箱','已发送','已删除','100'
        self.server.select_folder(box)
        
    def _getUIDs(self):
        # 获取序列
        UIDs = self.server.search(['NOT', 'DELETED'])
        return UIDs
    
    def emailBody(self, mss):
        # 获取某序列id的原始信息
        rawMessages = self.server.fetch([mss],['BODY[]','FLAGS'])
#         pprint.pprint(rawMessages)
        # 使用pyzmail，返回主体信息
        message = pyzmail.PyzMessage.factory(rawMessages[mss][b'BODY[]'])
        
        # 如果信息为空，返回None
        if not message:
            return None
        # 获取正文内容
        if message.text_part != None:
            lines = message.text_part.get_payload().decode(message.text_part.charset)
        
        str=''
        # 去除内容中的回车
        for line in lines:
            if line not in ['\n', '\r'] :    
                str+=line

        print(str)
        # body自动
        body = {'subject':message.get_subject(),
                'from': message.get_address('from'),
                'to': message.get_address('to'),
                'mainbody': str
                }
        return body
        
        
    def delAllMessage(self,folder):
        '''清空某个文件夹下的所有邮件'''
        self._into(folder)
        
        UIDs = self._getUIDs()
        if len(UIDs) ==  0 :
            return
        else:
            self._del(UIDs)
    
    def delNewMessage(self, fforlder):   
        '''把最近一封新邮件已到目的目录'''
        self._into(fforlder)
        
        Uids = self._getUIDs()
        
        if len(Uids) ==  0 :
            return
        else:
            self._del(Uids[-1])
    
    def moveAllMessageToFolder(self, fforlder, tforlder):   
        '''把maessage/messages 从 ffolder 移动到 tforlder'''
        
        self._into(fforlder)
        
        Uids = self._getUIDs()
        # 邮件数量为空
        if len(Uids) ==  0 :
            print("%s 数量为：0，该操作无效" %fforlder)
            return True
        self._mv(Uids, tforlder)
            

    def checkNewMessage(self):
        '''判断最新一封邮件，是否包含某个字段，显示邮件数量'''
        self._into("INBOX")
        
        Uids = self._getUIDs()

        print('current INBOX email: %s' %str(len(Uids)))

        if len(Uids) in [0 ,1]:
            print("不执行，目前邮件数量为：%r" %len(Uids))
            return
        
        if self.emailBody(Uids[-1])['subject'] == 'testReceive':
            self._del(Uids[-1])

    
    def deleteNewestMail(self):
        '''删除最新的一封邮件'''
        try:
            isTrue = False
            self.server.login(self.username, self.password)    
            self.delNewMessage('INBOX')
            isTrue = True   
        except BaseException as error:
            print(error)
            print("删除邮件可能出现错误")
        finally:
            self.logout()
            return isTrue  

    def clearForlder(self, l=[]):
        '''清空邮箱某个文件夹'''
        '''
        sample:
        clearForlder(['100', 'INBOX'])
        '''
        isTrue = False
        if len(l) == 0:
            return isTrue
        try:
            self.server.login(self.username, self.password)    
            for f in l:
                print("clear Forlder: %s" %f)
                self.delAllMessage(f)
                time.sleep(1)
                
            isTrue = True
        except BaseException as error:
            print(error)
            print("删除邮件可能出现错误")
        finally:
            self.logout() 
            return isTrue 
                
    def moveForlder(self, l=[]):
        '''移动邮件
        sample:
            moveForlder(['100', 'INBOX'])
        '''
        isTrue = False
        if len(l) == 0:
            return isTrue
        try:
            self.server.login(self.username, self.password)    
            self.moveAllMessageToFolder(l[0], l[1])
            print("移动邮件成功：%s => %s" %(l[0], l[1]))
            isTrue = True
        except BaseException as error:
            print(error)
            print("清空邮箱某个文件夹可能出现错误")
        finally:
            self.logout()
            return isTrue  
    
    def checkInboxCnt(self):
        '''获取邮件数量'''
        try:
            isTrue = 0
            self.server.login(self.username, self.password) 
            
            self._into("INBOX")
            Uids = self._getUIDs()
            # 数量为 0
            if len(Uids) == 0:
                return 0
            # 判断
            if len(Uids) == 100:
                print("100封邮件")
                return 0
            elif len(Uids) < 100:
                print('邮件数量少于100封')
                return 0
            else:
                cnt = len(Uids) - 100
                print('需要删除邮件数量为：%d' %cnt)
                isTrue =  cnt
        except BaseException as error:
            print(error)
            print("删除邮件可能出现错误")
        finally:
            self.logout() 
            return  isTrue     
    
    def checkInbox(self):
        '''确保收件箱有100封邮件'''
        try:
            isTrue = True
            self.server.login(self.username, self.password) 
            
            self._into("INBOX")
            Uids = self._getUIDs()
            all = len(Uids)
            # 数量为 0
            if all == 0:
                return False
            # 判断
            if all == 100:
                print("100封邮件")
                return isTrue
            elif all < 100:
                print('邮件数量少于100封')
                return False
            else:
                print('需要删除邮件数量为：%d' %(all - 100))
#                 print(Uids[100:])
                self._del(Uids[100:])
                return isTrue      
        except BaseException as error:
            print(error)
            print("删除邮件可能出现错误")
            isTrue = False
        finally:
            self.logout()  
            return isTrue

if __name__ == '__main__':
    eo = EmailOperation("13580491603@139.com","chinasoft123")
#     eo.moveForlder(['INBOX','100' ]) 
#     eo.moveForlder(['100', 'INBOX']) 
#     eo.clearForlder(['已发送','已删除'])
    eo.checkInbox()
