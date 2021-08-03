# -*-coding:utf-8-*-

"""
    Author: Thinkgamer
    Desc:
        代码3-2  数据集介绍之Book-Crossings数据集
"""
import pandas as pd
import matplotlib.pyplot as plt

# 用来正常显示中文标签
plt.rcParams["font.sans-serif"] = ["SimHei"]
# 用来正常显示负号
plt.rcParams["axes.unicode_minus"] = False

def getRatings(file_path):
    print("filePath is '{}'".format(file_path))
    ratings = pd.read_table(
        file_path,
        header=0,
        sep=";",
        encoding="ISO-8859-1"
    )

    print("前5条数据为: \n {}".format(ratings.head(5)))
    print("总的数据记录条数为: \n {}".format(ratings.count()))
    print("用户对图书的评分范围为: <{},{}>\n"
          .format(ratings["Book-Rating"].min(), ratings["Book-Rating"].max()))

    rateSer = ratings["Book-Rating"].groupby(ratings["Book-Rating"]).count()
    plt.bar(rateSer.keys(), rateSer.values, fc="r", tick_label=rateSer.keys())
    for x, y in zip(rateSer.keys(), rateSer.values):
        plt.text(x, y + 1, "%.0f" % y, ha="center", va="bottom", fontsize=9)
    plt.xlabel("用户评分")
    plt.ylabel("评分对应的人数")
    plt.title("每种评分下对应的人数统计图")
    plt.show()


def getBooksMess(file_path):
    print("filePath is '{}''".format(file_path))
    books = pd.read_table(
        file_path,
        header=0,
        sep=";",
        encoding="ISO-8859-1"
    )
    print("总的数据记录条数为: \n{}".format(books.count()))

    # # 出版时间分布
    # yearsSer = books["Year-Of-Publication"].groupby(books["Year-Of-Publication"]).count()
    # print(yearsSer)


def getUsersMess(file_path):
    print("filePath is '{}''".format(file_path))
    users = pd.read_table(
        file_path,
        header=0,
        sep=";",
        encoding="ISO-8859-1"
    )
    print("前5条数据为: \n {}".format(users.head(5)))
    print("总的数据记录条数为: \n {}".format(users.count()))
    print("年龄的最大最小值: <{},{}>"
          .format(users["Age"].min(), users["Age"].max()))


if __name__ == "__main__":
    # getRatings("../data/bookcrossings/BX-Book-Ratings.csv")
    getBooksMess("../data/bookcrossings/BX-Books.csv")
    # getUsersMess("../data/bookcrossings/BX-Users.csv")
