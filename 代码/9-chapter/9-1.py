# -*-coding:utf-8-*-
"""
    Author: Thinkgamer
    Desc:
        代码9-1 实例25: 分析BookCrossing数据集中的共性特征偏好
"""
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

class UserShow:
    def __init__(self):
        self.file_user = "../data/bookcrossings/BX-Users.csv"
        self.file_book = "../data/bookcrossings/BX-Books.csv"
        self.file_rate = "../data/bookcrossings/BX-Book-Ratings.csv"
        self.user_mess = self.loadUserData()
        self.book_mess = self.loadBookMess()
        self.user_book = self.loadUserBook()

    # 加载用户信息数据集
    def loadUserData(self):
        user_mess = dict()
        for line in open(self.file_user, "r", encoding="ISO-8859-1"):
            if line.startswith("\"User-ID\""): continue
            # 行的列值以";分隔，有三列，过滤掉不符的数据
            # 因为Location字段中存在; 所以这里以";分割数据
            if len(line.split("\";")) != 3: continue
            # 去除数据中的空格
            line = line.strip().replace(" ", "")
            # 去掉数据中的 "
            userid, addr, age = [one.replace("\"", "") for one in line.split("\";")]
            # 这里假设年龄的合理范围为(1,120)
            if age == "NULL" or int(age) not in range(1, 120): continue
            # 这里将年龄处理成年龄段 0-9=>0,10-19=>1,....
            # age_split = int(int(age) / 10)
            user_mess.setdefault(userid, {})
            user_mess[userid]["age"] = int(age)
            # Location 分为三级，以逗号分隔，对应国,州,市
            if len(addr.split(",")) < 3: continue
            city, province, country = addr.split(",")[-3:]
            user_mess[userid]["country"] = country
            user_mess[userid]["province"] = province
            user_mess[userid]["city"] = city
        return user_mess

    # 加载图书编号和名字的对应关系
    def loadBookMess(self):
        book_mess = dict()
        for line in open(self.file_book, "r", encoding="ISO-8859-1"):
            if line.startswith("\"ISBN\""): continue
            isbn, book_name = line.replace("\"", "").split(";")[:2]
            book_mess[isbn] = book_name
        return book_mess

    # 获取每个用户评分大于5的图书信息
    def loadUserBook(self):
        user_book = dict()
        for line in open(self.file_rate, "r", encoding="ISO-8859-1"):
            if line.startswith("\"User-ID\""): continue
            uid, isbn, rate = line.strip().replace("\"", "").split(";")
            user_book.setdefault(uid, list())
            if int(rate) > 5:
                user_book[uid].append(isbn)
        return user_book

    def show(self, X, Y, X_label, Y_label="数目"):
        # X、Y轴说明
        plt.xlabel(X_label)
        plt.ylabel(Y_label)
        # 保证X轴数据按照传入的X顺序排列
        plt.xticks(np.arange(len(X)), X, rotation=90)
        # 在坐标轴上显示X值对应的Y值
        for a, b in zip(np.arange(len(X)), Y):
            plt.text(a, b+2000, b, rotation=45)
        plt.bar(np.arange(len(X)), Y)
        plt.show()

    # 不同年龄段的用户人数统计
    def diffAge(self):
        age_user = dict()
        for key in self.user_mess.keys():
            age_split = int(int(self.user_mess[key]["age"]) / 10)
            age_user.setdefault(age_split, 0)
            age_user[age_split] += 1
        age_user_sort = sorted(age_user.items(), key=lambda x: x[0], reverse=False)
        X = [x[0] for x in age_user_sort]
        Y = [x[1] for x in age_user_sort]
        print(age_user_sort)
        self.show(X, Y, X_label="用户年龄段")

    # 美国不同州下的用户分布 top 20
    def diffPro(self):
        pro_user = dict()
        for key in self.user_mess.keys():
            if "province" in self.user_mess[key].keys() and self.user_mess[key]["province"] != "n/a":
                pro_user.setdefault(self.user_mess[key]["province"], 0)
                pro_user[self.user_mess[key]["province"]] += 1

        pro_user_sort = sorted(pro_user.items(), key=lambda x: x[1], reverse=True)[:20]
        X = [x[0] for x in pro_user_sort]
        Y = [x[1] for x in pro_user_sort]
        print(pro_user_sort)
        self.show(X, Y, X_label="用户所处州")


    # 获取不同年龄人群的评分图书分布
    # 这里选择20-30岁和大于50岁的用户进行分析
    def diffUserAge(self):
        age_books = dict()
        age_books.setdefault(1,dict())
        age_books.setdefault(2,dict())
        for key in self.user_mess.keys():
            if "country" not in self.user_mess[key].keys(): continue
            if key not in self.user_book.keys(): continue
            if int(self.user_mess[key]["age"]) in range(0,30):
                for book in self.user_book[key]:
                    if book not in self.book_mess.keys(): continue
                    age_books[1].setdefault(book,0)
                    age_books[1][book]+=1
            if int(self.user_mess[key]["age"]) in range(50,120):
                for book in self.user_book[key]:
                    if book not in self.book_mess.keys(): continue
                    age_books[2].setdefault(book,0)
                    age_books[2][book]+=1
        print("用户年龄段在30岁以下的用户偏好的共性图书top 5：")
        for one in sorted(age_books[1].items(), key=lambda x: x[1], reverse=True)[:10]:
            print(self.book_mess[one[0]])

        print("用户年龄段在50岁以上的用户偏好的共性图书top 5：")
        for one in sorted(age_books[2].items(), key=lambda x: x[1], reverse=True)[:10]:
            print(self.book_mess[one[0]])

if __name__ == "__main__":
    ushow = UserShow()
    # ushow.diffAge()
    # ushow.diffPro()
    ushow.diffUserAge()
