import unittest
from NT.common.log import MyLog
from NT.common.common import Common
from NT.common.send_email import SendEmail
from BeautifulReport import BeautifulReport
from NT.cases.api.alter_case import AlterCase
from NT.cases.web.login import WebLogin
from NT.cases.app.login import AppLogin
from NT.cases.app.exams import AppExams
from NT.cases.app.survey import AppSurvey
from NT.cases.app.practice import AppPractice
from NT.cases.app.curriculum import AppCurriculum
from NT.cases.app.courseware import AppCourseware
from NT.cases.app.technical_operation import AppTechnicalOperation


class Run(object):
    def __init__(self):
        self.common = Common()
        self.my_log = MyLog()
        self.alter_case = AlterCase()
        self.send_email = SendEmail()
        self.alter_case = AlterCase()
        # 获取报告存储路径
        self.path = self.common.get_result_path()
        # 生成所有api用例解析函数类TestCases
        self.alter_case.produce_case()
        # 获取api用例路径和用例dict
        self.cases_path, self.cases_dict = self.common.get_api_cases()
        # log日志
        self.log = self.my_log.get_log().logger
        # 测试套件（定义执行顺序）
        self.suit = unittest.TestSuite()

    def api_test(self):
        """api测试"""
        # self.log.info("用例路径：%s" % self.cases_path)
        # self.log.debug(self.cases_dict)
        # 生成所有用例解析函数类后导入TestCases
        from NT.cases.api.test_cases import APITestCases

        for case_name, case_params in self.cases_dict.items():
            self.suit.addTest(APITestCases("test_%s" % case_name))

    def ui_test(self):
        """ui测试"""
        self.suit.addTest(WebLogin("test_web_login"))  # web登录
        self.suit.addTest(AppLogin("test_app_login"))  # app登录
        self.suit.addTest(AppTechnicalOperation("test_app_operation"))  # 技术操作考核
        self.suit.addTest(AppExams("test_app_exams"))  # 考试
        self.suit.addTest(AppPractice("test_app_practice"))  # 练习
        self.suit.addTest(AppSurvey("test_app_survey"))  # 问卷调查
        self.suit.addTest(AppCurriculum("test_app_curriculum"))  # 课程学习
        self.suit.addTest(AppCourseware("test_app_courseware"))  # 课件学习


if __name__ == "__main__":
    run = Run()
    run.api_test()
    run.ui_test()

    # 生成测试报告：
    BeautifulReport(run.suit).report(log_path=run.path, filename="NT_测试报告.html", description='NT_测试报告')
    # 提取错误日志
    run.my_log.extraction_error_log()
    # 发送email
    # run.send_email.with_zip()

