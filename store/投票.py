#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get("http://survey.people.com.cn/survey_101185/wap.html?from=groupmessage&isappinstalled=0")
time.sleep(2)
driver.find_element_by_xpath("//ol/li[13]/em/input").click()
driver.find_element_by_link_text("提 交").click()
time.sleep(2)
driver.switchTo().alert().
time.sleep(2)
driver.quit()
