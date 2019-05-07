import random
import unittest
from NT.common.log import MyLog
from NT.common.common import Common
from NT.common.base_page import BasePage


class AppExams(unittest.TestCase):
    """考试"""

    def setUp(self):
        try:
            self.common = Common()
            self.base_page = BasePage()
            self.log = MyLog().get_log().logger
        except Exception as e:
            self.log.error(e)
            raise Exception("出现异常！")

    def test_app_exams(self):
        """app考试"""
        try:
            # 用例开始，输入负责人姓名，必须
            self.base_page.case_start("李彬")
            if not self.base_page.home_page_to("考试"):  # 判断待办事项中是否有考试
                if AppExams.enter(self) is False:  # 首页进入考试
                    # 如果没有可以考试的试卷就结束用例
                    self.base_page.case_pass()
                    return

            # 开始答题
            AppExams.answer(self)

            # 用例成功，必须
            self.base_page.case_pass()
        except Exception as e:
            self.log.error(e)
            # 用例失败，必须
            self.base_page.case_failed()
            raise Exception("出现异常！")
        finally:
            self.base_page.back_to()

    def answer(self):
        """答题"""
        exam_name = ("css_selector", "h2.exam-title.font-large.text-center.ng-binding")  # 试卷名称
        start_answer_button = ("xpath", "//a[contains(text(), '开始答题')]")
        re_answer_button = ("xpath", "//a[contains(text(), '重新答题')]")
        exam_time_elem = ("css_selector", "span.countdown.ng-binding")  # 考试时长
        count_num_elem = ("css_selector", "span.item-num.ng-binding")  # 题号和试题数量
        option_elem = ("css_selector", "li.option-list-li")  # 选项
        next_elem = ("css_selector", "div.col.col-33.col-center.text-right")  # 下一题
        submit_elem = ("css_selector", "a.button.button-clear.button-calm")  # 提交
        result_element = ("css_selector", "div.title.ng-binding")  # 成绩单title
        answer_sheet_elem = ("css_selector", "button.button.button-calm.exam-button")  # 答题页面的右上角的“答题卡”
        submit_button = ("css_selector", "button.button.button-block.button-calm")  # 提交按钮
        # 登录成功提示，有未答题提示，自动提交试卷提示
        popup_title = ("css_selector", "h3.popup-title.ng-binding")  # 提示框title

        try:
            self.base_page.screen_shot()
            self.assertIs(self.base_page.displayed(exam_name), True, "进入试卷异常！")
            self.base_page.get_text(exam_name, text="试卷名称：")

            if self.base_page.displayed(start_answer_button):
                self.log.debug("点击开始答题按钮")
                self.base_page.click_elem_tag(start_answer_button)
            elif self.base_page.displayed(re_answer_button):
                self.log.debug("点击重新答题按钮")
                self.base_page.click_elem_tag(re_answer_button)

            # 提示框
            self.base_page.popup()
            # 用答题页面的“答题卡”元素断言
            self.assertIs(self.base_page.displayed(answer_sheet_elem), True, "进入答题页异常！")
            # 获取考试时常
            self.base_page.get_text(exam_time_elem, text="剩余考试时长：")
            # 获取题目总数
            num = self.base_page.get_text(count_num_elem)
            count_num_str = num.split('/')[1:][0]  # 考题总数
            current_num_str = num.split('/')[:1][0]  # 当前题号

            self.log.debug("开始答题")
            count_num = int(count_num_str)
            current_num = int(current_num_str)
            # 自动提交试卷的提示框和总题数
            try:
                while not self.base_page.displayed(popup_title) and current_num <= count_num:
                    self.log.debug("第%s题" % current_num)
                    count_option = len(self.base_page.find_elements(option_elem))  # 选项数量
                    i = random.randint(0, count_option - 1)
                    self.base_page.click_elem_tag(option_elem, tag=i)
                    self.base_page.screen_shot()
                    # 点击下一题按钮
                    if current_num < count_num:
                        self.base_page.click_elem_tag(next_elem)
                        current_num += 1

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
                    else:
                        self.log.debug("置于后台")
                        self.base_page.app_driver.background_app(0)

                # 手动提交试卷
                if current_num == count_num and not self.base_page.displayed(popup_title):
                    self.log.debug("答题完毕后点击'提交'按钮，手动提交试卷！")
                    self.base_page.click_elem_tag(submit_elem, tag=1)
                    self.base_page.screen_shot()
                    self.assertIs(self.base_page.displayed(submit_button), True, "答题完毕后提交失败，未进入答题卡页面！")

                    # 答题卡页面点击提交按钮
                    self.base_page.click_elem_tag(submit_button, roll=True)
                    # 答题卡页点击提交按钮后的提示框
                    self.assertIs(self.base_page.displayed(popup_title), True, "答题卡页面点击提交按钮后未出现提示框！")
                    # 提示框
                    self.base_page.popup()
                # 自动提交试卷(时间到了/超过离开次数)
                elif self.base_page.displayed(popup_title):
                    self.base_page.popup()
                # 用成绩单页面的“成绩单”元素断言
                self.assertIs(self.base_page.displayed(result_element), True, "考试结果提交异常！")
                self.log.debug("提交成功！")
            except Exception as e:
                # 过程中出现弹框(自动提交弹框)
                if self.base_page.displayed(popup_title):
                    self.base_page.popup()
                    # 用成绩单页面的“成绩单”元素断言
                    self.assertIs(self.base_page.displayed(result_element), True, "考试结果提交异常！")
                    self.log.debug("提交成功！")
                else:
                    self.log.error(e)
                    raise Exception("出现异常！")
        except Exception as e:
            self.log.error(e)
            raise Exception("出现异常！")

    def enter(self):
        """进入试卷"""
        try:
            exams_module = ("css_selector", "img[src='img/exam.png']")  # 首页“考试”menu
            exam_state = ("css_selector", "span.tag.ng-binding.tag-warning.tag-right")  # “未考试”标签
            prompt_nothing = ("css_selector", "div.nw-nothing-text")  # “暂无内容”提示
            exams_type = ("css_selector", "div.exam-tabs.text-center.font-small.ng-binding")  # “未考试/已交卷”menu

            self.assertIs(self.base_page.displayed(exams_module), True, "首页异常！")
            self.log.debug("从首页进入考试模块")
            self.base_page.click_elem_tag(exams_module)
            self.base_page.screen_shot()
            self.assertIs(self.base_page.displayed(exams_type), True, "进入考试模块异常！")
            if self.base_page.displayed(exam_state):
                self.log.debug("进入试卷")
                self.base_page.click_elem_tag(exam_state)
                return True
            else:
                if self.base_page.displayed(prompt_nothing):
                    self.log.debug("未考试中暂无内容！")
                else:
                    self.log.debug("暂无未考试的试卷！")
                self.log.debug("进入已交卷中查看")
                self.base_page.click_elem_tag(exams_type, tag=1)
                self.base_page.screen_shot()
                if self.base_page.displayed(prompt_nothing):
                    self.log.debug("已交卷中暂无内容！")
                    return False
                else:
                    return AppExams.find_the_paper(self)
        except Exception as e:
            self.log.error(e)
            raise Exception("出现异常！")

    def find_the_paper(self):
        """已交卷中查找可以重新答题的试卷"""
        exams_type = ("css_selector", "div.exam-tabs.text-center.font-small.ng-binding")  # 已交卷menu
        exam_state = ("css_selector", "span.tag.ng-binding.tag-success.tag-right")  # "已考试"标签
        exam_name = ("css_selector", "h2.exam-title.font-large.text-center.ng-binding")  # 试卷名称
        re_answer_button = ("xpath", "//a[contains(text(), '重新答题')]")  # 重新答题按钮

        try:
            count = len(self.base_page.find_elements(exam_state))  # "已考试"标签总数
            # self.log.debug("[已考试]标签数量：%s" % str(count))

            i = 0
            j = 1
            n = 0
            if count != 0:
                while j <= count:
                    self.base_page.click_elem_tag(exams_type, tag=1)
                    self.log.debug("进入试卷")
                    self.base_page.click_elem_tag(exam_state, tag=i, roll=True)

                    if self.base_page.displayed(re_answer_button):
                        n += 1
                        self.log.debug("该试卷可以重新答题")
                        return True

                    self.base_page.get_text("试卷名称：", exam_name)
                    self.base_page.screen_shot()
                    self.log.debug("该试卷不能重新答题，继续查看下一个试卷")
                    self.base_page.back()
                    i += 2
                    j += 1
                    if j % 10 == 0:
                        self.log.debug("向上滑动屏幕！")
                        self.base_page.swipe_up()
                        self.base_page.screen_shot()
                        elements = self.base_page.find_elements(exam_state)
                        count = len(elements)
            if n == 0:
                self.log.debug("已交卷中没有可以重新答题的试卷！")
                return False
        except Exception as e:
            self.log.error(e)
            raise Exception("出现异常！")

    def tearDown(self):
        # 用例结束，必须
        self.base_page.case_end()
