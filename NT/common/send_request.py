import os
import json
import threading
import requests
from NT.common.log import MyLog
from NT.common.read_config import ReadConfig


class SendRequest:
    """配置URL参数并发送请求"""
    _instance_lock = threading.Lock()  # 设置单例锁

    def __new__(cls, *args, **kwargs):
        """单例模式(支持多线程)"""
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        try:
            global timeout, headers
            self.log = MyLog.get_log().logger
            self.config = ReadConfig()
            self.session = requests.session()  # 一个session对象会保持同一个会话中的所有请求之间的cookie信息，此方法只适用于是cookies且没有有效期的，token的没用

            # 从配置文件中读取信息
            # 获取超时时长
            timeout = self.config.get_http("timeout")
            # 获取headers，并将str转换为dict
            headers = json.loads(self.config.get_http("headers"))
            # 获取cookie，并将str转换为dict
            cookie = json.loads(self.config.get_http("cookie"))
            if cookie != {}:
                requests.utils.add_dict_to_cookiejar(self.session.cookies, cookie)  # 添加cookie,保持登录
        except Exception as e:
            self.log.error(e)
            raise Exception("出现异常！")

    def send_request(self, origin, case_params):
        """发送请求"""
        method, url, body, file = "", "", "", {}
        response = None

        try:
            # origin2 = json.dumps(origin)  # 转为str类型
            # self.config.update_http("origin", origin)  # 写入配置文件中
            # # 获取访问地址原点
            # origin1 = self.config.get_http("origin")
            # 解析case_params中的参数
            for param_key, param_value in case_params.items():
                if isinstance(param_value, str):
                    if param_key == "method":
                        method = param_value
                    elif param_key == "url":
                        url = origin + param_value
                    elif param_key == "body":
                        if ":" in param_value and "/" in param_value or "\\" in param_value:
                            if os.path.exists(param_value):  # 判断是否是一个文件路径且存在
                                file = {'file': open(param_value, 'rb')}  # 上传文件必须open
                            else:
                                raise Exception("需要上传文件的路径错误：%s" % param_value)
                        else:
                            try:
                                body = json.loads(param_value)  # 将str转换为dict
                            except Exception as e:
                                self.log.debug(e)
                                body = param_value  # 不能转换时
                        break
                else:
                    raise Exception("api用例中%s类型错误！" % param_key)

            self.log.debug("预设超时时长：%s s" % timeout)

            # 不验证ssl, verify=False
            if method == "get":
                response = self.session.get(url=url, params=body, headers=headers, timeout=float(timeout),
                                            verify=False)
            elif method == "post":
                response = self.session.post(url=url, data=body, headers=headers, files=file,
                                             timeout=float(timeout), verify=False)

            # 请求成功后更新cookie
            self.get_cookie(response)
            return response
        except requests.exceptions.ConnectionError as e:
            self.log.error(e)
            raise Exception("遇到网络问题(如：DNS 查询失败、拒绝连接等)！")
        except requests.exceptions.HTTPError as e:
            self.log.error(e)
            raise Exception("HTTP 请求返回了不成功的状态码！")
        except requests.exceptions.TooManyRedirects as e:
            self.log.error(e)
            raise Exception("请求超过了设定的最大重定向次数！")
        except requests.exceptions.Timeout as e:
            self.log.error(e)
            raise Exception("请求超时！")
        except requests.exceptions.RequestException as e:
            self.log.error(e)
            raise Exception("请求异常！")
        except Exception as e:
            self.log.error(e)
            raise Exception("请求异常！")

    def get_cookie(self, response):
        """保存cookie"""
        try:
            cookie = response.cookies.get_dict()
            if cookie != {}:
                str_cookie = json.dumps(cookie)  # 转为str类型
                self.config.update_http("cookie", str_cookie)  # 写入配置文件中
        except Exception as e:
            self.log.error(e)
            raise Exception("保存cookie时异常！")
