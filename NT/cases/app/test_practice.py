import random
import unittest
from NT.common.log import MyLog
from NT.common.base_page import BasePage


class AppPractice(unittest.TestCase):
    """练习"""

    def setUp(self):
        try:
            self.base_page = BasePage()
            self.log = MyLog().get_log().logger
        except Exception as e:
            self.log.error(e)
            raise Exception("出现异常！")

    def test_app_practice(self):
        """app练习"""
        try:
            # 用例开始，输入负责人姓名，必须
            self.base_page.case_start("李彬")

            if not self.base_page.home_page_to("练习"):  # 判断待办事项中是否有练习
                if AppPractice.enter(self) is False:  # 首页进入考试
                    # 如果没有练习试卷就结束用例
                    self.base_page.case_pass()
                    return

            # 开始答题
            AppPractice.answer(self)

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
        """进入练习"""
        practice_module = ("css_selector", "img[src='img/practice-icon.png']")  # 首页“练习”menu
        practice_title = ("css_selector", "div.title.ng-binding")  # “练习”title
        practice_list = ("css_selector", "ion-item.item-remove-animate.item-text-wrap.item.item-complex")  # “练习”试卷
        practice_state = ("css_selector", "span.tag.ng-binding.tag-orange.tag-right")  # “未练习”标签

        try:
            self.assertIs(self.base_page.displayed(practice_module), True, "首页异常！")
            self.log.debug("从首页进入练习模块")
            self.base_page.click_elem_tag(practice_module)
            self.base_page.screen_shot()
            self.assertIs(self.base_page.displayed(practice_title), True, "进入练习模块异常！")
            if self.base_page.displayed(practice_list):
                if self.base_page.displayed(practice_state):
                    self.log.debug("进入练习试卷")
                    self.base_page.click_elem_tag(practice_state)
                else:
                    self.log.debug("暂无未练习的试卷，进入已完成试卷中重新练习！")
                    practice_count = len(self.base_page.find_elements(practice_list))
                    i = random.randint(0, practice_count - 1)
                    self.base_page.click_elem_tag(practice_list, tag=i, roll=True)
                return True
            else:
                self.log.debug("暂无内容！")
                return False
        except Exception as e:
            self.log.error(e)
            raise Exception("出现异常！")

    def answer(self):
        """答题"""
        title = ("css_selector", "div.title.ng-binding")  # “练习”title
        exam_name = ("css_selector", "h2.exam-title.font-large.text-center.ng-binding")  # 试卷名称
        start_answer_button = ("xpath", "//a[contains(text(), '开始练习')]")
        continue_answer_button = ("xpath", "//a[contains(text(), '继续练习')]")
        re_answer_button = ("xpath", "//a[contains(text(), '重新练习')]")
        count_num_elem = ("css_selector", "span.item-num.ng-binding")  # 题号和试题数量
        option_elem = ("css_selector", "li.option-list-li")  # 选项
        next_elem = ("css_selector", "div.col.col-33.col-center.text-right")  # 下一题
        submit_elem = ("css_selector", "a.button.button-clear.button-calm")  # 提交
        result_element = ("css_selector", "div.title.ng-binding")  # 练习结果title
        answer_sheet_elem = ("css_selector", "button.button.button-calm.exam-button")  # 答题页面的右上角的“答题卡”
        submit_button = ("css_selector", "button.button.button-block.button-calm")  # 提交按钮
        # 登录成功提示，有未答题提示，自动提交试卷提示
        popup_title = ("css_selector", "h3.popup-title.ng-binding")  # 提示框title

        try:
            self.base_page.screen_shot()
            self.assertIs(self.base_page.displayed(title), True, "进入试卷异常！")
            self.base_page.get_text(exam_name, text="试卷名称：")

            if self.base_page.displayed(re_answer_button):
                self.log.debug("点击[重新练习]按钮")
                self.base_page.click_elem_tag(re_answer_button)
            elif self.base_page.displayed(start_answer_button):
                self.log.debug("点击[开始练习]按钮")
                self.base_page.click_elem_tag(start_answer_button)
            elif self.base_page.displayed(continue_answer_button):
                self.log.debug("点击[继续练习]按钮")
                self.base_page.click_elem_tag(continue_answer_button)
            # 用答题页面的“答题卡”元素断言
            self.assertIs(self.base_page.displayed(answer_sheet_elem), True, "进入答题页异常！")
            # 获取题目总数
            num = self.base_page.get_text(count_num_elem)
            count_num_str = num.split('/')[1:][0]  # 考题总数
            current_num_str = num.split('/')[:1][0]  # 当前题号

            self.log.debug("开始答题")
            count_num = int(count_num_str)
            current_num = int(current_num_str)

            while current_num <= count_num:
                self.log.debug("第%s题" % current_num)
                count_option = len(self.base_page.find_elements(option_elem))  # 选项数量
                i = random.randint(0, count_option - 1)
                self.base_page.click_elem_tag(option_elem, tag=i)
                self.base_page.screen_shot()
                # 点击下一题按钮
                if current_num < count_num:
                    self.base_page.click_elem_tag(next_elem)
                    current_num += 1
                else:
                    break

                if current_num >= 6:
                    self.log.debug("中断答题")
                    self.base_page.screen_shot()
                    self.base_page.click_elem_tag(answer_sheet_elem)
                    self.base_page.screen_shot()

                    if not self.base_page.displayed(popup_title):
                        self.log.debug("进入答题卡页面提交试卷！")
                        # 点击提交按钮
                        self.base_page.click_elem_tag(submit_button, roll=True)
                        self.base_page.screen_shot()
                        break
                    else:
                        break

            # 手动提交试卷
            if current_num == count_num and not self.base_page.displayed(popup_title):
                self.log.debug("答题完毕后点击'提交'按钮，手动提交试卷！")
                self.base_page.click_elem_tag(submit_elem, tag=1)
                self.base_page.screen_shot()
            # 自动提交试卷(中断答题/超过离开次数)
            elif self.base_page.displayed(popup_title):
                self.base_page.popup()
            # 用成绩单页面的“成绩单”元素断言
            self.assertIs(self.base_page.displayed(result_element), True, "考试结果提交异常！")
            self.log.debug("练习完成！")
        except Exception as e:
            self.log.error(e)
            raise Exception("出现异常！")

    def tearDown(self):
        self.base_page.case_end()
