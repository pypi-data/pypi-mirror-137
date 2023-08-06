# -*- coding: UTF-8 -*-
# name = 'expy'

from cmath import log
from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING
from threading import Thread, BoundedSemaphore as IthreadBoundedSemaphore

def genQRCode(url, midImg):
    """
    url - 二维码对应网址。

    img - 二维码中间图片文件路径。
    """

    from PIL import Image
    from qrcode import QRCode
    from qrcode.constants import ERROR_CORRECT_H

    qrdata = QRCode(version=1, error_correction=ERROR_CORRECT_H)  # 设置容错率为最高
    qrdata.add_data(url)
    qrdata.make()
    qrimg = qrdata.make_image()
    # 设置二维码为彩色
    qrimg = qrimg.convert("RGBA")
    factor = 4
    size_w = int(qrimg.size[0] / factor)
    size_h = int(qrimg.size[1] / factor)

    with Image.open(midImg) as icon:
        # 转换图标为彩色，测试不是必须
        # icon = icon.convert("RGBA")

        # 重设图标大小，确保不会过大
        icon_w, icon_h = icon.size
        if icon_w > size_w: icon_w = size_w
        if icon_h > size_h: icon_h = size_h
        icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)

        local_w = int((qrimg.size[0] - icon_w) / 2)
        local_h = int((qrimg.size[1] - icon_h) / 2)
        maskimg = Image.new("RGBA", (icon_w + 8, icon_h + 8), (255, 255, 255))
        # qrimg.paste(maskimg, (qrimg_w - 4, qrimg_h - 4), maskimg)
        # qrimg.paste(icon, (qrimg_w, qrimg_h), icon)
        qrimg.paste(maskimg, (local_w - 4, local_h - 4))
        qrimg.paste(icon, (local_w, local_h))

    return qrimg


def genLogger(name=__file__, path=None, lvl=DEBUG,file=''):
    """
    name - 日志器名称

    path - 日志文件输出路径, 如果没有指定则不写文件日志，日志文件夹总是命名为Log，如果路径末尾不含Log/，自动追加Log文件夹。

    lvl  - 日志级别，默认DEBUG

    file - 日志文件名称，如果没有给定，则以日期命名。
    """
    
    import logging, os
    from time import strftime

    logger = logging.getLogger(name)
    logger.setLevel(lvl)

    # 关联日志到控制台
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter('%(filename)12s:%(lineno)3d - %(levelname)5s: %(message)s'))
    logger.addHandler(ch)

    # 如果有路径则写文件日志
    if path:
        # 判断是否标准操作系统路径
        assert os.path.isdir(path) == True,'路径参数<path>不合法!'
        # 确保路径以分隔符结束
        if not path.endswith(os.sep):
            path = path + os.sep

        # 确保路径以'Log/'结束
        if (path.split(os.sep)[-1].lower() != 'log'):
            path = path + 'Log' + os.sep

        # 判断并生成文件夹
        if not os.path.exists(path):
            os.makedirs(path)
        # 生成日志文件名称
        logfile = path +(file or (strftime('%m-%d') + '.log'))

        # 关联日志到文件
        fh = logging.FileHandler(logfile, 'a', encoding='UTF-8')
        fh.setFormatter(logging.Formatter('%(asctime)s %(filename)12s :%(lineno)3d - %(levelname)5s: %(message)s'))
        logger.addHandler(fh)
    return logger


def genChromeHeaders(cookie: str = None):
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'cookie': cookie
    }


#  实用类


class Ithread(Thread):
    def __init__(self, func, args):
        Thread.__init__(self)
        self.func = func
        self.args = args

    def getResult(self):
        return self.result

    def run(self):
        self.result = self.func(*self.args)


class RestoreNesting(object):
    outdict = {}

    def __init__(self):
        self.outdict = {}

    #将多层嵌套的dict，解包为单层，key相加。
    def nested_dict(self, indict, parentkey=''):
        for key in indict:
            if isinstance(indict[key], dict):
                self.nested_dict(indict[key], parentkey + str(key) + '-')
            else:
                self.outdict[parentkey + str(key)] = indict[key]
        return self.outdict