import os
import codecs
import threading
import configparser
from NT.common.common import Common


class ReadConfig(object):
    """读取config配置文件中的内容"""

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
            # 拼接配置文件路径
            self.config_path = Common.get_path("data", "config.ini")

            # 判断文件是否存在
            if not os.path.isfile(self.config_path):
                raise Exception("文件%s不存在！" % self.config_path)

            # 读取文件
            with open(self.config_path, "r", encoding="utf-8") as file:
                data = file.read()

            # 去掉 BOM头后重新写入
            if data[:3] == codecs.BOM_UTF8:
                data = data[3:]
                with open(self.config_path, "w", encoding="utf-8") as file:
                    file.write(data)

            # 读取文件
            self.cf = configparser.ConfigParser()
            self.cf.read(self.config_path, encoding="utf-8")
        except Exception as e:
            raise Exception("ReadConfig.__init__异常 %s" % e)

    def set_web_headers(self, value):
        """"更新配置文件中的headers"""
        self.cf.set("web_headers", "headers", value)
        self.cf.write(open(self.config_path, "w", encoding="utf-8"))

    def get_web_param(self, value):
        """web参数"""
        value = self.cf.get("web_param", value)
        return value

    def get_app_param(self, value):
        """app参数"""
        value = self.cf.get("app_param", value)
        return value

    def get_http(self, name):
        """项目域名，端口，超时时长"""
        value = self.cf.get("http", name)
        return value

    def get_headers(self, name):
        """headers信息"""
        value = self.cf.get("web_headers", name)
        return value

    def get_email(self, name):
        """邮箱配置"""
        value = self.cf.get("email", name)
        return value

    def get_db(self, name):
        """数据库配置"""
        value = self.cf.get("database", name)
        return value
