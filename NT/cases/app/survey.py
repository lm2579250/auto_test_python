import random
import unittest
from NT.common.log import MyLog
from NT.common.base_page import BasePage


class AppSurvey(unittest.TestCase):
    """问卷调查"""

    def setUp(self):
        try:
            self.base_page = BasePage()
            self.log = MyLog().get_log().logger
        except Exception as e:
            self.log.error(e)
            raise Exception

    def test_app_survey(self):
        """app问卷调查"""
        try:
            # 用例开始，输入负责人姓名，必须
            self.base_page.case_start("李彬")

            if AppSurvey.enter(self) is False:  # 首页进入考试
                # 如果没有可以考试的试卷就结束用例
                self.base_page.case_pass()
                return

            # 开始答题
            AppSurvey.answer(self)

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
        """进入问卷调查"""
        survey_module = ("css_selector", "img[src='img/survey.png']")  # 首页“问卷调查”menu
        survey_title = ("css_selector", "div.title.ng-binding")  # “问卷调查”title
        survey_list = ("css_selector", "ion-item.item-remove-animate.item-text-wrap.item.item-complex")  # “问卷调查”问卷
        survey_state = ("css_selector", "span.tag.ng-binding.tag-warning.tag-right")  # “未填写”标签

        try:
            self.assertIs(self.base_page.displayed(survey_module), True, "首页异常！")
            self.log.debug("从首页进入问卷调查模块")
            self.base_page.click_elem_tag(survey_module)
            self.base_page.screen_shot()
            self.assertIs(self.base_page.displayed(survey_title), True, "进入问卷调查模块异常！")
            if self.base_page.displayed(survey_list):
                if self.base_page.displayed(survey_state):
                    self.log.debug("进入问卷")
                    self.base_page.click_elem_tag(survey_state)
                    return True
                else:
                    self.log.debug("暂无未填写的问卷！")
                    return False
            else:
                self.log.debug("暂无内容！")
                return False
        except Exception as e:
            self.log.error(e)
            raise Exception

    def answer(self):
        """答题"""
        survey_name = ("css_selector", "h2.exam-title.font-large.text-center.ng-binding")  # 问卷名称
        start_answer_button = ("css_selector", "a.button.button-block.button-calm")  # “开始填写”按钮
        problem_name = ("css_selector", "div.paper-title.font-big.ng-binding")  # 问题名称
        submit_button = ("css_selector", "button.button.button-full.button-calm.lesson-footer-button")  # 提交按钮
        text = u"大幅度dddz12345，，kds。，.,m@!~" * 5

        try:
            self.base_page.screen_shot()
            self.assertIs(self.base_page.displayed(survey_name), True, "进入问卷异常！")
            self.base_page.get_text(survey_name, text="问卷名称：")

            if self.base_page.displayed(start_answer_button):
                self.log.debug("点击[开始填写]按钮")
                self.base_page.click_elem_tag(start_answer_button)
                self.base_page.screen_shot()

            # 用答题页面的“提交”按钮断言
            self.assertIs(self.base_page.displayed(submit_button), True, "进入答题页异常！")
            # 问题数量
            problem_count = len(self.base_page.find_elements(problem_name))
            self.log.debug("问题数量：%s" % problem_count)

            i = 1
            while i <= problem_count:
                problem_type_elem = ("xpath", "//div[@class='survey-content'][%s]//span[2]" % i)  # 问题类型
                problem_type = self.base_page.get_text(problem_type_elem, text="第%s题：" % i)

                if "单选题" in problem_type or "评分题" in problem_type:
                    radio = ("xpath", "//div[@class='survey-content'][%s]//label" % i)  # 单选题和评分题选项
                    radio_count = len(self.base_page.find_elements(radio))
                    a = random.randint(0, radio_count - 1)
                    self.base_page.click_elem_tag(radio, tag=a)
                elif "多选题" in problem_type:
                    multiple = ("xpath", "//div[@class='survey-content'][%s]//div[@ng-repeat='option in question.questionOptionList']" % i)  # 多选题选项
                    multiple_count = len(self.base_page.find_elements(multiple))
                    b = random.randint(0, multiple_count - 1)
                    self.base_page.click_elem_tag(multiple, tag=b)
                    c = b
                    while c == b:
                        c = random.randint(0, multiple_count - 1)
                    self.base_page.click_elem_tag(multiple, tag=c)
                elif "简答题" in problem_type:
                    textarea = ("xpath", "//div[@class='survey-content'][%s]//textarea[@class='no-resize ng-pristine ng-untouched ng-invalid ng-invalid-required']" % i)  # 问答题输入框
                    self.base_page.input_tag(textarea, text=text)
                i += 1
                self.base_page.screen_shot()

            self.base_page.click_elem_tag(submit_button)
            self.base_page.screen_shot()
            self.base_page.popup()
        except Exception as e:
                self.log.error(e)
                raise Exception

    def tearDown(self):
        self.base_page.case_end()
