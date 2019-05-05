# -*- coding: utf_8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import os

try:
    # driver = webdriver.Firefox()
    driver = webdriver.Chrome()
    HomeUrl = 'http://bbs.xiaomi.cn/'
    driver.get(HomeUrl)
    OnePageNum = len(driver.find_elements_by_xpath('/html/body/div[1]/div[3]/div[2]/div[2]/div/ul/li'))
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div[2]/div/div[2]/div/ul/li[12]/a').click()
    EndPageNum = len(driver.find_elements_by_xpath('/html/body/div[1]/div[3]/div[2]/div[2]/div/ul/li'))
    EndPage = int(
        driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div[2]/div/div[2]/div/ul/li[10]/a').text)
    print('共%s*%s+%s=%s条\n' % (OnePageNum, EndPage - 1, EndPageNum, OnePageNum * (EndPage - 1) + EndPageNum))
    PageUrl = 'http://bbs.xiaomi.cn/d-{page}'
    file = '.\小米论坛爬虫.txt'
    num = 1
    if os.path.exists(file) == False:  # 如果文件不存在
        with open(file, 'w+', encoding='utf-8') as f:
            f.truncate()
            f.write('共%s*%s+%s=%s条\n' % (OnePageNum, EndPage - 1, EndPageNum, OnePageNum * (EndPage - 1) + EndPageNum))
    else:
        with open(file, 'w+', encoding='utf-8') as f:
            f.truncate()
            f.write('共%s*%s+%s=%s条\n' % (OnePageNum, EndPage - 1, EndPageNum, OnePageNum * (EndPage - 1) + EndPageNum))
    for i in range(1, EndPage):
        url = PageUrl.format(page=i)
        driver.get(url)
        PageSource = BeautifulSoup(driver.page_source, 'html.parser')
        Titles = PageSource.find_all('div', {'class': 'title'})

        for title in Titles:
            title_content = title.get_text().strip('\n').strip()
            with open(file, 'a+', encoding='utf-8') as f:
                f.write('%s.%s%s\n' % (num, ' ' * 2, title_content))
                print('%s.%s%s\n' % (num, ' ' * 2, title_content))
                num += 1
    driver.close()
    driver.quit()
except Exception as e:
    print("出错了！", e)
finally:
    print("结束")
