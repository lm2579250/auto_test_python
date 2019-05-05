import unittest, time
from selenium import webdriver


class canDao(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.url = "http://bug.mobimedical.cn/www/index.php?m=user&f=login&referer=L3d3dy9pbmRleC5waHA.bT1teSZmPWluZGV4"
        self.driver.implicitly_wait(30)
        self.users = {'?': '#', '': '123456', 'huangminghua': '123456', 'huang': '123456', ' ': ' '}

    def test_login(self):
        i = 0
        driver = self.driver
        driver.get(self.url)
        print(len(self.users), self.users)
        for user, pwd in self.users.items():
            i += 1
            print(driver.title)
            driver.find_element_by_id("account").clear()
            driver.find_element_by_id("account").send_keys(user)
            driver.find_element_by_name("password").clear()
            driver.find_element_by_name("password").send_keys(pwd)
            driver.find_element_by_id("submit").click()
            time.sleep(1)
            print(driver.title)
            try:
                driver.switch_to.frame("hiddenwin")
                msg = driver.switch_to.alert
                print(msg.text)
                msg.accept()
                driver.switch_to.default_content()
            except:
                driver.switch_to.default_content()
                driver.find_element_by_link_text("退出").click()
                time.sleep(1)
                driver.switch_to.default_content()
            finally:
                if user == "huangminghua" and pwd == "123456":
                    print('%d:登录成功！(%r,%r)' % (i, user, pwd))
                    print(driver.current_url)
                elif user == "" or user == " ":
                    print("%d:请数输入用户名！(%s,%s)" % (i, user, pwd))
                    print(driver.current_url)
                elif pwd == "" or pwd == " ":
                    print("%d:请数输入密码！(%s,%s)" % (i, user, pwd))
                    print(driver.current_url)
                else:
                    print("%d:登录信息错误！(%s,%s)" % (i, user, pwd))
                    print(driver.current_url)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
