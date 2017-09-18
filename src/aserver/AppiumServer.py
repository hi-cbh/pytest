
import os
import time
import urllib.request
from urllib.error import URLError
from multiprocessing import Process
import threading


'''方式1：启动appium'''
class AppiumServer:

    def __init__(self):
        global openAppium, baseUrl
#         openAppium = readConfigLocal.getcmdValue("openAppium")
#         baseUrl = readConfigLocal.getConfigValue("baseUrl")

    def start_server(self):
        """start the appium server
        :return:
        """
        oa = "node \"C:\\Program Files (x86)\\Appium\\node_modules\\appium\\bin\\appium.js\""
        t1 = RunServer(oa)
        p = Process(target=t1.start())
        p.start()

    def stop_server(self):
        """stop the appium server
        :return:
        """
        # kill myServer
        os.popen('taskkill /F /IM node.exe')

    def re_start_server(self):
        """reStart the appium server
        """
        self.stop_server()
        self.start_server()

    def is_runnnig(self):
        """Determine whether server is running
        :return:True or False
        """
        response = None
        url = baseUrl+"/status"
        try:
            response = urllib.request.urlopen(url, timeout=5)

            if str(response.getcode()).startswith("2"):
                return True
            else:
                return False
        except URLError:
            return False
        finally:
            if response:
                response.close()

'''方式1：启动appium'''
class AppiumServer2:
    def __init__(self):
        global openAppium, baseUrl
#         openAppium = readConfigLocal.getcmdValue("openAppium")
#         baseUrl = readConfigLocal.getConfigValue("baseUrl")

    def start_server(self):
        """start the appium server
        :return:
        """
        t1 = RunServer("start D:\\workspace\\workspace_python3\\appium_python\\bat\\startAppiumServer.bat")
        p = Process(target=t1.start())
        p.start()

    def stop_server(self):
        """stop the appium server
        :return:
        """
        t1 = RunServer("start D:\\workspace\\workspace_python3\\appium_python\\bat\\stopAppiumServer.bat")
        p = Process(target=t1.start())
        p.start()




class RunServer(threading.Thread):

    def __init__(self, cmd):
        threading.Thread.__init__(self)
        self.cmd = cmd

    def run(self):
        os.system(self.cmd)


if __name__ == "__main__":

    oo = AppiumServer2()
    oo.start_server()
    print("start server")
    print("running server")
     
    time.sleep(10)
    oo.stop_server()
    print("stop server")