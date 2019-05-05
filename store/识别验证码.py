# coding:utf-8
from selenium import webdriver
from time import sleep
import unittest
from PIL import Image
from PIL import ImageEnhance
import pytesseract

# driver = webdriver.Firefox()
# url = "https://passport.baidu.com/?getpassindex"
# driver.get(url)
# driver.maximize_window()
# driver.save_screenshot(r"E:\aa.png")  # 截取当前网页，该网页有我们需要的验证码
# imagelement = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/form/div/div[3]/img")
# # imagelement = driver.find_element_by_id("code")  #定位验证码
# location = imagelement.location  # 获取验证码x,y轴坐标
# size = imagelement.size  # 获取验证码的长宽
# coderange = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
#              int(location['y'] + size['height']))  # 写成我们需要截取的位置坐标
# i = Image.open(r"E:\aa.png")  # 打开截图
# frame4 = i.crop(coderange)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
# frame4.save(r"E:\frame4.png")
# i2 = Image.open(r"E:\frame4.png")
i2 = Image.open(r'E:\t0121fcc5aaabf88851.jpg')
imgry = i2.convert('L')  # 图像加强，二值化，PIL中有九种不同模式。分别为1，L，P，RGB，RGBA，CMYK，YCbCr，I，F。L为灰度图像
sharpness = ImageEnhance.Contrast(imgry)  # 对比度增强
i3 = sharpness.enhance(3.0)  # 3.0为图像的饱和度
i3.save("E:\\image_code.png")
i4 = Image.open("E:\\image_code.png")
text = pytesseract.image_to_string(i4).strip()  # 使用image_to_string识别验证码
print(text)


# # -*-coding:utf-8-*-
# import requests
# from pytesseract import *
# from bs4 import BeautifulSoup
# from PIL import Image
#
# url = 'http://app.szzfgjj.com:7001/accountQuery'
# url_verify = "http://app.szzfgjj.com:7001/pages/code.jsp?yzm="
# session = requests.Session()
# ad = "F:\\Python\\python3\\"
# path = ad + "557" + ".jpg"
# accnum = input("请输入电脑号或者公积金账号：")
# certinum = input("请输入身份证号码：")
#
#
# def verify_code():
#     r = session.get(url_verify)
#     with open(path, "wb") as fd:
#         for chunk in r.iter_content(100):
#             fd.write(chunk)
#             # 下载图片 data=urllib.request.urlretrieve(urlyzm,path)
#     im = Image.open(path)
#     verify_x = pytesseract.image_to_string(im)
#     return verify_x
#
#
# def query_data(verify):
#     data_a = {}
#     if len(accnum) == 11:
#         data_a = {
#             "accnum": accnum,
#             "certinum": certinum,
#             "qryflag": 1,
#             "verify": verify
#         }
#     elif len(accnum) == 9:
#         data_a = {
#             "accnum": accnum,
#             "certinum": certinum,
#             "qryflag": 0,
#             "verify": verify
#         }
#     # y有公积金账号和电脑号查询两种方式
#     else:
#         print("请重新输入公积金账号或者电脑号：")
#     return data_a
#
#
# def query(data1):
#     rr = session.post(url, data=data1)
#     soup = BeautifulSoup(rr.text, "html.parser")
#     return soup
#
#
# if __name__ == '__main__':
#     i = 1
#     for i in range(10):
#         verify = verify_code()
#         data1 = query_data(verify=verify)
#         soup = query(data1=data1)
#         if "验证码错误" in str(soup):
#             print("验证码错误")
#         else:
#             print(soup)
#             break
#         i += 1


# # coding:utf-8
# import subprocess
# from PIL import Image
# from PIL import ImageOps
# from selenium import webdriver
# import time, os, sys
#
#
# def cleanImage(imagePath):
#     image = Image.open(imagePath)  # 打开图片
#     image = image.point(lambda x: 0 if x < 143 else 255)  # 处理图片上的每个像素点，使图片上每个点“非黑即白”
#     borderImage = ImageOps.expand(image, border=20, fill='white')
#     borderImage.save(imagePath)
#
#
# def getAuthCode(driver, url="http://localhost/"):
#     captchaUrl = url + "common/random"
#     driver.get(captchaUrl)
#     time.sleep(0.5)
#     driver.save_screenshot("captcha.jpg")  # 截屏，并保存图片
#     # urlretrieve(captchaUrl, "captcha.jpg")
#     time.sleep(0.5)
#     cleanImage("captcha.jpg")
#     p = subprocess.Popen(["tesseract", "captcha.jpg", "captcha"], stdout= \
#         subprocess.PIPE, stderr=subprocess.PIPE)
#     p.wait()
#     f = open("captcha.txt", "r")
#
#     # Clean any whitespace characters
#     captchaResponse = f.read().replace(" ", "").replace("\n", "")
#
#     print("Captcha solution attempt: " + captchaResponse)
#     if len(captchaResponse) == 4:
#         return captchaResponse
#     else:
#         return False
#
#
# def withoutCookieLogin(url="http://org.cfu666.com/"):
#     driver = webdriver.Chrome()
#     driver.maximize_window()
#     driver.get(url)
#     while True:
#         authCode = getAuthCode(driver, url)
#         if authCode:
#             driver.back()
#             driver.find_element_by_xpath("//input[@id='orgCode' and @name='orgCode']").clear()
#             driver.find_element_by_xpath("//input[@id='orgCode' and @name='orgCode']").send_keys("orgCode")
#             driver.find_element_by_xpath("//input[@id='account' and @name='username']").clear()
#             driver.find_element_by_xpath("//input[@id='account' and @name='username']").send_keys("username")
#             driver.find_element_by_xpath("//input[@type='password' and @name='password']").clear()
#             driver.find_element_by_xpath("//input[@type='password' and @name='password']").send_keys("password")
#             driver.find_element_by_xpath("//input[@type='text' and @name='authCode']").send_keys(authCode)
#             driver.find_element_by_xpath("//button[@type='submit']").click()
#             try:
#                 time.sleep(3)
#                 driver.find_element_by_xpath("//*[@id='side-menu']/li[2]/ul/li/a").click()
#                 return driver
#             except:
#                 print("authCode Error:", authCode)
#                 driver.refresh()
#     return driver
#
#
# driver = withoutCookieLogin("http://localhost/")
# driver.get("http://localhost/enterprise/add/")


# -*- coding: utf-8 -*-
# Author：哈士奇说喵
# from selenium import webdriver
# import os
# import pytesser3, csv
# import sys, time
# from PIL import Image, ImageEnhance
# import importlib

# # shift+tab多行缩进(左)
#
# importlib.reload(sys)
# PostUrl = "https://login.bce.baidu.com/"
#
# driver = webdriver.Firefox()
# driver.get(PostUrl)
#
# i = 0
# # while 1:  # sb登录系统，即使输对所有消息还是登不进去的，需要登录两次及以上
#
# i = i + 1
#
# # elem_user = driver.find_element_by_name('id')
# # elem_psw = driver.find_element_by_name('password')
# # elem_code = driver.find_element_by_name('checkcode')
#
# driver.find_element_by_id('TANGRAM__PSP_4__userName').send_keys('1111111')
# driver.find_element_by_id('TANGRAM__PSP_4__password').send_keys('111111111')
# time.sleep(3)
# driver.find_element_by_id('TANGRAM__PSP_4__submit').click()
#
# # -------------------对验证码进行区域截图，好吧，这方法有点low------------------
# driver.get_screenshot_as_file('F:\Python\python3\image1.jpg')  # 比较好理解
# im = Image.open('F:\Python\python3\image1.jpg')
# box = (516, 417, 564, 437)  # 设置要裁剪的区域
# region = im.crop(box)  # 此时，region是一个新的图像对象。
# # region.show()#显示的话就会被占用，所以要注释掉
# region.save("F:\Python\python3\image_code1.jpg")

# -------------------------------------------------------------------

# --------------ImageGrab.grab()直接可以区域截图，但是有bug，截图不全-------
# '''
# bbox = (780, 0, 1020, 800)
# img = ImageGrab.grab()
# img.save("F:\Python\python3\image_code.jpg")
# img.show()
# '''
# # -------------------------手动输入验证码：适用范围更广，但不够方便------------------------------
# '''
# response = opener.open(CaptchaUrl)
# picture = response.read()
# with open('F:\Python\python3\image.jpg', 'wb') as local:
#     local.write(picture)
# # 保存验证码到本地
#
# #------------对于不能用pytesser+ocr进行识别，手动打开图片手动输入--------
# # 打开保存的验证码图片 输入
# #SecretCode = raw_input('please enter the code: ')
# #----------------------------------------------------------------------
# '''
#
#
# # --------------------图片增强+自动识别简单验证码-----------------------------
# # time.sleep(3)防止由于网速，可能图片还没保存好，就开始识别
# def image_file_to_string(file):
#     cwd = os.getcwd()
#     try:
#         os.chdir("E:\Program Files (x86)\python3.6\Lib")
#         return pytesser.image_file_to_string(file)
#     finally:
#         os.chdir(cwd)
#
#
# im = Image.open("F:\Python\python3\image_code.jpg")
# imgry = im.convert('L')  # 图像加强，二值化
# sharpness = ImageEnhance.Contrast(imgry)  # 对比度增强
# sharp_img = sharpness.enhance(2.0)
# sharp_img.save("F:\Python\python3\image_code.jpg")
# # http://www.cnblogs.com/txw1958/archive/2012/02/21/2361330.html
# # imgry.show()#这是分布测试时候用的，整个程序使用需要注释掉
# # imgry.save("E:\\image_code.jpg")
#
# code = pytesseract.image_to_string("F:\Python\python3\image_code.jpg").strip()
# # code = pytesser3.image_file_to_string("F:\Python\python3\image_code.jpg")  # code即为识别出的图片数字str类型
# print(code)
# 打印code观察是否识别正确

# ----------------------------------------------------------------------
# if i <= 2:  # 根据自己登录特性，我这里是验证码失败一次，重填所有，失败两次，重填验证码
#     elem_user.send_keys('S315080092')
#     elem_psw.send_keys('xxxxxxxxxx')
#
# elem_code.send_keys(code)
# click_login = driver.find_element_by_xpath("//img[@src='main_images/images/loginbutton.gif']")
# click_login.click()

# time.sleep(5)#搜索结果页面停留片刻
# driver.save_screenshot('C:\Users\MrLevo\image.jpg')
# driver.close()
# driver.quit()
