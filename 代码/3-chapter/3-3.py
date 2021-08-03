# -*-coding:utf-8-*-

"""
    Author: Thinkgamer
    Desc:
        代码3-3  数据集介绍之Book-Crossings数据集
"""
import pandas as pd
import matplotlib.pyplot as plt

# 用来正常显示中文标签
plt.rcParams["font.sans-serif"] = ["SimHei"]
# 用来正常显示负号
plt.rcParams["axes.unicode_minus"] = False

def getRatingsMess(filePath):
    print("filePath is : {}".format(filePath))
    # drop 删除函数，这里删除第0行
    events = pd.read_table(filePath, header=0, sep="|").drop([0])
    print("数据的前5条为: \n{}".format(events.head(5)))
    print("events 的 key为: \n {}".format(events.keys()))
    # 因为原数据的原因，按|分割后 字段前后多了空格
    rateSer = events[" rating "].groupby(events[" rating "]).count()
    print("Event的值有: \n{}".format(rateSer))

    plt.axes(aspect=1)
    plt.pie(x=rateSer.values, labels=rateSer.keys(), autopct="%3.1f %%")
    plt.legend(bbox_to_anchor=(1.0, 1.0))
    plt.show()

if __name__ == "__main__":
    getRatingsMess("../data/foursquare-2013/ratings.dat")
