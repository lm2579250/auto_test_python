import os
import json
import logging
import threading
from NT.data.read_config import ReadConfig
from NT.common.common import Common


class Log(object):
    _instance_lock = threading.Lock()  # 设置单例锁

    def __new__(cls, *args, **kwargs):
        """单例模式(支持多线程)"""
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        """配置日志数据"""
        self.common = Common()
        try:
            # 生成日志文件
            log_path = self.common.get_result_path("result.log")

            # 定义logger
            self.logger = logging.getLogger()
            # 定义输出等级
            self.logger.setLevel(logging.DEBUG)

            # 日志输出到屏幕控制台
            sh = logging.StreamHandler()
            # 设置日志等级
            sh.setLevel(logging.DEBUG)

            # 输出日志信息到log_path
            fh = logging.FileHandler(log_path, encoding="utf-8")
            # 设置日志等级
            fh.setLevel(logging.DEBUG)

            # 设置handler的格式对象
            formatter = logging.Formatter(
                '%(asctime)s %(name)s %(filename)s %(module)s [line:%(lineno)d] %(levelname)s %(message)s')

            # 设置handler的格式对象
            sh.setFormatter(formatter)
            fh.setFormatter(formatter)

            # 将handler增加到logger中
            self.logger.addHandler(sh)
            self.logger.addHandler(fh)
        except Exception as e:
            raise Exception("Log.__init__异常 %s" % e)


class MyLog:
    log = None
    mutex = threading.Lock()

    def __init__(self):
        self.common = Common()

    @staticmethod
    def get_log():
        """日志单例模式"""
        try:
            if MyLog.log is None:
                MyLog.mutex.acquire()
                MyLog.log = Log()
                MyLog.mutex.release()
            return MyLog.log
        except Exception as e:
            raise Exception("MyLog.get_log异常 %s" % e)

    def extraction_error_log(self):
        """按负责人提取错误日志"""
        try:
            # 生成原始日志文件路径
            log_path = self.common.get_result_path("result.log")
            # 生成错误日志文件路径
            error_log_path = self.common.get_result_path("error.log")

            # 从邮件的收件人信息中读取所有的负责人姓名，实现错误日志按人分类
            config = ReadConfig()
            # 收件人列表str类型(姓名，邮箱)
            receivers = config.get_email("receivers")
            # 收件人列表dict类型(姓名，邮箱)
            receivers_dict = json.loads(receivers)
            principal_list = []  # 收件人姓名列表
            for key, value in receivers_dict.items():
                principal_list.append(key)

            data = ""  # 单个错误日志临时存储器
            error = False  # 错误日志标识
            all_error_num = 0  # 错误用例总的编号
            # principal_error_num = 0  # 负责人的错误编号
            i = 1  # 原始日志中的文本行数
            j = 1  # 单个用例内的行数

            # 打开原始日志
            with open(log_path, "r", encoding="utf-8") as log:
                # 打开错误日志
                with open(error_log_path, "w", encoding="utf-8") as error_log:
                    lines = log.readlines()  # 读取原始日志

                    principal = ""  # 用例负责人
                    for line in lines:
                        # 匹配负责人姓名，以便是错误日志时创建负责人对应的错误日志文件名，负责人姓名在单个用例的第一行
                        if j == 1:
                            for name in principal_list:
                                if name in line:
                                    principal = name

                        # 临时存储一个用例的日志
                        data = data + line
                        # line中包含"ERROR"的标记为错误日志
                        if "failed!" in line:
                            error = True
                        # "*"不可改，出现"*"表示一个用例结束，一个用例结束并被标记为错误日志的内容被写入error_log和principal_log文件
                        if "*" * 100 in line and error is True:
                            all_error_num += 1
                            error_log.write("\n错误用例%s：" % str(all_error_num))
                            # 所有错误日志写入一个文件中
                            error_log.write(data)

                            # 将错误日志提取到对应负责人的日志文件中
                            # 负责人对应的错误日志名
                            principal_log_name = "%s.log" % principal
                            # 生成负责人对应的错误日志路径
                            principal_log_path = self.common.get_result_path(principal_log_name)
                            # 按负责人分类写入对应的文件中
                            # 判断principal_log_path是否存在
                            if not os.path.exists(principal_log_path):
                                with open(principal_log_path, "w+", encoding="utf-8") as principal_log:
                                    principal_log.write(data)
                            else:
                                with open(principal_log_path, "a+", encoding="utf-8") as principal_log:
                                    principal_log.write(data)

                            # 有错误日志时恢复初始化
                            data = ""
                            error = False
                            j = 1
                        # "*"不可改
                        elif "*" * 100 in line:
                            # 没有错误日志时恢复初始化
                            data = ""
                            error = False
                            j = 1
                        i += 1
            # 如果没有错误日志，就删除空的error_log文件
            if os.path.exists(error_log_path) and os.path.getsize(error_log_path) == 0:
                os.remove(error_log_path)
        except Exception as e:
            raise Exception("MyLog.extraction_error_log异常 %s" % e)
