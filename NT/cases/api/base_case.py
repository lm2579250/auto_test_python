import unittest
from NT.common.log import MyLog
from NT.common.base_page import BasePage
from NT.common.send_request import SendRequest


class APITestCases(unittest.TestCase):
    """api测试用例"""

    def setUp(self):
        try:
            self.request = SendRequest()
            self.base_page = BasePage()
            self.log = MyLog.get_log().logger
        except Exception as e:
            self.log.error(e)
            raise Exception("出现异常！")

    def execute_case(self, origin, case_params, case_name, case_num):
        """api请求实现"""
        try:
            principal = case_params["principal"]  # 从用例中提取负责人姓名
            self.base_page.case_start(principal, case_name, case_num)  # 用例开始头部信息
            msg, code = "", ""  # 期望返回的文本内容和状态码

            self.log.debug("用例参数：%s" % case_params)
            for param_key, param_value in case_params.items():
                if param_key == "msg":
                    if isinstance(param_value, str):
                        msg = param_value
                    else:
                        raise Exception("api用例中msg类型错误！")
                elif param_key == "code":
                    if isinstance(param_value, int):
                        code = int(param_value)
                    else:
                        raise Exception("api用例中code类型错误！")

            response = self.request.send_request(origin, case_params)  # 发送请求

            self.log.debug("是否请求成功：%s" % response.ok)
            self.log.debug("返回状态码：%s" % response.status_code)
            self.log.debug("接口响应时长：%s s" % response.elapsed.total_seconds())
            self.log.debug("编码格式：%s" % response.encoding)
            self.log.debug("请求的url：%s" % response.url)
            self.log.debug("请求头：%s" % response.request.headers)
            self.log.debug("响应头：%s" % response.headers)
            self.log.debug("请求返回json：%s" % response.json())

            # 断言
            tip = response.json()["tip"]  # 返回文本内容
            actual_code = response.json()["ret"]  # 返回状态码
            self.assertEqual(msg, tip, "msg期望值：%s，实际值：%s" % (msg, tip))
            self.assertEqual(code, actual_code, "code期望值：%s，实际值：%s" % (code, actual_code))

            response.raise_for_status()  # 状态码不是200时抛出异常
            self.base_page.case_pass()
        except Exception as e:
            self.log.error(e)
            self.base_page.case_failed()
            raise Exception("出现异常！")
        finally:
            self.base_page.case_end()

    # 定位标记
    def test_case(self):
        """用例描述"""
        case_params = {}
        origin = 'null'
        case_name = 'null'
        case_num = 0

        self.execute_case(origin, case_params, case_name, case_num)
