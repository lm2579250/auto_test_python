import os
import re
import json
import shutil
import zipfile
import smtplib
import threading
import email.mime.text
import email.mime.multipart
from email.header import Header
from email.mime.application import MIMEApplication
from NT.common.common import Common
from NT.data.read_config import ReadConfig
from NT.common.log import MyLog


class SendEmail(object):
    """发送测试报告"""
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
            self.common = Common()  # 实例化一个common调用公用函数
            self.log = MyLog().get_log().logger  # 实例化一个log打印日志
            self.config = ReadConfig()  # 实例化一个read_config读取email的配置信息
            self.msg = email.mime.multipart.MIMEMultipart('alternative')  # 实例化一个email发送email
        except Exception as e:
            self.log.error("SendEmail.__init__异常 %s" % e)

    def with_zip(self):
        """附件以zip格式发送邮件"""

        result = False  # 发送结果标志
        num = 0  # 发送失败后重试次数
        # 发送失败后重试3次
        while result is False and num < 3:
            try:
                global log_dir, zip_path
                log_dir = self.common.get_result_path()  # 获取存储日志的目录
                file_list = os.listdir(log_dir)  # 获取目录下的文件列表
                zip_path = log_dir + ".zip"  # 设置存放zip的路径

                # 提取错误负责人
                principal_name_list = []  # 错误负责人list
                for file in file_list:
                    file_name = os.path.splitext(file)[0]  # 文件名
                    # 用正则表达式查找文件名为汉字的文件(负责人对应的错误日志文件)，正则表达式为：非汉字的字符用""替换掉
                    if file_name == re.sub("[^\u4e00-\u9fa5]+", "", file_name):
                        principal_name_list.append(file_name)  # 添加负责人姓名到错误负责人list中

                # 从配置文件中读取发件人信息
                sender_name = ""  # 发件人
                sender_email = ""  # 发件箱
                sender_dict = json.loads(self.config.get_email("sender"))
                for key, value in sender_dict.items():
                    sender_name = key
                    sender_email = value

                # 从配置文件中读取收件人信息
                # receivers内容为字典时使用(receivers = {"蓝梦":"597878110@qq.com", "孟冰":"597878110@qq.com")
                receivers_dict = json.loads(self.config.get_email("receivers"))
                name_list = []  # 收件人list
                receivers = []  # 收件箱list
                for key, value in receivers_dict.items():
                    if key in principal_name_list:
                        name_list.append(key)
                        receivers.append(value)

                # 创建一个写入的zip对象
                with zipfile.ZipFile(zip_path, mode='w', compression=zipfile.ZIP_DEFLATED) as zip_obj:
                    for path, folders, files in os.walk(log_dir):
                        for file in files:
                            zip_obj.write(os.path.join(path, file))
                # 添加附件
                part = MIMEApplication(open(zip_path, 'rb').read())  # 读取内容
                part.add_header('Content-Disposition', 'attachment', filename=('gbk', '', "result.zip"))  # 设置附件名
                self.msg.attach(part)
                # 邮件信息
                name_list_str = ",".join(name_list)  # 收件人姓名，将list转换为str
                mail_host = self.config.get_email("email_host")  # 设置邮箱服务器域名
                mail_port = self.config.get_email("email_port")  # 设置邮箱服务器接口
                mail_user = self.config.get_email("email_user")  # 发件人用户名
                mail_pass = self.config.get_email("email_pass")  # 发件人口令
                subject = self.config.get_email("subject")  # 主题
                content = self.config.get_email("content")  # 正文
                if len(name_list_str) == 0:
                    self.log.debug("所有用例都正常通过！")
                else:
                    self.log.debug("发件人：%s" % sender_name)
                    self.log.debug("收件人：%s" % name_list_str)

                    txt = email.mime.text.MIMEText(content, 'plain', 'utf-8')
                    self.msg.attach(txt)
                    self.msg['Subject'] = Header(subject, 'utf-8')
                    self.msg['From'] = Header(sender_name, 'utf-8')
                    self.msg['To'] = Header("%s" % name_list_str, 'utf-8')

                    # 调用邮箱服务器
                    smt_obj = smtplib.SMTP_SSL(mail_host, mail_port)
                    # 登录邮箱
                    smt_obj.login(mail_user, mail_pass)
                    # 发送邮件
                    smt_obj.sendmail(sender_email, receivers, self.msg.as_string())
                    # 关闭邮箱
                    smt_obj.quit()
                    self.log.debug("发送成功！")
                result = True
            except Exception as e:
                self.log.error("发送失败 %s" % e)
                num += 1
            finally:
                os.remove(zip_path)  # 删除zip文件
                self.remove_result()

    def with_file(self):
        """附件以单个文件形式发送邮件"""

        result = False  # 发送结果标志
        num = 0  # 发送失败后重试次数
        # 发送失败后重试3次
        while result is False and num < 3:
            try:
                # 添加附件
                global log_dir
                log_dir = self.common.get_result_path()  # 获取存储日志的目录
                file_list = os.listdir(log_dir)  # 获取目录下的文件列表
                principal_name_list = []  # 错误负责人list
                for file in file_list:
                    file_name = os.path.splitext(file)[0]  # 文件名
                    file_type = os.path.splitext(file)[1]  # 文件类型

                    # 用正则表达式查找文件名为汉字的文件(负责人对应的错误日志文件)，正则表达式为：非汉字的字符用""替换掉
                    if file_name == re.sub("[^\u4e00-\u9fa5]+", "", file_name):
                        principal_name_list.append(file_name)  # 添加负责人姓名到错误负责人list中
                        current_file = os.path.join(log_dir, file)  # 拼接当前的日志路径
                        part = MIMEApplication(open(current_file, 'rb').read())  # 读取当前的日志
                        part.add_header('Content-Disposition', 'attachment', filename=('gbk', '', file))  # 设置附件名
                        self.msg.attach(part)
                    elif file_type == ".html":  # 查找html文件
                        current_file = os.path.join(log_dir, file)  # 拼接当前的日志路径
                        part = MIMEApplication(open(current_file, 'rb').read())  # 读取当前的日志
                        part.add_header('Content-Disposition', 'attachment', filename=('gbk', '', file))  # 设置附件名
                        self.msg.attach(part)
                    elif "error" in file_name:  # 查找错误日志文件
                        current_file = os.path.join(log_dir, file)  # 拼接当前的日志路径
                        part = MIMEApplication(open(current_file, 'rb').read())  # 读取当前的日志
                        part.add_header('Content-Disposition', 'attachment', filename=('gbk', '', file))  # 设置附件名
                        self.msg.attach(part)

                # 从配置文件中读取邮件信息
                sender_name = ""  # 发件人
                sender_email = ""  # 发件箱
                sender_dict = json.loads(self.config.get_email("sender"))
                for key, value in sender_dict.items():
                    sender_name = key  # 发件人
                    sender_email = value  # 发件箱

                # receivers内容为字典时使用(receivers = {"蓝梦":"597878110@qq.com", "孟冰":"597878110@qq.com")
                receivers_dict = json.loads(self.config.get_email("receivers"))
                name_list = []  # 收件人list
                receivers = []  # 收件箱list
                for key, value in receivers_dict.items():
                    if key in principal_name_list:
                        name_list.append(key)
                        receivers.append(value)

                name_list_str = ",".join(name_list)  # 收件人姓名，将list转换为str
                mail_host = self.config.get_email("email_host")  # 设置邮箱服务器域名
                mail_port = self.config.get_email("email_port")  # 设置邮箱服务器接口
                mail_user = self.config.get_email("email_user")  # 发件人用户名
                mail_pass = self.config.get_email("email_pass")  # 发件人口令
                subject = self.config.get_email("subject")  # 主题
                content = self.config.get_email("content")  # 正文
                if len(name_list_str) == 0:
                    self.log.debug("所有用例都正常通过！")
                else:
                    self.log.debug("发件人：%s" % sender_name)
                    self.log.debug("收件人：%s" % name_list_str)

                    txt = email.mime.text.MIMEText(content, 'plain', 'utf-8')
                    self.msg.attach(txt)
                    self.msg['Subject'] = Header(subject, 'utf-8')
                    self.msg['From'] = Header(sender_name, 'utf-8')
                    self.msg['To'] = Header("%s" % name_list_str, 'utf-8')

                    # 调用邮箱服务器
                    smt_obj = smtplib.SMTP_SSL(mail_host, mail_port)
                    # 登录邮箱
                    smt_obj.login(mail_user, mail_pass)
                    # 发送邮件
                    smt_obj.sendmail(sender_email, receivers, self.msg.as_string())
                    # 关闭邮箱
                    smt_obj.quit()
                    self.log.debug("发送成功！")
                result = True
            except Exception as e:
                self.log.error("发送失败： %s" % e)
                num += 1
            finally:
                self.remove_result()

    def remove_result(self):
        """发送报告后删除其他的文件夹"""
        try:
            result_path = os.path.dirname(log_dir)  # 获取result目录路径
            result_list = os.listdir(result_path)  # 获取result下的文夹列表
            i = len(result_list)  # 统计文件夹数量
            for file in result_list:
                path = os.path.join(result_path, file)  # 拼接每个文件夹的路径
                if i > 1:  # 保留最新的文件夹
                    shutil.rmtree(path)
                    i -= 1
        except Exception as e:
            self.log.error("删除result下文件夹时异常：%s" % e)
            raise Exception
