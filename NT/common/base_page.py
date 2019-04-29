import sys
import time
import threading
import appium.webdriver
import selenium.webdriver
from datetime import datetime
from NT.common.log import MyLog
from NT.common.common import Common
from NT.data.read_config import ReadConfig
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class BasePage(object):
    """页面元素基本操作,page module"""

    # web用例编号，web_driver用于标记web用例，app_driver用于标记APP用例
    web_case_num = 0
    web_driver = None
    app_driver = None
    _instance_lock = threading.Lock()  # 设置单例锁

    def __new__(cls, *args, **kwargs):
        """单例模式(支持多线程)"""
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        self.config = ReadConfig()
        self.log = MyLog().get_log().logger
        self.common = Common()

    def open_app(self):
        """打开app"""
        try:
            # 读取app参数
            system = self.config.get_app_param("system")  # 系统类型
            udid = self.config.get_app_param("udid")  # 手机udid
            version = self.config.get_app_param("version")  # 手机系统版本
            app_package = self.config.get_app_param("app_package")  # 待测app包名
            app_activity = self.config.get_app_param("app_activity")  # 待测app的activity名
            # app_address = self.config.get_app_param("app_address")  # app安装包路径
            # android_process = self.config.get_app_param("androidProcess")  # 小程序线程名

            desired_caps = {'platformName': system, 'platformVersion': version, 'automationName': 'appium',
                            'deviceName': 'udid', 'udid': udid, 'newCommandTimeout': 60,
                            'appActivity': app_activity, 'appPackage': app_package,
                            'unicodeKeyboard': True, 'resetKeyboard': True,
                            'setWebContentsDebuggingEnabled': True,
                            'recreateChromeDriverSessions': True,
                            'noReset': True,
                            # 'app': app_address,
                            # 'chromeOptions': {'androidProcess': android_process}
                            }
            self.app_driver = appium.webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
            global current_driver  # 用于标记是web端还是APP端的用例，以便后边方法调用
            current_driver = "app_driver"  # 标记为APP端用例
            self.switch_context()  # H5时需要切换context
        except Exception as e:
            self.log.error("打开app时异常 %s" % e)
            raise Exception

    def open_browser(self, browser="chrome"):
        """打开浏览器"""
        try:
            if browser == "chrome" or browser == "Chrome":
                driver = selenium.webdriver.Chrome()
            elif browser == "firefox" or browser == "Firefox" or browser == "FireFox" or browser == "ff":
                driver = selenium.webdriver.Firefox()
            elif browser == "ie" or browser == "IE" or browser == "internet explorer":
                driver = selenium.webdriver.Ie()
            else:
                raise Exception(self.log.error("没有找到浏览器 %s, 你可以输入'Chrome，Firefox or Ie'" % browser))
            self.web_driver = driver
            global current_driver  # 用于标记是web端还是APP端的用例，以便后边方法调用
            current_driver = "web_driver"  # 标记为web端用例
            self.web_driver.maximize_window()
        except Exception as e:
            self.log.error("打开%s浏览器时异常 %s" % (browser, e))
            raise Exception

    def get(self, url, element):
        """打开web端URL, element用于等待页面加载完成"""
        try:
            if url != "" or url != " ":
                self.web_driver.get(url)
                self.wait_elem(element)  # 等待元素出现
            else:
                raise Exception("URL地址错误！")
        except Exception as e:
            self.log.debug("打开网址时异常 %s" % e)
            raise Exception

    def refresh(self):
        """刷新页面"""
        if current_driver == "web_driver":
            self.web_driver.refresh()
        else:
            self.swipe_down()

    def back(self):
        """返回上一页"""
        if current_driver == "web_driver":
            self.web_driver.back()
        else:
            self.app_driver.keyevent(4)
        time.sleep(0.5)

    def quit(self):
        """退出程序"""
        try:
            if current_driver == "web_driver":
                self.web_driver.quit()
            else:
                # H5时用
                self.app_driver.switch_to.context("NATIVE_APP")
                # input_name = self.app_driver.active_ime_engine
                # self.log.debug("当前输入法：%s" % input_name)
                input_list = self.app_driver.available_ime_engines
                # self.log.debug("现有输入法：%s" % input_list)
                self.app_driver.activate_ime_engine(input_list[0])
                # input_name = self.app_driver.active_ime_engine
                # self.log.debug("更改当前输入法为：%s" % input_name)
                self.app_driver.quit()
        except Exception as e:
            self.log.error("退出程序时异常 %s" % e)
            raise Exception

    def click_elem_tag(self, elements, tag=0, roll=False, t=1):
        """根据元素下标点击元素"""
        for i in range(1, 6, +1):  # 操作失败后重试
            try:
                if roll:  # 是否需要滚动页面
                    self.location(elements, tag)  # app端页面上下微调
                elem = self.find_elements_tag(elements, tag)
                elem.click()
                time.sleep(t)
                break
            except Exception as e:
                time.sleep(1)
                self.log.debug("等待 %s s %s" % (i, e))
        else:
            self.log.debug("%s元素未出现！" % str(elements))
            raise Exception

    def input_tag(self, elements, text, tag=0, roll=False):
        """输入文本"""
        for i in range(1, 6, +1):  # 操作失败后重试
            try:
                if roll:  # 是否需要滚动页面
                    self.location(elements, tag)  # app端页面上下微调
                elem = self.find_elements_tag(elements, tag)
                elem.clear()
                elem.send_keys(text)
                break
            except Exception as e:
                time.sleep(1)
                self.log.debug("等待 %s s %s" % (i, e))
        else:
            self.log.debug("%s元素未出现！" % str(elements))
            raise Exception

    def get_text(self, *args, text="", tag=0):
        """获取文本内容，可多条，text为获取内容的标题/属性"""
        value = ""  # 文本内容
        for param in args:
            for i in range(1, 6, +1):  # 操作失败后重试
                try:
                    elem = self.find_elements_tag(param, tag)
                    value = elem.text  # web端获取文本内容

                    if value == "":
                        # app获取文本内容
                        value = elem.get_attribute("name")

                    if value != "":
                        self.log.debug("%s%s" % (text, value))
                        break
                except Exception as e:
                    time.sleep(1)
                    self.log.debug("等待 %s s %s" % (i, e))
            else:
                self.log.debug("%s元素未出现！" % str(param))
                raise Exception
        return value

    def switch_context(self, tag=1):
        """切换环境，tag=0时为android原生context"""
        try:
            contexts = self.app_driver.contexts   # 获取当前所有context
            self.log.debug("contexts:%s" % contexts)
            if len(contexts) != 1:  # 需要切换context
                self.app_driver.switch_to.context(contexts[tag])  # 切换context
                self.log.debug("切换context")
            context = self.app_driver.current_context  # 获取当前context
            self.log.debug("current_context: %s" % context)
        except Exception as e:
            self.log.debug("切换context时异常： %s" % e)
            raise Exception

    def switch_handle(self, element):
        """切换句柄"""
        try:
            handles = self.app_driver.window_handles
            if len(handles) != 1:  # 需要切换句柄
                self.log.debug("handles：%s" % handles)
                self.app_driver.switch_to.window(handles[-1])
                if self.displayed(element):  # 判断该句柄下是否有该元素
                    self.log.debug("切换handle")
            return self.displayed(element)
        except Exception as e:
            self.log.debug("切换handle时异常 %s" % e)
            raise Exception

    def home_page_to(self, module):
        """首页待办事项进入功能模块"""
        #  待办事项中的模块标签
        module_elem = ("xpath", "//span[contains(text(), '%s')]" % module)
        result = False
        try:
            if self.displayed(module_elem):
                self.log.debug("从首页的待办事项进入%s" % module)
                self.screen_shot()
                self.click_elem_tag(module_elem)
                self.screen_shot()
                result = True
            return result
        except Exception as e:
            self.log.debug("从首页的待办事项进入%s时异常 %s" % (module, e))
            raise Exception

    def back_to(self, *args):
        """返回(首页)或指定元素页面(须该页独有元素)"""
        try:
            home_menu = ("css_selector", "span.tab-title.ng-binding")  # 首页底部menu
            menu_elem = ()
            if args != ():
                menu_elem = args[0]
            self.log.debug("返回")
            i = 1
            while i <= 5:  # 最多返回5级页面
                self.back()
                self.screen_shot()
                if args == ():  # 返回首页
                    if self.switch_handle(home_menu):
                        self.click_elem_tag(home_menu)
                        break
                elif args != ():  # 返回指定元素页面
                    if self.switch_handle(menu_elem):
                        break
                self.log.debug("返回：%s" % i)
                i += 1
            else:
                self.log.debug("app返回异常，重新打开app")
                self.open_app()
        except Exception as e:
            self.log.error("返回时异常 %s" % e)
            raise Exception

    def popup(self):
        """获取弹框信息，点击按钮"""
        popup_title = ("css_selector", "h3.popup-title.ng-binding")  # 提示框title
        popup_info = ("css_selector", "div.popup-body")  # 提示信息
        popup_ok_button = ("css_selector", "button.button.ng-binding.button-calm")  # 确定按钮
        try:
            n = len(self.find_elements(popup_title))
            # self.log.debug("弹框数量：%s" % n)
            self.get_text(popup_title, popup_info, tag=n - 1)
            self.screen_shot()
            self.click_elem_tag(popup_ok_button, tag=n - 1)
            self.screen_shot()

        except Exception as e:
            self.log.error("操作弹框时异常 %s" % e)
            raise Exception

    def roll(self, elements):
        """web端页面下滑"""
        elem = self.find_elements_tag(elements)
        selenium.webdriver.ActionChains(self.web_driver).move_to_element(elem).perform()
        time.sleep(1)
        self.log.debug("滚动页面！")

    def screen_shot(self):
        """截图"""
        try:
            # 获取当前时间
            current_time = str(datetime.now().strftime("%H%M%S"))
            # 获取调用函数名
            func_name = sys._getframe().f_back.f_code.co_name
            # 获取调用行号
            line_number = sys._getframe().f_back.f_lineno

            path = self.common.get_result_path(case_name, "%s %s %s.png" % (current_time, func_name, line_number))
            if current_driver == "web_driver":  # web端直接截图
                self.web_driver.get_screenshot_as_file(path)
            else:  # 移动端截图
                contexts = self.app_driver.contexts  # 获取所有的context
                current_context = self.app_driver.current_context  # 获取当前的context
                if current_context == contexts[0]:  # 如果是android原生环境直接截图
                    self.app_driver.get_screenshot_as_file(path)
                else:  # 如果是H5页面先切换到android原生环境再截图
                    self.app_driver.switch_to.context(contexts[0])
                    self.app_driver.get_screenshot_as_file(path)
                    self.app_driver.switch_to.context(contexts[1])  # 截完图后回到原来的context
        except Exception as e:
            self.log.error("截图保存时异常 %s" % e)
            raise Exception

    def case_start(self, principal, api_case_name="", api_case_num=0):
        """用例开始，参数为负责人姓名，api测试名，api测试编号"""
        try:
            # 获取调用函数名作为截图文件夹名
            global case_name
            if api_case_name == "" and api_case_num == 0:
                case_name = sys._getframe().f_back.f_code.co_name
                self.web_case_num += 1
                self.log.debug("web用例%s：%s，负责人：%s" % (self.web_case_num, case_name, principal))
            else:
                # 将全局变量case_name重新赋值
                case_name = api_case_name
                self.log.debug("api用例%s：%s，负责人：%s" % (api_case_num, api_case_name, principal))
        except Exception as e:
            self.log.debug("用例开始时异常 %s" % e)
            raise Exception

    def case_end(self):
        """用例结束"""
        # "*"号不可改，用于提取用例失败的日志
        self.log.debug("*" * 100 + "\n")

    def case_pass(self):
        """用例通过"""
        self.log.debug("=" * 10 + "%s: pass!" % case_name + "=" * 10)

    def case_failed(self):
        """用例失败"""
        # "failed!"不可改，用于标记用例失败的日志
        self.log.debug("=" * 10 + "%s: failed!" % case_name + "=" * 10)

    def find_elements_tag(self, elements, tag=0):
        """查找元素(一个具体的元素点击和输入时定位)"""
        try:
            key = elements[0]  # 定位方式
            value = elements[1]  # 值

            if current_driver == "web_driver":  # web定位
                if key == "css_selector":
                    elem = self.web_driver.find_elements_by_css_selector(value)[tag]
                elif key == "xpath":
                    elem = self.web_driver.find_elements_by_xpath(value)[tag]
                elif key == "id":
                    elem = self.web_driver.find_elements_by_id(value)[tag]
                elif key == "name":
                    elem = self.web_driver.find_elements_by_name(value)[tag]
                elif key == "class":
                    elem = self.web_driver.find_elements_by_class_name(value)[tag]
                elif key == "link_text":
                    elem = self.web_driver.find_elements_by_link_text(value)
                elif key == "partial_link_text":
                    elem = self.web_driver.find_elements_by_partial_link_text(value)
                elif key == "tag_name":
                    elem = self.web_driver.find_elements_by_tag_name(value)[tag]
                else:
                    self.log.error("定位类型书写错误：%s" % str(elements))
                    raise Exception
                return elem
            else:  # app定位
                if key == "css_selector":
                    elem = self.app_driver.find_elements_by_css_selector(value)[tag]
                elif key == "xpath":
                    elem = self.app_driver.find_elements_by_xpath(value)[tag]
                elif key == "accessibility_id":
                    elem = self.app_driver.find_elements_by_accessibility_id(value)[tag]
                elif key == "id":
                    elem = self.app_driver.find_elements_by_id(value)[tag]
                elif key == "name":
                    elem = self.app_driver.find_elements_by_name(value)[tag]
                elif key == "class":
                    elem = self.app_driver.find_elements_by_class_name(value)[tag]
                elif key == "link_text":
                    elem = self.app_driver.find_elements_by_link_text(value)
                elif key == "partial_link_text":
                    elem = self.app_driver.find_elements_by_partial_link_text(value)
                elif key == "tag_name":
                    elem = self.app_driver.find_elements_by_tag_name(value)[tag]
                else:
                    self.log.error("定位类型书写错误：%s" % str(elements))
                    raise Exception
                return elem
        except Exception as e:
            # self.log.debug("元素不存在：%s，%s" % (str(elements), e))
            raise Exception

    def find_elements(self, elements):
        """查找元素集合"""
        try:
            key = elements[0]
            value = elements[1]

            if current_driver == "web_driver":  # web查找元素
                if key == "css_selector":
                    elem = self.web_driver.find_elements_by_css_selector(value)
                elif key == "xpath":
                    elem = self.web_driver.find_elements_by_xpath(value)
                elif key == "id":
                    elem = self.web_driver.find_elements_by_id(value)
                elif key == "name":
                    elem = self.web_driver.find_elements_by_name(value)
                elif key == "class_name":
                    elem = self.web_driver.find_elements_by_class_name(value)
                elif key == "link_text":
                    elem = self.web_driver.find_elements_by_link_text(value)
                elif key == "partial_link_text":
                    elem = self.web_driver.find_elements_by_partial_link_text(value)
                elif key == "tag_name":
                    elem = self.web_driver.find_element_by_tag_name(value)
                else:
                    self.log.error("函数类型书写错误：%s" % str(elements))
                    raise Exception
                return elem
            else:  # APP查找元素
                if key == "css_selector":
                    elem = self.app_driver.find_elements_by_css_selector(value)
                elif key == "xpath":
                    elem = self.app_driver.find_elements_by_xpath(value)
                elif key == "accessibility_id":
                    elem = self.app_driver.find_elements_by_accessibility_id(value)
                elif key == "id":
                    elem = self.app_driver.find_elements_by_id(value)
                elif key == "name":
                    elem = self.app_driver.find_elements_by_name(value)
                elif key == "class":
                    elem = self.app_driver.find_elements_by_class_name(value)
                elif key == "link_text":
                    elem = self.app_driver.find_elements_by_link_text(value)
                elif key == "partial_link_text":
                    elem = self.app_driver.find_elements_by_partial_link_text(value)
                elif key == "tag_name":
                    elem = self.app_driver.find_elements_by_tag_name(value)
                else:
                    self.log.error("函数类型书写错误：%s" % str(elements))
                    raise Exception
                return elem
        except Exception as e:
            # self.log.debug("元素不存在：%s，%s" % (str(elements), e))
            raise Exception

    def wait_elem(self, element):
        """等待元素出现"""
        key = element[0]
        value = element[1]
        locator = None

        try:
            if key == "css_selector":
                locator = (By.CSS_SELECTOR, value)
            elif key == "xpath":
                locator = (By.XPATH, value)
            elif key == "id":
                locator = (By.ID, value)
            elif key == "name":
                locator = (By.NAME, value)
            elif key == "class":
                locator = (By.CLASS_NAME, value)
            elif key == "link_text":
                locator = (By.LINK_TEXT, value)
            elif key == "partial_link_text":
                locator = (By.PARTIAL_LINK_TEXT, value)
            elif key == "tag_name":
                locator = (By.TAG_NAME, value)

            if current_driver == "web_driver":
                WebDriverWait(self.web_driver, 20, 0.5).until(ec.presence_of_element_located(locator),
                                                              "%s元素未出现！" % str(element))
            else:
                WebDriverWait(self.app_driver, 20, 0.5).until(ec.presence_of_element_located(locator),
                                                              "%s元素未出现！" % str(element))
        except Exception as e:
            self.log.debug("等待元素出现时异常 %s" % e)
            raise Exception

    # def judgment(self, elements, tag=0):
    #     """判断元素是否存在"""
    #     for i in range(1, 6, +1):
    #         time.sleep(1)
    #         try:
    #             self.find_elements_tag(elements, tag)
    #             return True
    #         except Exception as e:
    #             self.log.debug(e)
    #             return False

        # 方式二（速度较慢）：
        # key = elements[0]
        # value = elements[1]
        # locator = None
        #
        # if key == "css_selector":
        #     locator = (By.CSS_SELECTOR, value)
        # elif key == "xpath":
        #     locator = (By.XPATH, value)
        # elif key == "id":
        #     locator = (By.ID, value)
        # elif key == "name":
        #     locator = (By.NAME, value)
        # elif key == "class":
        #     locator = (By.CLASS_NAME, value)
        # elif key == "link_text":
        #     locator = (By.LINK_TEXT, value)
        # elif key == "partial_link_text":
        #     locator = (By.PARTIAL_LINK_TEXT, value)
        # elif key == "tag_name":
        #     locator = (By.TAG_NAME, value)
        #
        # if current_driver == "web_driver":
        #     try:
        #         WebDriverWait(self.web_driver, 20, 0.5).until(lambda x: x.find_element(*locator))
        #         return True
        #     except:
        #         return False
        # else:
        #     try:
        #         WebDriverWait(self.app_driver, 20, 0.5).until(lambda x: x.find_element(*locator))
        #         return True
        #     except:
        #         return False

    def displayed(self, elements, tag=0):
        """判断元素是否可见"""
        try:
            elem = self.find_elements_tag(elements, tag)
            return elem.is_displayed()  # 元素可见为True，隐藏为False
        except:
            # 没有找到元素
            return False

    def swipe_up(self, x=0.5, y1=0.85, y2=0.15, t=500):
        """屏幕向上滑动"""
        try:
            self.swipe(x, y1, y2, t)
            self.log.debug("上滑")
        except Exception as e:
            self.log.error("屏幕向上滑动时异常 %s" % e)
            raise Exception

    def swipe_down(self, x=0.5, y1=0.15, y2=0.85, t=500):
        """屏幕向下滑动"""
        try:
            self.swipe(x, y1, y2, t)
            self.log.debug("下滑")
        except Exception as e:
            self.log.error("屏幕向下滑动时异常 %s" % e)
            raise Exception

    def swipe(self, x, y1, y2, t):
        """上下滑动"""
        try:
            coordinate_x = self.app_driver.get_window_size()['width']  # 获取屏幕宽度
            coordinate_y = self.app_driver.get_window_size()['height']  # 获取屏幕高度
            x1 = int(coordinate_x * x)  # x坐标
            y1 = int(coordinate_y * y1)  # 起始y坐标
            y2 = int(coordinate_y * y2)  # 终点y坐标
            self.app_driver.swipe(x1, y1, x1, y2, t)
            time.sleep(1)
        except Exception as e:
            raise Exception(e)

    def location(self, element, tag=0):
        """屏幕内容上下微调"""
        current_context = ""
        try:
            elem = self.find_elements_tag(element, tag)  # css_selector不能在android环境下定位，所以定位完成后再切换环境
            y1 = elem.location["y"]  # 获取元素y坐标
            # self.log.debug(y1)

            contexts = self.app_driver.contexts  # 获取所有的context
            current_context = self.app_driver.current_context  # 获取当前的context
            if current_context != contexts[0]:  # 当前为非android环境时需要切换为APP_context才能进行滑动操作
                self.app_driver.switch_to.context(contexts[0])

            y2 = self.app_driver.get_window_size()['height']  # 获取屏幕高度
            # self.log.debug(y2)

            # 判断是否需要滑动
            while y1 + 200 > y2 or y1 < 100:
                if y1 + 200 > y2:
                    self.swipe(x=0.02, y1=0.85, y2=0.45, t=500)  # 向上滑
                    self.screen_shot()

                n = y1

                if current_context == contexts[1]:  # 当前为非H5环境时需要切换为H5环境才能获取元素坐标
                    self.app_driver.switch_to.context(contexts[1])
                y1 = elem.location["y"]
                # self.log.debug(y1)
                if current_context != contexts[0]:  # 当前为非android环境时需要切换为APP_context才能进行滑动操作
                    self.app_driver.switch_to.context(contexts[0])

                if y1 < 100:
                    self.swipe(x=0.02, y1=0.60, y2=0.75, t=500)  # 向下滑
                    self.screen_shot()

                if n == y1:
                    break
        except Exception as e:
            self.log.debug("位置调整时异常 %s" % e)
            raise Exception
        finally:
            self.app_driver.switch_to.context(current_context)  # 微调完成后切换为原来的环境
