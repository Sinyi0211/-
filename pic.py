import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

# 建立圖形化資料
# 圖表顯示中文及負數
mpl.rcParams['font.sans-serif']='Arial Unicode MS'
mpl.rcParams['axes.unicode_minus']=False

# 開啟資料表1
df = pd.read_excel('/Users/apple/Desktop/2020totalSale.xlsx',sheet_name='sale')
x = df['month']
y1 = df['2020sale']
y2 = df['2019sale']
plt.plot(x,y1,label='2020sale',linewidth=5)
plt.plot(x,y2,label='2019sale',linewidth=5,color='r')
plt.title('總銷售額')
plt.legend()
plt.show()

# 開啟資料表2
df = pd.read_excel('/Users/apple/Desktop/2020totalSale.xlsx',sheet_name='sale')
y3 = df['YOY']
plt.plot(x,y3,label='YOY',linewidth=5,color='BLACK')
plt.title('年營收成長率')
plt.legend()
plt.show()

# 開啟資料表3
df = pd.read_excel('/Users/apple/Desktop/2020totalSale.xlsx',sheet_name='item')
x2 = df['類別']
y4 = df['銷售額']
plt.barh(x2, y4, label='2020類別排行',linewidth=5,color='green')
plt.title('2020銷售排行')
plt.show()

# 開啟資料表4
df = pd.read_excel('/Users/apple/Desktop/2020totalSale.xlsx',sheet_name='item')
labels='牛肉乾','肉紙','肉乾','肉條/肉角','肉鬆/魚鬆','其他','海產','堅果/果乾','蒟蒻','禮盒'
explode=(0.1,0,0,0,0,0,0,0,0)
x5=df['銷售額']
plt.pie(x5,labels=labels,autopct='%1.1f%%')
plt.axis("equal")
plt.title('2020類別佔比')
plt.show()


#x6=df['月份']
#y5=df['客單價']
#y6=df['平均值']


#plt.xlabel('銷售額')
#plt.ylabel('類別')
#plt.plot(x6, y6, label='平均值',linewidth=5,color='r')

# 建立折線圖
x=df['month']
columnName = ['牛肉乾', '肉紙', '肉乾', '肉條/肉角', '肉鬆/魚鬆', '其他', '海產', '堅果/果乾', '蒟蒻']
for row in columnName:
    plt.plot(x, df[row], label=row,linewidth=3)
plt.title('2020年商品銷售')

plt.legend()
plt.show()
