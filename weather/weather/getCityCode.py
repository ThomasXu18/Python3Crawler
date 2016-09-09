#-*- coding:utf-8 -*-

import urllib
import urllib.request
import time
import json
import _thread
import pymysql



citycode = '101'

def my_func(p_citycode,start,end):
    for i in range(start, end):
        c_citycode = p_citycode + (('%04d') % (i))
        print(c_citycode)
        headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'  }      
        req = urllib.request.Request(url = ('http://www.weather.com.cn/data/cityinfo/%s.html'%str(c_citycode)),headers=headers);          
        try:
            content = urllib.request.urlopen(req).read()
            data = json.loads(content.decode())
        except json.decoder.JSONDecodeError as e:
            continue
        except Exception as ex:
            continue
        result = data['weatherinfo']
        str_info = ('%s %s') % (result['city'],result['cityid'])
        insert_new_rows(result['city'],result['cityid'])
        print(str_info)


def insert_new_rows(cityname, citycode):
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='',db='citycode',charset='UTF8')
    cur = conn.cursor()
    cur.execute("insert into citycode (cityname, citycode) values (%s, %s)", (cityname, citycode))
    conn.commit()
    cur.close()
    conn.close()

for x in range(1,35):
    p_citycode = citycode + (('%02d') % (x))
    print(x)
    _thread.start_new_thread(my_func,(p_citycode,1,4000))
