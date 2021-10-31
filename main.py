import requests
from bs4 import BeautifulSoup
import pandas
import json
import pymysql
from comment_crawler import commentCatch

# 資料庫連線
conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='@@qaz0211',db='DDD',charset='UTF8MB4') 
cursor = conn.cursor()

# 建立主資料表
cursor.execute("CREATE TABLE product_All(itemid VARCHAR(255),name VARCHAR(255), price INTEGER(99), historical_sold VARCHAR(255),liked_count VARCHAR(255),rating_star INTEGER(99))")

# 建立留言評論資料表
cursor.execute("CREATE TABLE product_Item(userid VARCHAR(255),orderid VARCHAR(255),shopid VARCHAR(255),username VARCHAR(255),time VARCHAR(255),comment NVARCHAR(9999),itemid VARCHAR(255),product_name VARCHAR(255),rating_star int(10))")

# 修改資料表字元格式
sql = "ALTER TABLE product_Item CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
sql2 ="ALTER TABLE product_All CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 
cursor.execute(sql)
cursor.execute(sql2)
conn.commit()

# API一次抓取30筆資料,最多打5次API
maxCatchCount = 30
for pagination in range(0,maxCatchCount*5,maxCatchCount):
    url = f"https://shopee.tw/api/v4/search/search_items?by=pop&entry_point=ShopBySearch&limit=30&match_id=16927479&newest={pagination}&order=desc&page_type=shop&scenario=PAGE_OTHERS&version=2"

    header = {
        'if-none-match-': '55b03-6d87c8daaec8704cfeaed125531c1672',
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    }
    req = requests.get(url, headers = header)
    data = req.json()
# 將所需欄位存取至資料表中
    for item in range(0,maxCatchCount):
        itemId = data['items'][item]['item_basic']['itemid']
        name = data['items'][item]['item_basic']['name']
        price = int(data['items'][item]['item_basic']['price'])/100000
        historicalSold = data['items'][item]['item_basic']['historical_sold']
        likedCount = data['items'][item]['item_basic']['liked_count']
        ratingStar = round(data['items'][item]['item_basic']['item_rating']['rating_star'],2)
        cursor.execute("INSERT INTO product_All(itemid,name,price,historical_sold,liked_count,rating_star)VALUES('{0}','{1}','{2}','{3}','{4}','{5}');".format(itemId,name,price,historicalSold,likedCount,ratingStar))
        conn.commit()
        commentCatch(itemId, conn)

cursor.close() 
conn.close()