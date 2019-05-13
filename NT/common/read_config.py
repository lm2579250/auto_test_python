import os
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
            self.config_path = Common.get_path("data", "config.ini")  # 拼接配置文件路径
            self.cf = configparser.ConfigParser()  # 读取配置文件的对象

            # 判断文件是否存在
            if not os.path.isfile(self.config_path):
                raise Exception("文件%s不存在！" % self.config_path)

            # 判断是否有BOM头
            bom = b'\xef\xbb\xbf'  # BOM头多出的内容
            exist_bom = lambda s: True if s == bom else False  # 定义一个匿名函数
            with open(self.config_path, 'rb') as fr:
                if exist_bom(fr.read(3)):  # 读取头3个字节进行判断
                    data = fr.read()
                    with open(self.config_path, 'wb') as fw:
                        fw.write(data)  # 利用二进制重新写入后BOM头就消失了

            # 读取文件
            self.cf.read(self.config_path, encoding="utf-8")
        except Exception as e:
            raise Exception("ReadConfig.__init__异常 %s" % e)

    def set_headers(self, value):
        """"更新配置文件中的headers"""
        self.cf.set("headers", "cookie", value)
        self.cf.write(open(self.config_path, "w", encoding="utf-8"))

    def get_web_param(self, value):
        """web参数"""
        value = self.cf.get("web_params", value)
        return value

    def get_app_param(self, value):
        """app参数"""
        value = self.cf.get("app_params", value)
        return value

    def get_origin(self, name):
        """传输协议，项目域名，端口，超时时长"""
        value = self.cf.get("origin", name)
        return value

    def get_headers(self, name):
        """headers信息"""
        value = self.cf.get("headers", name)
        return value

    def get_email(self, name):
        """邮箱配置"""
        value = self.cf.get("email", name)
        return value

    def get_db(self, name):
        """数据库配置"""
        value = self.cf.get("database", name)
        return value
