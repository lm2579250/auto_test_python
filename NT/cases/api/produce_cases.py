import threading
from NT.common.log import MyLog
from NT.common.common import Common


class ProduceCases:
    """利用base_case.py自动生成所有api测试用例的请求函数类test_cases.py"""
    _instance_lock = threading.Lock()  # 设置单例锁

    def __new__(cls, *args, **kwargs):
        """单例模式(支持多线程)"""
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        try:
            self.log = MyLog.get_log().logger
            self.common = Common()
            self.api_cases_path, self.api_cases_dict = self.common.get_api_cases()
        except Exception as e:
            self.log.error(e)
            raise Exception("出现异常！")

    def produce_case(self):
        """生成所有api用例"""
        try:
            self.log.debug("api用例路径：%s" % self.api_cases_path)
            # self.log.debug(self.common.api_cases_dict)

            # 拼接用例解析函数模板(base_case.py)路径
            base_case_path = Common.get_path("cases", "api", "base_case.py")
            # 拼接存放生成的所有测试用例的文件路径
            test_cases_path = Common.get_path("cases", "api", "test_cases.py")

            with open(base_case_path, "r", encoding="utf-8") as file_old:  # 从file_old中读取
                with open(test_cases_path, "w", encoding="utf-8") as file_new:  # 写入file_new中

                    lines = file_old.readlines()  # 按行读取file_old中的所有数据

                    # 不需要改变的部分
                    i = 1  # 不需要改变的行号
                    for line in lines:
                        if "# 定位标记" in line:
                            break
                        file_new.write(line)
                        i += 1

                    # 需要改变的部分
                    n = 0  # 用例编号
                    global case_name  # 用例名
                    for origin, sheet_dict in self.api_cases_dict.items():
                        # key:origin(项目地址原点),value:sheet_dict(单个sheet中的用例集合)
                        for case_name, case_params in sheet_dict.items():
                            # key:case_name(用例名),value:case_params(一条用例)
                            n += 1
                            j = i  # 需要改变的行号
                            while j < len(lines):  # 动态生成一个用例
                                if "def test_case(self):" in lines[j]:
                                    line = lines[j].replace("test_case", "test_%s" % case_name)
                                elif "用例描述" in lines[j]:
                                    line = lines[j].replace("用例描述", str(case_params["remark"]))
                                elif "case_params = {}" in lines[j]:
                                    line = lines[j].replace("{}", str(case_params))
                                elif "origin = 'null'" in lines[j]:
                                    line = lines[j].replace("null", origin)
                                elif "case_name = 'null'" in lines[j]:
                                    line = lines[j].replace("null", case_name)
                                elif "case_num = 0" in lines[j]:
                                    line = lines[j].replace("0", str(n))
                                elif "self.execute_case" in lines[j]:
                                    line = lines[j] + "\n"
                                else:
                                    line = lines[j]  # 不在上边的其他行(空行)

                                file_new.write(line)
                                j += 1

                    self.log.debug("api用例数量：%s" % n)
                    self.log.debug("*" * 100 + "\n")
        except Exception as e:
            self.log.error(e)
            raise Exception("请检测用例%s格式是否正确！" % case_name)
