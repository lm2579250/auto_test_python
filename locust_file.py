from NT.common.read_config import ReadConfig
from locust import HttpLocust, TaskSet


class UserBehavior(TaskSet):
    def on_start(self):
        with self.client.get(r'/pc/qrcode/get/qrcode?qrCodeUrl=https%3A%2F%2Fntapp.hushijie.com.cn%2Fwx%2Fprogram%2Fercode%2F%3FhospitalId%3D22%26id%3D985%26hospitalName%3D%E5%8C%97%E4%BA%AC%E6%B5%8B%E8%AF%95%E5%8C%BB%E9%99%A2%26qrcodeType%3DMEETING%26meetingType%3D2&functionShortname=qrWxProgreamCodeEventMeetingUrl', catch_response=True) as response:
            print(response.status_code)
            if response.status_code != 200:
                response.failure('failed!')
            else:
                response.success()


class User(HttpLocust):
    cf = ReadConfig()
    host = r"https://admin.hushijie.com.cn"

    task_set = UserBehavior
    min_wait = 1000
    max_wait = 3000
