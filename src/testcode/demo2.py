#!/user/bin/env python
# -*-coding:utf-8-*-
# @time       : 16/11/8 12:09
# @Author     : Zhangxy
# @File       : 001baiduSearch.py
# @Software   : PyCharm


from selenium import webdriver
driver = webdriver.Chrome("chromedriver")
driver.get("http://www.baidu.com")
driver.find_element_by_id('kw').send_keys('selenium')
driver.find_element_by_id('su').click()
driver.quit()