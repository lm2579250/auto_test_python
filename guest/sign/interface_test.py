import requests
import unittest


class GetEventListTest(unittest.TestCase):
    """查询发布会接口"""

    def setUp(self):
        self.url = "http://127.0.0.1:8000/api/get_event_list/"

    def test_get_event_null(self):
        """发布会 id 为空"""

        r = requests.get(self.url, params={'eid': ''})
        result = r.json()
        print(result)
        self.assertEqual(result['status'], 10021)
        self.assertEqual(result['message'], "parameter error")

    def test_get_event_success(self):
        """发布会 id 为 1，查询成功"""

        r = requests.get(self.url, params={'eid': '1'})
        result = r.json()
        print(result)
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], "success")
        self.assertEqual(result['data']['name'], "小米5发布会")
        self.assertEqual(result['data']['address'], "北京市故宫博物院")
        self.assertEqual(result['data']['start_time'], "2019-03-14T12:18:17")

    def test_get_all_event_success(self):
        """所有发布会，查询成功"""

        r = requests.get(self.url, params={'name': '发布会'})
        result = r.json()
        print(result)
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], "success")


if __name__ == '__main__':
    unittest.main()
