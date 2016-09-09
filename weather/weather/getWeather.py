#-*- coding:utf-8 -*-

import urllib
import urllib.request
import time
import json
import _thread
import pymysql


def getCityWeather(cityCode):
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/200160801 Firefox/3.5.6'  }      
    req = urllib.request.Request(url = ('http://www.weather.com.cn/data/cityinfo/%s.html'%str(cityCode)),headers=headers);
    content = urllib.request.urlopen(req).read()
    data = json.loads(content.decode())
    result = data['weatherinfo']
    insert_new_weatherinfo(result) 
    print(result)

def query_all_city_weather():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='mysql',db='citycode',charset='UTF8')
    cur = conn.cursor()
    cur.execute("select citycode from citycode order by citycode")
    for i in cur:
        getCityWeather(i[0])      
    cur.close()
    conn.close()

def insert_new_weatherinfo(result):
    cityname = result['city']
    mintemp = result['temp1']
    maxtemp = result['temp2']
    weatherinfo = result['weather']
    if result.__contains__('ptime'):
        ptime = result['ptime']
    else:
        ptime = '--:--'    
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='',db='citycode',charset='UTF8')
    cur = conn.cursor()
    cur.execute("insert into cityweatherinfo (cityname,mintemp,maxtemp,weather,ptime) values(%s,%s,%s,%s,%s)",(cityname,mintemp,maxtemp,weatherinfo,ptime))
    conn.commit()    
    cur.close()
    conn.close()
    


query_all_city_weather()
