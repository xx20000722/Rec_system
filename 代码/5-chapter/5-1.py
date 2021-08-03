# coding: utf-8 -*-
"""
    Author: Thinkgamer
    Desc:
        代码5-1: 对手机属性进行特征建模
"""

# 对iPhone5的离散型属性（颜色和内存）进行one-hot编码（1）
from sklearn import preprocessing
onehot = preprocessing.OneHotEncoder()
# 训练数据，所有特征的可能组合
onehot.fit([[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]])
print(onehot.transform([[0,0]]).toarray())


# 对iPhone5的离散型属性（颜色和内存）进行one-hot编码（2）
onehot.fit([[0, 0], [1, 1], [2, 2]])
print(onehot.transform([[0, 0]]).toarray())


# 对iPhone5的连续型属性（尺寸和价格）进行0-1归一化处理
def MaxMinNormalization(x, Max, Min):
    x = (x - Min) / (Max - Min)
    return x

# 尺寸数组
sizes = [4, 4.7, 5.5]
# 价格数组
prices = [1358, 2788, 3656]
size_min, size_max = min(sizes), max(sizes)
price_min, price_max = min(prices), max(prices)

# 求iphone 5，iphone 6，iphone 6sp的尺寸归一化
nor_size = []
for size in sizes:
    nor_size.append(round(MaxMinNormalization(size, size_max, size_min), 4))
print("尺寸归一化为：%s" % nor_size)

# 求iphone 5，iphone 6，iphone 6sp的价格归一化
nor_price = []
for price in prices:
    nor_price.append(round(MaxMinNormalization(price, price_max, price_min), 4))
print("价格归一化为：%s" % nor_price)
