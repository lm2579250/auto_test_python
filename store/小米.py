# coding:utf-8
from splinter import Browser
import time, threading


def qq_mail_login(url=None, username=None, password=None):
    with Browser(driver_name="chrome") as browser:
        browser.visit(url[0])
        # 进入登录界面
        browser.click_link_by_href("//order.mi.com/site/login?redirectUrl=http://www.mi.com/")
        # 输入用户名密码，完成登录
        browser.find_by_id(u"username").first.fill(username)
        browser.find_by_id(u"pwd").first.fill(password)
        browser.find_by_id("login-button").first.click()
        time.sleep(1)
        # 进入购买界面
        browser.visit(url[1])
        # 点击购买“下一步”
        count = 1
        while not browser.is_element_not_present_by_id('J_chooseResultInit'):
            print("第", count, "次： ", browser.is_element_not_present_by_id('J_chooseResultInit'))
            time.sleep(10)
            count += 1
        browser.find_by_id("J_chooseResultInit").first.click()
        quit_browser(browser)


def quit_browser(browser=None):
    flag = input("Input q when you want to quit: ")
    if 'q' == str(flag):
        quit(browser)


if __name__ == '__main__':
    url = ["http://www.mi.com/", "http://item.mi.com/buyphone/mix/"]
    username = "597878110@qq.com"
    password = "@lsym2579250!"
    # t1 = threading.Thread(target=qq_mail_login,args=(url,username,password))
    # t1.start()
    # t1.join()
    qq_mail_login(url, username, password)
