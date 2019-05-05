import random
import unittest
from NT.common.log import MyLog
from NT.common.base_page import BasePage


class AppCurriculum(unittest.TestCase):
    """课程"""

    def setUp(self):
        try:
            self.base_page = BasePage()
            self.log = MyLog().get_log().logger
        except Exception as e:
            self.log.error(e)
            raise Exception

    def test_app_curriculum(self):
        """app课程"""
        try:
            # 用例开始，输入负责人姓名，必须
            self.base_page.case_start("李彬")

            if not self.base_page.home_page_to("课程"):  # 判断待办事项中是否有课程
                if AppCurriculum.enter(self) is False:  # 首页进入课程
                    # 如果没有课程就结束用例
                    self.base_page.case_pass()
                    return

            # 开始学习
            AppCurriculum.study(self)

            # 用例成功，必须
            self.base_page.case_pass()
        except Exception as e:
            self.log.error(e)
            # 用例失败，必须
            self.base_page.case_failed()
            raise Exception
        finally:
            self.base_page.back_to()

    def enter(self):
        """进入课程"""
        module = ("css_selector", "img[src='img/lesson.png']")  # 首页“课程”menu
        title = ("css_selector", "div.title.ng-binding")  # “课程”title
        curriculum_list = ("css_selector", "ion-item.item-remove-animate.item-text-wrap.item.item-complex")  # “课程”list
        state = ("css_selector", "span.tag.ng-binding.tag-orange.tag-right")  # “未学习”标签

        try:
            self.assertIs(self.base_page.displayed(module), True, "首页异常！")
            self.log.debug("从首页进入课程模块")
            self.base_page.click_elem_tag(module)
            self.base_page.screen_shot()
            self.assertIs(self.base_page.displayed(title), True, "进入课程模块异常！")

            if self.base_page.displayed(curriculum_list):
                if self.base_page.displayed(state):
                    self.log.debug("进入课程")
                    self.base_page.click_elem_tag(state, roll=True)
                else:
                    self.log.debug("暂无未学习的课程，进入已学习的课程中重新学习！")
                    count = len(self.base_page.find_elements(curriculum_list))  # 课程数量
                    i = random.randint(0, count - 1)
                    self.base_page.click_elem_tag(curriculum_list, tag=i, roll=True)
                return True
            else:
                self.log.debug("暂无内容！")
                return False
        except Exception as e:
            self.log.error(e)
            raise Exception

    def study(self):
        """学习"""
        curriculum_name = ("css_selector", "h1.exam-title.font-large.text-center.ng-binding")  # 课程名称
        curriculum_exam = ("css_selector", "button.button.button-full.button-calm.lesson-footer-button")  # 随堂考试
        curriculum_list = ("css_selector", "ion-item.item-remove-animate.item-complex.item-text-wrap.item")  # 课件list
        # state = ("css_selector", "span.tag.ng-binding.tag-orange.tag-right")  # “未学习”标签
        courseware_name = ("css_selector", "h2.exam-title.font-large.text-center.ng-binding")  # 课件名称
        start_answer_button = ("xpath", "//a[contains(text(), '开始学习')]")

        try:
            self.base_page.screen_shot()
            self.assertIs(self.base_page.displayed(curriculum_name), True, "进入课程异常！")
            self.base_page.get_text(curriculum_name, text="课程名称：")

            # 随堂考试（只能放课件学习的前面，不然会有句柄切换问题）
            if self.base_page.displayed(curriculum_exam):
                AppCurriculum.answer(self)
                self.base_page.back_to(curriculum_name)

            curriculum_count = len(self.base_page.find_elements(curriculum_list))
            if curriculum_count != 0:
                self.base_page.switch_handle(curriculum_list)
                i = random.randint(0, curriculum_count - 1)
                self.base_page.click_elem_tag(curriculum_list, tag=i, roll=True)
                self.assertIs(self.base_page.displayed(courseware_name), True, "进入课件异常！")
                self.base_page.get_text(courseware_name, text="进入课件：")
                self.base_page.screen_shot()

                if self.base_page.displayed(start_answer_button):
                    self.log.debug("点击开始学习按钮")
                    self.base_page.click_elem_tag(start_answer_button, t=2)
                    self.base_page.screen_shot()

                self.base_page.back_to(curriculum_name)
                self.log.debug("学习完成！")
            else:
                self.log.debug("暂无内容！")
        except Exception as e:
                self.log.error(e)
                raise Exception

    def answer(self):
        """随堂考试"""
        curriculum_exam = ("css_selector", "button.button.button-full.button-calm.lesson-footer-button")  # 随堂考试
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
            self.log.debug("进入随堂考试")
            self.base_page.click_elem_tag(curriculum_exam)
            self.base_page.screen_shot()

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
            self.log.debug("提交成功！")
        except Exception as e:
            self.log.error(e)
            raise Exception

    def tearDown(self):
        self.base_page.case_end()
