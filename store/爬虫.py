import urllib, re, time
import urllib.request
'''
def get_image(url):
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    get_img = response.read()
    with open('E:\Python/tests\images/001.jpg', 'wb') as fp:
        fp.write(get_img)
        print("图片下载完成！")
        return
url = 'http://upload-images.jianshu.io/upload_images/2917634-7667382cc63b833d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240'
get_image(url)

def download_page(url):
    request = urllib.request.Request(url)
    time.sleep(2)
    response = urllib.request.urlopen(request)
    data = response.read()
def get_image(html):
    regx = r'http://[\s]*.jpg'
    pattern = re.compile(regx)
    get_img = re.findall(pattern, repr(html))
    num = 1
    for img in get_img:
        image = download_page(img)
        with open('E:\Python/tests\images\%s,jpg' % num, 'wb') as fp:
            fp.write(image)
            num += 1
            print("正在下载第%s张图片", num)
    return

url = 'about:cehome'
html = download_page(url)
get_image(html)
'''
import Queue

initial_page = ""
url_queue = Queue.Queue()