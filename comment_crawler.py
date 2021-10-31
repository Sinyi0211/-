import requests
from bs4 import BeautifulSoup
import pandas
import json
import pymysql
from datetime import datetime


def commentCatch (itemId, connector):
    cursor = connector.cursor()
# API串接抓取留言評論
    maxCommentCount = 6
    for page in range(0,3500,maxCommentCount):
        url = f"https://shopee.tw/api/v2/item/get_ratings?filter=0&flag=1&itemid=197260285&limit=6&offset={page}&shopid=16927479&type=0"

        header = {
            # 'if-none-match-': '55b03-5377a85c53a70439df5e94b50fd0c9ee',
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
        }
        req = requests.get(url, headers = header)
        data = req.json()

        if len(data['data']['ratings']) == 0:
            break
#
        for commentRow in range(0,maxCommentCount):
            userId = data['data']['ratings'][commentRow]['userid']
            orderId = data['data']['ratings'][commentRow]['orderid']
            authorShopid = data['data']['ratings'][commentRow]['author_shopid']
            authorUsername = data['data']['ratings'][commentRow]['author_username']
            time = data['data']['ratings'][commentRow]['ctime']
            tureTime = datetime.fromtimestamp(time).strftime("%Y%m")
            # "'{}'".format(data['data']['ratings'][commentRow]['comment'])
            comment = (data['data']['ratings'][commentRow]['comment'])
            if (type(comment) == str) :
                comment = comment.replace("'", "''")
            #comment = (data['data']['ratings'][commentRow]['comment']).replace("'", "''")
            # formatComment = comment.replace('▽', ' ')
            ratingStar = data['data']['ratings'][commentRow]['rating_star']
            productId = data['data']['ratings'][commentRow]['itemid']
            productName = data['data']['ratings'][commentRow]['product_items'][0]['model_name']
            cursor.execute("INSERT INTO product_Item(userid,orderid,shopid,username,time,comment,itemid,product_name,rating_star)VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}');".format(userId,orderId,authorShopid,authorUsername,tureTime,comment,productId,productName,ratingStar))
            connector.commit()
