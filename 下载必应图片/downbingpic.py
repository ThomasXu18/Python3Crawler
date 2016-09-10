# -*- coding:utf-8 -*-

import re
import requests
import time
import os


date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
string = date + '.jpg'
if os.path.isfile(string):
    print("Picture already exists")
else:
    url = "http://cn.bing.com/"
    html = requests.get(url).text
    pic_url = re.findall(r'http://[0-9a-zA-Z\_:./-]*jpg', html)
    print(pic_url)
    try:
        pic = requests.get(pic_url[0], timeout=10)
    except requests.exceptions.ConnectionError:
        print("error")
    except requests.exceptionns.Timeout:
        print("error")

    fp = open(string, 'wb')
    fp.write(pic.content)
    fp.close()
