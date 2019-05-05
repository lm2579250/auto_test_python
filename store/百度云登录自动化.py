# -*- coding: UTF-8 -*-

import unittest
import csv, time
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

class baiduyunLogin():
    def login():
        with open('F:\Python\python3\百度云登录自动化参数.csv') as csvfile:
            parameter = csv.reader(csvfile)
            driver = webdriver.Firefox()
            for row in parameter:
                driver.get('https://login.bce.baidu.com/')
                driver.find_element_by_id('TANGRAM__PSP_4__userName').send_keys(row[0])
                driver.find_element_by_id('TANGRAM__PSP_4__password').send_keys(row[1])
                time.sleep(3)
                driver.find_element_by_id('TANGRAM__PSP_4__submit').click()
                time.sleep(5)
            driver.close()

if __name__ == '__main__':
    baiduyunLogin.login()
