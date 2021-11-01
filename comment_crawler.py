import requests
from datetime import datetime



def commentCatch (itemId, connector):
    cursor = connector.cursor()

    # API一次抓取6筆資料
    maxCommentCount = 6
    for page in range(0,3500,maxCommentCount):
        url = f"https://shopee.tw/api/v2/item/get_ratings?filter=0&flag=1&itemid={itemId}&limit=6&offset={page}&shopid=16927479&type=0"

        header = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
        }
        req = requests.get(url, headers = header)
        data = req.json()

        # 若後續無評論就無須繼續抓取
        if len(data['data']['ratings']) == 0:
            break
                
        for commentRow in range(0,len(data['data']['ratings'])):
            userId = data['data']['ratings'][commentRow]['userid']
            orderId = data['data']['ratings'][commentRow]['orderid']
            authorShopid = data['data']['ratings'][commentRow]['author_shopid']
            authorUsername = data['data']['ratings'][commentRow]['author_username']
            time = data['data']['ratings'][commentRow]['ctime']
            # 時間僅顯示年份及月份
            tureTime = datetime.fromtimestamp(time).strftime("%Y%m")
            comment = (data['data']['ratings'][commentRow]['comment'])
            # 替換評論裡的特殊字元符號
            if (type(comment) == str) :
                comment = comment.replace("'", "''").replace("\\", "")
            ratingStar = data['data']['ratings'][commentRow]['rating_star']
            productId = data['data']['ratings'][commentRow]['itemid']
            productName = data['data']['ratings'][commentRow]['product_items'][0]['model_name']
            cursor.execute("INSERT INTO product_Item(userid,orderid,shopid,username,time,comment,itemid,product_name,rating_star)VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}');".format(userId,orderId,authorShopid,authorUsername,tureTime,comment,productId,productName,ratingStar))
            connector.commit()

