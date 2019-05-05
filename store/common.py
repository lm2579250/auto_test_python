import os
import xlrd
import random
from datetime import datetime

global case_name


# 获取当前时间
def get_now_time():
    format = "%Y_%m_%d %H_%M_%S"
    return datetime.now().strftime(format)


def get_now_time_str():
    # 字符串祛空格和下划线
    # time = common.get_now_time()
    # i = time.replace('_', '')
    # j = i.replace(' ', '')
    format = "%H%M%S"
    return datetime.now().strftime(format)


# 计算时间差
def interval(start_time, end_time):
    format = "%Y_%m_%d %H_%M_%S"
    return datetime.strptime(end_time, format) - datetime.strptime(start_time, format)


time = get_now_time()


# 设置日志路径
def setting_log_path():
    try:
        path = "./TestReport/log/"

        if not os.path.exists(path):
            os.makedirs(path)

        path = path + "%s.log" % time
    except Exception as e:
        return Exception(e)
    return path


# 设置测试报告路径
def setting_report_path():
    try:
        path = "./TestReport/ReportHtml/"

        if not os.path.exists(path):
            os.makedirs(path)
        path = path + "%s.html" % time
    except Exception as e:
        raise Exception(e)
    finally:
        return path


# 设置截图保存路径
def setting_screenshot_path():
    try:
        path = "./TestReport/Screenshot/" + time + "/" + case_name + "/"

        if not os.path.exists(path):
            os.makedirs(path)
    except Exception as e:
        raise Exception(e)
    finally:
        return path


# 生成手机号
def generate_phone_number():
    i = [130, 131, 132, 140, 145, 146, 155, 156, 166, 185, 186, 175, 176]
    j = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    number = random.sample(j, 8)
    number.insert(0, random.choice(i))
    phone_number = int(''.join(str(n) for n in number))
    return phone_number


# 上传
def upload(obj):
    try:
        os.system(".\Data\\upload.exe %s" % obj)
    except:
        os.system("..\Data\\upload.exe %s" % obj)


# 读取参数
def get_parameter():
    #  文件位置
    try:
        excel_file = xlrd.open_workbook('./Data/data.xlsx')
    except:
        excel_file = xlrd.open_workbook('../Data/data.xlsx')
    #  获取Excel文件sheet名
    sheet = excel_file.sheet_by_name('Sheet1')
    rows = sheet.nrows
    # 获取单元格内容
    system = ""
    user = []
    uid_and_version = []
    app_info = []
    app = ""
    for i in range(0, rows):
        if "system" == sheet.cell(i, 0).value:
            system = sheet.cell(i, 1).value
        if "uid_and_version" == sheet.cell(i, 0).value:
            uid_and_version = [sheet.cell(i, 1).value, sheet.cell(i, 2).value]
        if "user" == sheet.cell(i, 0).value:
            user = [sheet.cell(i, 1).value, sheet.cell(i, 2).value]
        if "app_info" == sheet.cell(i, 0).value:
            app_info = [sheet.cell(i, 1).value, sheet.cell(i, 2).value]
        if "app" == sheet.cell(i, 0).value:
            app = sheet.cell(i, 1).value
    return system, uid_and_version, user, app_info, app


if __name__ == "__main__":
    # 手机号
    phone_number = generate_phone_number()
    print(phone_number)

    # 读取excel
#     Data = get_parameter()
#     print(Data)
#     print("system")
#     print(Data[0])
#     print("uid_and_version")
#     print(Data[1][0], Data[1][1])
#     print("user")
#     print(Data[2][0], Data[2][1])
#     print("app_info")
#     print(Data[3][0], Data[3][1])
#     print("app_address")
#     print(Data[4])
