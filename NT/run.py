import unittest
from NT.common.log import MyLog
from NT.common.common import Common
from NT.common.send_email import SendEmail
from BeautifulReport import BeautifulReport
from NT.cases.api.produce_cases import ProduceCases
from NT.cases.web.test_login import WebLogin
from NT.cases.app.test1_login import AppLogin
from NT.cases.app.test_exams import AppExams
from NT.cases.app.test_survey import AppSurvey
from NT.cases.app.test_practice import AppPractice
from NT.cases.app.test_curriculum import AppCurriculum
from NT.cases.app.test_courseware import AppCourseware
from NT.cases.app.test_operation import AppOperation


class Run(object):
    def __init__(self):
        self.common = Common()
        self.my_log = MyLog()
        self.send_email = SendEmail()
        self.cases = ProduceCases()
        self.cases.produce_case()  # 自动生成接口测试用例
        self.path = self.common.get_result_path()  # 获取报告存储路径
        self.log = self.my_log.get_log().logger  # log日志
        self.suit = unittest.TestSuite()  # 测试套件（定义执行顺序）

    # 方式一：
    def add_api_test(self):
        """添加api测试用例"""
        from NT.cases.api.test_cases import APITestCases  # 生成所有接口测试用例后导入TestCases类

        for case_name, case_params in self.common.api_cases_dict.items():
            self.suit.addTest(APITestCases("test_%s" % case_name))

    # 方式一：
    def add_ui_test(self):
        """添加ui测试用例"""
        self.suit.addTest(WebLogin("test_web_login"))  # web登录
        self.suit.addTest(AppLogin("test_app_login"))  # app登录
        self.suit.addTest(AppOperation("test_app_operation"))  # 技术操作考核
        self.suit.addTest(AppExams("test_app_exams"))  # 考试
        self.suit.addTest(AppPractice("test_app_practice"))  # 练习
        self.suit.addTest(AppSurvey("test_app_survey"))  # 问卷调查
        self.suit.addTest(AppCurriculum("test_app_curriculum"))  # 课程学习
        self.suit.addTest(AppCourseware("test_app_courseware"))  # 课件学习

    # 方式二：
    def add_cases(self):
        """添加所有测试用例"""
        cases_path = self.common.get_path("cases")  # 用例路径
        cases_file = "test*.py"  # 用例文件或用例模式
        discover = unittest.defaultTestLoader.discover(cases_path, pattern=cases_file, top_level_dir=None)
        return discover

    # 方式二：
    def run_cases(self, case):
        """执行用例并生成报告"""
        result = BeautifulReport(case)
        result.report(log_path=self.path, filename="NT_测试报告.html", description='NT自动化测试')


if __name__ == "__main__":
    run = Run()
    common = Common()
    start_time = common.get_now_time()
    # 方式一：
    # run.add_api_test()
    # run.add_ui_test()
    # BeautifulReport(run.suit).report(log_path=run.path, filename="NT_测试报告.html", description='NT自动化测试')

    #  方式二：
    cases = run.add_cases()
    run.run_cases(cases)

    # 提取错误日志
    run.my_log.extraction_error_log()
    # 发送email
    run.send_email.with_zip()
    end_time = common.get_now_time()
    run.log.debug("耗时：%s s" % common.interval(start_time, end_time))
