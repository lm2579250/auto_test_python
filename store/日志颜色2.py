#!/usr/bin/env python3

sites = ["baidu","runoob","google","taobao"]
for site in sites:
    if site == "runoob":
        print("菜鸟教程")
        break
    print("循环数据"+site)
else:
    print("没有循环数据")
print("完成循环")

sites = ["baidu","runoob","google","taobao"]
for site in range(len(sites)):
    if sites[site] == "runoob":
        print("菜鸟教程")
        break
    print(site,sites[site])
else:
    print("没有循环数据")
print("完成循环")


sites = 'Python'
for site in range(len(sites)):
    print(site)
    print(sites)
    print(sites[site])


for site in range(5):
    print(site)

'''
 1 格式：\033[显示方式;前景色;背景色m
 2
 3 说明：
 4 前景色            背景色           颜色
 5 ---------------------------------------
 6 30                40              黑色
 7 31                41              红色
 8 32                42              绿色
 9 33                43              黃色
10 34                44              蓝色
11 35                45              紫红色
12 36                46              青蓝色
13 37                47              白色
14 显示方式           意义
15 -------------------------
16 0                终端默认设置
17 1                高亮显示
18 4                使用下划线
19 5                闪烁
20 7                反白显示
21 8                不可见
22
23 例子：
24 \033[1;31;40m    <!--1-高亮显示 31-前景色红色  40-背景色黑色-->
25 \033[0m          <!--采用终端默认设置，即取消颜色设置-->
'''
print('\033[1;31;40m')
print('*' * 50)
print('*HOST:\t', 2002)
print('*URI:\t', 'http://127.0.0.1')
print('*ARGS:\t', 111)
print('*TIME:\t', '22:28')
print('*' * 50)
print('\033[0m')
print("\033[33;1mHello, world\033[0m")
print("\033[1;5;34;;4mHello, world\033[0m")
print('\033[34;1m进入一级科室\033[0m')
'''1-高亮 5-闪烁 33-前景色 44-背景色 4-下划线
\033[0m   采用终端默认设置，即取消颜色设置'''