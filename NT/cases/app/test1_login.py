import unittest
from NT.common.log import MyLog
from NT.common.base_page import BasePage
from NT.common.read_config import ReadConfig


class AppLogin(unittest.TestCase):
    """登录"""

    def setUp(self):
        try:
            config = ReadConfig()
            self.base_page = BasePage()
            self.log = MyLog().get_log().logger
            self.user_name = config.get_app_param("user_name")
            self.password = config.get_app_param("password")
        except Exception as e:
            self.log.error(e)
            raise Exception("出现异常！")

    def test_app_login(self):
        """app登录"""
        username_input = ("css_selector", "input[type='text']")  # 用户名输入框定位信息
        password_input = ("css_selector", "input[type='password']")  # 密码输入框定位信息
        login_button = ("css_selector", "button.button.button-block.button-calm")  # 登录按钮定位信息
        bottom_menu = ("css_selector", "span.tab-title.ng-binding")  # 底部menu
        answer_sheet_elem = ("css_selector", "button.button.button-calm.exam-button")  # 答题页面的“答题卡”按钮
        submit_button = ("css_selector", "button.button.button-block.button-calm")  # 提交按钮
        # 登录成功提示，有未答题提示，自动提交试卷提示
        popup_title = ("css_selector", "h3.popup-title.ng-binding")  # 提示框title

        try:
            # 用例开始，输入负责人姓名，必须
            self.base_page.case_start("李彬")

            self.log.debug("打开app")
            self.base_page.open_app()

            for i in range(1, 6, +1):
                # 未登录状态
                if self.base_page.displayed(login_button):
                    self.log.debug("输入用户名")
                    self.base_page.input_tag(username_input, self.user_name)
                    self.log.debug("输入密码")
                    self.base_page.input_tag(password_input, self.password)

                    self.base_page.screen_shot()
                    self.log.debug("点击登录按钮")
                    self.base_page.click_elem_tag(login_button)
                    self.base_page.screen_shot()
                    # 用弹框的标题断言
                    self.assertEqual(self.base_page.displayed(login_button), False, "登录失败！")

                    # 打印弹框上的信息
                    self.base_page.popup()
                    self.log.debug("进入首页！")
                    self.base_page.case_pass()
                    break
                # 有提示框(登录成功提示，自动交卷提示)
                elif self.base_page.displayed(popup_title):
                    # 打印弹框上的信息
                    self.base_page.popup()
                    self.base_page.back_to()  # 返回首页
                    self.log.debug("返回首页！")
                    self.base_page.case_pass()
                    break
                # 处于答题页面
                elif self.base_page.displayed(answer_sheet_elem):
                    self.log.debug("进入app后正处于答题页面，进入答题卡页面提交试卷，结束该次考试！")
                    self.base_page.screen_shot()
                    self.base_page.click_elem_tag(answer_sheet_elem)
                    # 点击提交按钮
                    self.base_page.click_elem_tag(submit_button)

                    # 未答题的提示框
                    self.base_page.popup()
                    self.base_page.back_to()  # 返回首页
                    self.log.debug("返回首页！")
                    self.base_page.case_pass()
                    break
                # 进入首页
                elif self.base_page.displayed(bottom_menu):
                    self.base_page.screen_shot()
                    self.log.debug("进入首页！")
                    self.base_page.case_pass()
                    break
            else:
                raise Exception("打开app时异常！")
        except Exception as e:
            self.log.error(e)
            # 用例失败，必须
            self.base_page.case_failed()
            raise Exception("出现异常！")

    def tearDown(self):
        self.base_page.case_end()
