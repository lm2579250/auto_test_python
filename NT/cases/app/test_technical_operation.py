import time
import random
import unittest
from NT.common.log import MyLog
from NT.common.base_page import BasePage


class AppTechnicalOperation(unittest.TestCase):
    """技术操作"""
    def setUp(self):
        try:
            self.base_page = BasePage()
            self.log = MyLog().get_log().logger
        except Exception as e:
            self.log.error(e)
            raise Exception

    def test_app_operation(self):
        """app技术操作"""
        bottom_menu = ("css_selector", "span.tab-title.ng-binding")  # 底部menu
        operation_tool_menu = ("css_selector", "i.iconfont.nw-tool.mine-icon")  # 操作工具
        operation_exam_menu = ("css_selector", "a.item.item-icon-right")  # 技术操作考核
        prompt_nothing = ("css_selector", "div.nw-nothing-text")  # “暂无内容”提示
        operation_list = ("css_selector", "ion-item.item-remove-animate.item-text-wrap.item")  # 试卷list
        operation_name = ("css_selector", "h1.operate-title.text-center.font-large.ng-binding")  # 试卷名称
        scan_button = ("css_selector", "button.button.button-block.button-calm")  # 扫码考核按钮
        popup_title = ("css_selector", "h3.popup-title.ng-binding")  # 提示框title

        deduction_button = ("xpath", "//android.view.View[@content-desc='扣分']")  # 扣分按钮
        remark = ("class", "android.widget.EditText")  # 扣分备注
        deduction_value = ("xpath", "//android.view.View[@content-desc='0.5分']")  # 扣分值
        determine_button = ("xpath", "//android.view.View[@content-desc='确认']")  # 确认扣分
        remark_value = u"agaa vjvvabaz v测试,./!，。？！1234567890" * 10
        submit_button = ("css_selector", "button.button.button-calm.exam-button")  # 判分零和提交按钮

        try:
            # 用例开始，输入负责人姓名，必须
            self.base_page.case_start("李彬")
            self.assertIs(self.base_page.displayed(bottom_menu), True, "首页异常！")
            self.log.debug("进入[我的]")
            self.base_page.click_elem_tag(bottom_menu, tag=-1)
            self.base_page.screen_shot()

            if self.base_page.displayed(operation_tool_menu):
                self.log.debug("进入[操作工具]")
                self.base_page.click_elem_tag(operation_tool_menu)
                self.base_page.screen_shot()
                if self.base_page.displayed(prompt_nothing):
                    self.log.debug("暂无内容！")
                    self.base_page.case_pass()
                    return
            else:
                self.log.debug("没有[操作工具]选项，结束测试！")
                self.base_page.case_pass()
                return
            self.log.debug("进入[技术操作列表]")
            if self.base_page.displayed(prompt_nothing):
                self.log.debug("暂无内容！")
                self.base_page.case_pass()
                return
            self.base_page.click_elem_tag(operation_exam_menu)
            self.base_page.screen_shot()
            self.assertIs(self.base_page.displayed(operation_list), True, "进入[技术操作列表]异常！")

            self.log.debug("进入[技术操作详情]")
            operation_count = len(self.base_page.find_elements(operation_list))  # 技术操作试卷数量
            i = random.randint(0, operation_count - 1)
            self.base_page.click_elem_tag(operation_list, tag=i, roll=True)
            self.base_page.screen_shot()
            self.assertIs(self.base_page.displayed(scan_button), True, "进入[技术操作详情]异常！")
            self.base_page.get_text(operation_name, text="考核表名称：")
            self.log.debug("请扫描考生的二维码！")
            self.base_page.click_elem_tag(scan_button)

            i = 0
            while self.base_page.displayed(scan_button):
                self.log.debug("等待扫码！")
                time.sleep(2)
                # 开始考核/重新考核/非本院学员/扫码失败
                if self.base_page.displayed(popup_title):
                    self.base_page.popup()
                    break

                i += 1
                if i == 30:
                    raise Exception("扫码超时！")
            self.assertIs(self.base_page.displayed(submit_button), True, "进入答题页面异常！")
            self.log.debug("扫码完成,进入答题页面！")

            self.base_page.switch_context(tag=0)
            elements = len(self.base_page.find_elements(deduction_button))
            self.log.debug("总题数：%s" % str(elements))
            if elements != 0:
                i = 0
                while i < elements:
                    self.log.debug("点击第%s题的扣分按钮" % (i+1))
                    self.base_page.click_elem_tag(deduction_button, tag=i, roll=True)
                    self.base_page.screen_shot()

                    self.log.debug("选择扣分")
                    self.assertIs(self.base_page.displayed(deduction_value), True, "点击扣分按钮时异常！")
                    tag_id = len(self.base_page.find_elements(deduction_value))
                    self.base_page.click_elem_tag(deduction_value, tag=(tag_id - 1))
                    self.base_page.get_text(deduction_value, text="第%s题扣除：" % (i+1), tag=(tag_id-1))
                    self.base_page.screen_shot()

                    self.base_page.click_elem_tag(determine_button)  # 确认扣分
                    self.base_page.screen_shot()

                    if self.base_page.displayed(remark, tag=i):
                        self.log.debug("输入第%s题的扣分备注" % (i+1))
                        self.base_page.input_tag(remark, remark_value, tag=i, roll=True)
                    self.base_page.screen_shot()
                    i += 1

                    if i >= 5:
                        self.log.debug("中断答题")
                        self.base_page.screen_shot()
                        break

                self.base_page.switch_context()

                self.log.debug("点击[提交]按钮，提交本次考核成绩！")
                self.base_page.click_elem_tag(submit_button, tag=1)

                self.assertIs(self.base_page.displayed(popup_title), True, "点击[提交]按钮后未出现确定提交的提示框！")
                self.base_page.popup()

                self.assertIs(self.base_page.displayed(popup_title), True, "点击[确定]按钮后未出现提交成功的提示框！")
                self.base_page.popup()

                self.assertIs(self.base_page.displayed(scan_button), True, "提交考试结果后未回到技术操作详情页面！")
                self.log.debug("本次考核成绩已提交！")

                # 用例成功，必须
                self.base_page.case_pass()
            else:
                self.base_page.screen_shot()
                raise Exception("页面显示异常！")
        except Exception as e:
            self.log.error(e)
            # 用例失败，必须
            self.base_page.case_failed()
            raise Exception
        finally:
            self.base_page.back_to()

    def tearDown(self):
        self.base_page.case_end()
