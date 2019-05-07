import unittest
from NT.common.log import MyLog
from NT.common.common import Common
from NT.common.base_page import BasePage
from NT.common.read_config import ReadConfig


class WebLogin(unittest.TestCase):
    """登录"""
    def setUp(self):
        try:
            config = ReadConfig()
            self.base_page = BasePage()
            self.common = Common()
            self.log = MyLog().get_log().logger

            self.url = config.get_web_param("url")
            self.user_name = config.get_web_param("user_name")
            self.password = config.get_web_param("password")
        except Exception as e:
            self.log.error(e)
            raise Exception

    @unittest.skip("暂不执行")
    def test_web_login(self):
        """web登录"""
        try:
            # 用例开始，输入负责人姓名，必须
            self.base_page.case_start("乔一庭")

            username_element = ("css_selector", "input.form-control.user")  # 用户名输入框定位信息
            password_element = ("css_selector", "input.form-control.psd")  # 密码输入框定位信息
            button_element = ("css_selector", "input.btn.btn-primary.btn-block.login-btn.submit")  # 登录按钮定位信息
            menu_elements = ("css_selector", "span.fa.fa-angle-right")  # 左边菜单栏，用于断言

            self.log.debug("打开浏览器")
            self.base_page.open_browser()
            self.base_page.screen_shot()
            self.log.debug("输入url")
            self.base_page.get(self.url, menu_elements)
            # 用登录按钮断言，成功打开登录页后，页面上有登录按钮
            self.assertEqual(self.base_page.displayed(button_element), True, "打开url时异常！")

            self.log.debug("输入用户名")
            self.base_page.input_tag(username_element, self.user_name)
            self.log.debug("输入密码")
            self.base_page.input_tag(password_element, self.password)
            self.base_page.screen_shot()
            self.log.debug("点击登录按钮")
            self.base_page.click_elem_tag(button_element)
            self.base_page.wait_elem(menu_elements)
            # 用左侧菜单，断言
            self.assertEqual(self.base_page.displayed(menu_elements), True, "登录失败！")
            self.base_page.screen_shot()

            # 用例成功，必须
            self.base_page.case_pass()
        except Exception as e:
            self.log.error(e)
            # 用例失败，必须
            self.base_page.case_failed()
            raise Exception

    def tearDown(self):
        try:
            self.log.debug("关闭网页！")
            self.base_page.quit()
        except Exception as e:
            self.log.error("关闭页面时异常！\n%s\n" % e)
            raise Exception
        finally:
            # 用例结束，必须
            self.base_page.case_end()
