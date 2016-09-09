import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='',db='citycode',charset='UTF8')
cur = conn.cursor()
cur.execute("select citycode, cityname from citycode order by citycode")
for i in cur:
    print(i)
    print(i[0])
cur.close()
conn.close()
