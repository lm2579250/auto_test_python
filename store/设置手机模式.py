# -*- coding: utf-8 -*-
from selenium import webdriver
from time import sleep


mobileEmulation = {'deviceName': 'Apple iPhone 6'}
options = webdriver.ChromeOptions()
options.add_experimental_option('mobileEmulation', mobileEmulation)

driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)
driver.set_window_size(390, 760)
driver.get('http://histest.mobimedical.cn/index.php?g=Wap&m=CloudIndex&a=index&wx=NbDXANO0O0Ok&openid=oHdcPs_fblVqELOJjUJQp8gfWnVY')
sleep(10)
# driver.close()
'''
WIDTH = 414
HEIGHT = 808
PIXEL_RATIO = 3.0
UA = 'Mozilla/5.0 (Linux; Android 4.1.1; GT-N7100 Build/JRO03C) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/6.3'

mobileEmulation = {"deviceMetrics": {"width": WIDTH, "height": HEIGHT, "pixelRatio": PIXEL_RATIO}, "userAgent": UA}
options = webdriver.ChromeOptions()
options.add_experimental_option('mobileEmulation', mobileEmulation)
driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)
driver.set_window_size(414, 808)
driver.get('http://histest.mobimedical.cn/index.php?g=Wap&m=CloudIndex&a=index&wx=NbDXANO0O0Ok&openid=oHdcPs_fblVqELOJjUJQp8gfWnVY')

sleep(10)
driver.close()
'''