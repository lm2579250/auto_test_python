# coding=utf-8

import xml.dom.minidom

dom = xml.dom.minidom.parse(r'F:\Python\python3\python读取xml内容.xml')  # 打开xml文档
root = dom.documentElement  # 得到文档元素对象
# print(root.nodeName, root.nodeValue, root.nodeType, root.ELEMENT_NODE)
bb = root.getElementsByTagName('maxid')
b = bb[0]
print(b.nodeName)

login = root.getElementsByTagName('login')
oneLogin = login[0]
username = oneLogin.getAttribute("username")
print(username)
pswd = oneLogin.getAttribute('passwd')
print(pswd)

caption = root.getElementsByTagName('caption')
c1 = caption[0]
print(c1.firstChild.data)
c2 = caption[1]
print(c2.firstChild.data)
c3 = caption[2]
print(c3.firstChild.data)
c4 = caption[3]
print(c4.firstChild.data)

item = root.getElementsByTagName('item')
i1 = item[0]
i = i1.getAttribute('id')
print(i)
i2 = item[1]
i = i2.getAttribute('id')
print(i)

# 获得标签对之间的数据第二种方法
from xml.etree import ElementTree as ET

per = ET.parse(r'F:\Python\python3\python读取xml内容.xml')

catalog = per.findall('login')
for tag in catalog:
    for child in tag.getchildren():
        print(child.tag, ':', child.text)

loginitem = per.findall('./login/item')
for oneper in loginitem:
    for child in oneper.getchildren():
        print(child.tag, ':', child.text)

item2 = per.findall('./item')

for oneper in item2:
    for child in oneper.getchildren():
        print(child.tag, ':', child.text)


