# -*-coding:utf-8-*-

"""
    Author: Thinkgamer
    Desc:
        代码3-4  数据集介绍之retailrocket数据集
"""

import pandas as pd
import matplotlib.pyplot as plt

# 用来正常显示中文标签
plt.rcParams["font.sans-serif"] = ["SimHei"]
# 用来正常显示负号
plt.rcParams["axes.unicode_minus"] = False

def getEventsMess(filePath):
    print("filePath is : {}".format(filePath))
    events = pd.read_csv(filePath, header=0, encoding="utf-8")
    print("数据的前5条为: \n{}".format(events.head(5)))
    print("数据总条数为: \n{}".format(events.count()))
    eventSer = events["event"].groupby(events["event"]).count()
    print("Event的值有: \n{}".format(eventSer))

    plt.axes(aspect=1)
    plt.pie(x=eventSer.values, labels=eventSer.keys(), autopct="%3.1f %%")
    plt.legend(bbox_to_anchor=(1.0, 1.0))
    plt.show()

if __name__ == "__main__":
    getEventsMess("../data/retailrocket/events.csv")
