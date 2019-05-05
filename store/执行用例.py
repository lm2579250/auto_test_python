import unittest
class Test(unittest.TestCase):

    def setUp(self):
        print("11111111111111111111111")
        self.number = input('Enter a number:')
        self.number = int(self.number)

    def test_case1(self):
        print("a", self.number)
        self.assertEqual(self.number, 10, msg='Your input is not 10')

    def test_case2(self):
        print("b", self.number)
        self.assertEqual(self.number, 20, msg='Your input is not 20')

    # @unittest.skip('暂时跳过用例3的测试')
    def test_case3(self):
        print("c", self.number)
        self.assertEqual(self.number, 30, msg='Your input is not 30')

    def tearDown(self):
        print('Test over')
'''
# 方案一
if __name__ == '__main__':
    unittest.main()
# 方案二
suite = unittest.TestSuite()
suite.addTest(Test('test_case1'))
suite.addTest(Test('test_case2'))
runner = unittest.TextTestRunner()
runner.run(suite)
'''
# 方案三
test_dir = './'
discover = unittest.defaultTestLoader.discover(test_dir, pattern='test*.py')
runner = unittest.TextTestRunner()
runner.run(discover)