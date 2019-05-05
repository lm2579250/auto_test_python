# -*- coding: UTF-8 -*-
# 从文件中读取数据
# import xml.etree.ElementTree as ET
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

class ReadXml():
    # 字典编号
    global id
    id = 1

    def get_xml_data(file_name):
        count = 1  # 子节点下的元素数量统计
        result_list = []
        ele_dict = {}
        root = ET.parse(file_name).getroot()
        ReadXml.walk_data(root, count, ele_dict, result_list)
        return result_list

    # 遍历所有的节点
    def walk_data(root_node, count, ele_dict, result_list):
        global id

        # 遍历每个子节点
        children_node = root_node.getchildren()

        for child in children_node:
            if len(child.getchildren()) == 0:
                ele_dict["id"] = id
                ele_dict["count"] = count
                ele_dict[child.tag] = child.text
                count += 1
            else:
                ReadXml.walk_data(child, count, ele_dict, result_list)
                ele_dict["node"] = child.tag
                result_list.append(ele_dict)
                ele_dict = {}
                id += 1

if __name__ == "__main__":
    file_name = r"E:\Python\hospitals\test_case\common\variables.xml"
    dict_list = ReadXml.get_xml_data(file_name)
    for dict in dict_list:
        print("字典长度：", len(dict), dict)
        for key in dict:
            print(key, dict[key])
    pass