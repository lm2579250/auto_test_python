import os
import openpyxl
import threading
from datetime import datetime


class Common(object):
    """公用函数"""
    # 用例开始执行时间作文件夹名
    start_time = str(datetime.now().strftime("%Y%m%d%H%M%S"))
    _instance_lock = threading.Lock()  # 设置单例锁

    def __new__(cls, *args, **kwargs):
        """单例模式(支持多线程)"""
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = object.__new__(cls)
        return cls._instance

    @staticmethod
    def get_path(*args):
        """生成路径，参数为文件夹名或文件名，无参时为项目根路径"""
        try:
            # 获取当前目录的父目录路径(项目根路径)
            path = str(os.path.dirname(os.path.dirname(__file__)))

            # 循环生成路径
            for value in args:
                path = os.path.join(path, value).replace("\\", "/")
                # 不存在则创建文件夹/文件
                if not os.path.exists(path) and "." not in value:
                    os.mkdir(path)
            return path
        except Exception as e:
            raise Exception("函数Common.get_path异常：%s" % e)

    def get_result_path(self, *args):
        """result目录下的日志，报告，截图路径"""
        # 自动生成result父目录和时间子目录，以及时间目录下的各级子目录
        log_path = Common.get_path("result", self.start_time, *args)
        return log_path

    @staticmethod
    def get_api_cases():
        """从Excel中读取cases"""
        try:
            # 拼接接口用例api_cases.xlsx路径
            api_cases_path = Common.get_path("data", "api_cases.xlsx")

            # 打开xls文件
            wb = openpyxl.load_workbook(api_cases_path)
            # 获取workbook中所有的sheet
            sheets = wb.sheetnames

            # case_dict结构： case_dict = {case_key:case_value}/case_dict = {case_key:{param_key: param_value}}
            # case_value = {param_key: param_value}
            cases_dict = {}  # case字典
            case_key = []  # case_dict的key
            case_value = {}  # case_dict的value
            case_param_key = []  # case_value的key
            # case_param_value = ""  # case_value的value

            # 循环遍历所有sheet
            for i in range(len(sheets)):
                sheet = wb[sheets[i]]
                # print("正在读取的sheet:%s" % wb.active)
                # print("正在读取的sheet名:%s" % sheet.title)

                # 循环遍历所有行
                for r in range(1, sheet.max_row + 1):
                    # 第一行为参数类型，用list case_param_key保存（从第二列开始，第一列为用例名）
                    if r == 1:
                        for c in range(2, sheet.max_column + 1):
                            param_key = sheet.cell(row=r, column=c).value
                            case_param_key.append(param_key)
                    elif sheet.cell(row=r, column=1).value is not None:
                        # 从第二行开始的第一列为用例名，用list case_key保存
                        key = sheet.cell(row=r, column=1).value
                        case_key.append(key)
                        # 从第二行的第二列开始为用例数据，用字符串 case_param_value保存
                        for c in range(2, sheet.max_column + 1):
                            case_param_value = sheet.cell(row=r, column=c).value
                            # 将参数类型case_param_key和用例数据组case_param_value成字典case_value
                            case_value[case_param_key[c - 2]] = case_param_value
                        # 将第一列的用例名case_key和用例数据字典case_value组成用例字典case_dict
                        cases_dict[case_key[r - 2]] = case_value
                        case_value = {}

                return api_cases_path, cases_dict
        except Exception as e:
            raise Exception("Common.get_api_cases异常 %s" % e)
