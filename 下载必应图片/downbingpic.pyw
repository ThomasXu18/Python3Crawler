# -*- coding:utf-8 -*-

import re
import requests
import time
import os
import sys
import subprocess
from PIL import Image
import win32api, win32con, win32gui


#Ping cn.bing.com  online--0 
def my_ping():
    # return1 = os.system('ping -n 2 -w 1 cn.bing.com')
    ret = subprocess.call("ping -n 1 -w 1 cn.bing.com", shell = True)
    print(ret)
    return ret
    
def set_wallpaper_from_bmp(bmp_path):  
    #打开指定注册表路径  
    reg_key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)  
    #最后的参数:2拉伸,0居中,6适应,10填充,0平铺  
    win32api.RegSetValueEx(reg_key, "WallpaperStyle", 0, win32con.REG_SZ, "2")  
    #最后的参数:1表示平铺,拉伸居中等都是0  
    win32api.RegSetValueEx(reg_key, "TileWallpaper", 0, win32con.REG_SZ, "0")  
    #刷新桌面  
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,bmp_path, win32con.SPIF_SENDWININICHANGE)  
  
def set_wallpaper(img_path):  
    #把图片格式统一转换成bmp格式,并放在源图片的同一目录  
    img_dir = os.path.dirname(img_path)  
    bmpImage = Image.open(img_path)  
    new_bmp_path = os.path.join(img_dir,'wallpaper.bmp')  
    bmpImage.save(new_bmp_path, "BMP")  
    set_wallpaper_from_bmp(new_bmp_path)

#下载图片
def downImg():
    date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    path = get_cur_file_dir() 
    path = path +"\\" + date + '.jpg'
    if os.path.isfile(path):
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

        fp = open(path, 'wb')
        fp.write(pic.content)
        fp.close()
    return path

#获取脚本文件的当前路径   
def get_cur_file_dir():
    path = sys.path[0]
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)

while(my_ping() != 0):
    time.sleep(10)
set_wallpaper(downImg())
#print(get_cur_file_dir())
