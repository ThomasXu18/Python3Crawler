#-*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from urllib import parse
import requests
import csv
import codecs

# 此处加载的是北京的房源
url = "http://bj.58.com/pinpaigongyu/pn/{page}/?minprice=2000_4000"

# 已完成的页数序号 初始为0
page = 0

# 使用codecs打开文件并制定编码为utf8
csv_file = codecs.open("rent.csv", "w", "utf-8")
csv_writer = csv.writer(csv_file, delimiter=',')

while True:
    page += 1
    print("fetch: ", url.format(page=page))
    response = requests.get(url.format(page=page))
    html = BeautifulSoup(response.text, "html.parser")
    house_list = html.select(".list > li")

    if not house_list:
        break

    for house in house_list:
        house_title = house.select("h2")[0].string.strip("【合租】").strip("【整租】")
        house_url = parse.urljoin(url, house.select("a")[0]["href"])
        house_info_list = house_title.split()


        if "公寓" in house_info_list[1] or "青年社区" in house_info_list[1]:
            house_location = house_info_list[0]
        else:
            house_location = house_info_list[1]

        house_money = house.select(".money")[0].select("b")[0].string
        csv_writer.writerow([house_title, house_location, house_money, house_url])
        

csv_file.close()
