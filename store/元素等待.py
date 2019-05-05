# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
driver = webdriver.Firefox()
driver.get("https://passport.baidu.com/v2/?login&u=http://wenku.baidu.com/user/myinfo")
driver.maximize_window()
time.sleep(2)
driver.find_element_by_id('TANGRAM__PSP_3__footerULoginBtn').click()

try:
    """这段可以查看selenium的源码,属于smart wait"""
    email = WebDriverWait(driver, timeout=10).until(EC.presence_of_element_located((By.ID, 'TANGRAM__PSP_3__userNameWrapper')), message=u'元素加载超时!')
    email.send_keys("597878110@qq.com")
    passwd = WebDriverWait(driver, timeout=10).until(EC.presence_of_element_located((By.ID, 'TANGRAM__PSP_3__passwordWrapper')), message=u'元素加载超时!')
    passwd.send_keys("lsym2579250bdy")
    driver.find_element_by_id("TANGRAM__PSP_3__submit").click() #点击登录
except NoSuchElementException as e:
    print(e.message)