import os
import json
import threading
import requests
from NT.common.log import MyLog
from NT.data import read_config


class ConfigHTTP:
    """配置http参数并请求"""
    _instance_lock = threading.Lock()  # 设置单例锁

    def __new__(cls, *args, **kwargs):
        """单例模式(支持多线程)"""
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        global host, timeout, headers
        self.log = MyLog.get_log().logger
        self.cf = read_config.ReadConfig()
        self.session = requests.Session()

        # 从配置文件中读取信息
        # 获取域名
        host = self.cf.get_http("url")
        # 获取超时时长
        timeout = self.cf.get_http("timeout")
        # 获取headers，并将str转换为dict
        headers = json.loads(self.cf.get_headers("headers"))

    def send_request(self, case_params):
        """发送请求"""
        method, url, params, files = "", "", "", {}
        try:
            # 解析case_params中的参数
            for param_key, param_value in case_params.items():
                if param_key == "method":
                    method = param_value
                if param_key == "url":
                    url = host + param_value
                if param_key == "params":
                    if param_value is not None and param_value != "None":
                        if os.path.exists(param_value):  # 判断是否是一个文件路径且存在
                            files = {'file': open(param_value, 'rb')}  # 上传文件必须open
                        else:
                            params = json.loads(param_value)  # 将str转换为dict

            self.log.info("预设超时时长：%s s" % timeout)
            response = None
            # 不验证ssl, verify=False
            if method == "get":
                response = self.session.get(url, params=params, headers=headers, timeout=float(timeout),
                                            verify=False)
            elif method == "post":
                response = self.session.post(url, data=params, headers=headers, files=files,
                                             timeout=float(timeout), verify=False)
                # 请求成功后更新token
                self.update_token(response)
            return response
        except requests.exceptions.ConnectionError as e:
            self.log.error("遇到网络问题！（如：DNS 查询失败、拒绝连接等）：%s" % e)
            raise Exception
        except requests.exceptions.HTTPError as e:
            self.log.error("HTTP 请求返回了不成功的状态码：%s" % e)
            raise Exception
        except requests.exceptions.TooManyRedirects as e:
            self.log.error("请求超过了设定的最大重定向次数：%s" % e)
            raise Exception
        except requests.exceptions.Timeout as e:
            self.log.error("请求超时：%s" % e)
            raise Exception
        except requests.exceptions.RequestException as e:
            self.log.error("请求异常：%s" % e)
            raise Exception
        except Exception as e:
            self.log.error("请求异常：%s" % e)
            raise Exception

    def update_token(self, response):
        """更新token"""
        try:
            req = json.loads(response)  # 将str转换为dict

            if "token" in req:
                token = req["token"]
                headers["token"] = token
                self.cf.set_web_headers(json.dumps(headers))  # 将dict转换为str
        except Exception as e:
            self.log.error("更新token时异常：%s" % e)
            raise Exception
