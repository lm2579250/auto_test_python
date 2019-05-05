import os
from PIL import Image
import zxing
import random
import logging


class ReadQRCode(object):

    def read_QR_code1(img_path):

        logger = logging.getLogger(__name__)
        if not logger.handlers:
            logging.basicConfig(level=logging.INFO)
        DEBUG = (logging.getLevelName(logger.getEffectiveLevel()) == 'DEBUG')

        # 在当前目录生成临时文件，规避java的路径问题
        img = Image.open(img_path)
        ran = int(random.random() * 100000)
        img.save('%s%s.jpg' % (os.path.basename(img_path).split('.')[0], ran))
        zx = zxing.BarCodeReader()
        data = ''
        zxing_data = zx.decode('%s%s.jpg' % (os.path.basename(img_path).split('.')[0], ran))
        # 删除临时文件
        os.remove('%s%s.jpg' % (os.path.basename(img_path).split('.')[0], ran))
        if zxing_data:
            logger.debug(u'zxing识别二维码:%s,内容: %s' % (img_path, zxing_data.parsed))
            data = zxing_data.parsed
        else:
            logger.error(u'识别zxing二维码出错:%s' % img_path)
            # img.save('%s-zxing.jpg' % img_path)
        return data

    def read_QR_code(img_path):

        logger = logging.getLogger(__name__)
        if not logger.handlers:
            logging.basicConfig(level=logging.INFO)
        DEBUG = (logging.getLevelName(logger.getEffectiveLevel()) == 'DEBUG')

        zx = zxing.BarCodeReader()
        zxing_data = zx.decode(img_path)
        data = ""

        if zxing_data:
            logger.debug(u'zxing识别二维码:%s,内容: %s' % (img_path, zxing_data.parsed))
            data = zxing_data.parsed
        else:
            logger.error(u'识别zxing二维码出错:%s' % img_path)
        return data


if __name__ == '__main__':
    img_path = '../data/2.jpg'
    text = ReadQRCode.read_QR_code(img_path)
    # logger.info('[%s]Zxing二维码识别:[%s]!!!' % (img_path, text))
    print(text)
