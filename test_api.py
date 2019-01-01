# -*- coding:utf-8 -*-
"""上传文件测试"""

import datetime
import sys

import requests

default_encode = 'utf-8'

def test_post():
    # api = 'http://127.0.0.1:48703/api/classify'
    api = 'http://47.74.234.157:48703/api/classify'

    filename1 = './gesture/test/0/0.jpg'
    filename2 = './gesture/test/0/0.jpg'

    files = {
        "filename1": (filename1, open(filename1, "rb")),
        "filename2": (filename2, open(filename2, "rb")),
    }
    r = requests.post(url=api, files=files)
    print r.text


if __name__ == '__main__':
    if sys.getdefaultencoding() != default_encode:
        reload(sys)
        sys.setdefaultencoding(default_encode)

    test_post()
