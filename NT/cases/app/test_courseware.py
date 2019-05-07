import unittest
from NT.common.log import MyLog
from NT.common.base_page import BasePage


class AppCourseware(unittest.TestCase):
    """课件"""

    def setUp(self):
        try:
            self.base_page = BasePage()
            self.log = MyLog().get_log().logger
        except Exception as e:
            self.log.error(e)
            raise Exception("出现异常！")

    def test_app_courseware(self):
        """app课件"""
        top_menu = ("xpath", "//div[@class='nw-tab']/div")  # 课件类型menu
        search_menu = ("css_selector", "button.button.button-calm.exam-button")  # 搜索按钮
        search_input = ("css_selector", "input[type='text']")  # 搜索内容
        search_button = ("css_selector", "button.button.button-small.button-clear.button-dark.search-button.font-small")  # 搜索按钮
        global text
        text = ""
        try:
            # 用例开始，输入负责人姓名，必须
            self.base_page.case_start("李彬")

            if not self.base_page.home_page_to("课件"):  # 判断待办事项中是否有课件
                if AppCourseware.enter(self) is False:  # 首页进入课件
                    # 如果没有课件就结束用例
                    self.base_page.case_pass()
                    return

            # 开始学习
            self.log.debug("进入全部：")
            AppCourseware.study(self)
            type_count = len(self.base_page.find_elements(top_menu))  # 课件类型数量
            i = 1
            while i < type_count:
                self.base_page.get_text(top_menu, tag=i, text="进入：")
                self.base_page.click_elem_tag(top_menu, tag=i)
                AppCourseware.study(self, tag=i)
                i += 1

            self.log.debug("进入搜索：")
            self.base_page.click_elem_tag(search_menu)
            self.base_page.input_tag(search_input, text)
            self.base_page.screen_shot()

            self.base_page.switch_handle(search_button)
            self.base_page.click_elem_tag(search_button)
            self.base_page.screen_shot()

            self.base_page.switch_handle(search_button)
            AppCourseware.study(self)

            # 用例成功，必须
            self.base_page.case_pass()
        except Exception as e:
            self.log.error(e)
            # 用例失败，必须
            self.base_page.case_failed()
            raise Exception("出现异常！")
        finally:
            self.base_page.back_to()

    def enter(self):
        """进入课件"""
        module = ("css_selector", "img[src='img/courseware.png']")  # 首页“课件”menu
        title = ("css_selector", "div.title.ng-binding")  # “课件”title
        all_list = ("css_selector", "ion-item.item-remove-animate.item-text-wrap.item.item-complex")  # “课件”list

        try:
            self.assertIs(self.base_page.displayed(module), True, "首页异常！")
            self.log.debug("从首页进入课件模块")
            self.base_page.click_elem_tag(module)
            self.base_page.screen_shot()

            self.base_page.switch_handle(title)
            self.assertIs(self.base_page.displayed(title), True, "进入课件模块异常！")
            if self.base_page.displayed(all_list):
                return True
            else:
                self.log.debug("暂无内容！")
                return False
        except Exception as e:
            self.log.error(e)
            raise Exception("出现异常！")

    def study(self, tag=0):
        """学习课件"""
        top_menu = ("xpath", "//div[@class='nw-tab']/div")  # 课件类型menu
        courseware_list = ("css_selector", "ion-item.item-remove-animate.item-complex.item-text-wrap.item")  # 课件list
        courseware_name = ("css_selector", "h2.exam-title.font-large.text-center.ng-binding")  # 课件名称
        start_answer_button = ("xpath", "//a[contains(text(), '开始学习')]")

        try:
            courseware_count = len(self.base_page.find_elements(courseware_list))
            if courseware_count != 0:
                self.base_page.click_elem_tag(courseware_list)
                self.assertIs(self.base_page.displayed(courseware_name), True, "进入课件列表异常！")
                name = self.base_page.get_text(courseware_name, text="进入课件：")
                self.base_page.screen_shot()
                global text
                text = name

                self.base_page.switch_handle(start_answer_button)
                self.assertIs(self.base_page.displayed(start_answer_button), True, "进入课件主页异常！")
                self.log.debug("点击开始学习按钮")
                self.base_page.click_elem_tag(start_answer_button, t=2)
                self.base_page.screen_shot()

                self.base_page.back_to(top_menu)
                self.base_page.click_elem_tag(top_menu, tag=tag)
                self.log.debug("学习完成！")
            else:
                self.log.debug("暂无内容！")
        except Exception as e:
            self.log.error(e)
            raise Exception("出现异常！")

    def tearDown(self):
        self.base_page.case_end()
