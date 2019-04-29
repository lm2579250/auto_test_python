import threading
from NT.common.log import MyLog
from NT.common.common import Common


class AlterCase:
    """利用base_case.py自动生成所有api测试用例的请求函数"""
    _instance_lock = threading.Lock()  # 设置单例锁

    def __new__(cls, *args, **kwargs):
        """单例模式(支持多线程)"""
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        self.log = MyLog.get_log().logger
        self.cases_path, self.cases_dict = Common().get_api_cases()

    def produce_case(self):
        """生成所有api用例"""
        try:
            # 拼接用例解析函数模板(base_case.py)路径
            base_case_path = Common.get_path("cases", "api", "base_case.py")
            # 拼接存放生成的所有测试用例的文件名
            test_cases_path = Common.get_path("cases", "api", "test_cases.py")

            with open(base_case_path, "r", encoding="utf-8") as file_old:  # 从file_old中读取
                with open(test_cases_path, "w", encoding="utf-8") as file_new:  # 写入file_new中

                    lines = file_old.readlines()  # 读取file_old的每行数据
                    # 不需要改变的部分
                    i = 0  # 代码行数
                    for line in lines:
                        if "class TestCase(unittest.TestCase):" in line:
                            line = line.replace("class TestCase", "class APITestCases")
                        if "# 定位标记" in line:
                            break
                        file_new.write(line)
                        i += 1

                    # 需要改变的部分
                    n = 1  # 用例编号
                    global case_name
                    for case_name, case_params in self.cases_dict.items():
                        j = 0
                        for line in lines:
                            if j > i:
                                if "def test_case(self):" in line:
                                    line = line.replace("test_case", "test_%s" % case_name)
                                if "用例描述" in line:
                                    line = line.replace("用例描述", str(case_params["remark"]))
                                if "case_params = {}" in line:
                                    line = line.replace("{}", str(case_params))
                                if "case_num = 0" in line:
                                    line = line.replace("0", "%s" % n)
                                if "case_name = 'null'" in line:
                                    line = line.replace("null", case_name)
                                if "TestCase.execute_case" in line:
                                    line = line.replace("TestCase.execute_case", "APITestCases.execute_case")
                                file_new.write(line)
                            j += 1
                        n += 1
        except Exception as e:
            self.log.error("请检测用例%s格式是否正确！" % case_name)
            raise Exception(e)
