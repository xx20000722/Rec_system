# -*-coding:utf-8-*-
"""
    Author: Thinkgamer
    Desc:
        实例20：实现一个“增加时间衰减函数的协同过滤算法”
        代码7-3：增加时间衰减函数的协同过滤算法实现 UserCF 数据集依旧使用第五章中实例使用的数据
"""

import math, json, os, random
from sklearn.model_selection import train_test_split

class ItemBasedCF:
    # 初始化函数,max_data 表示数据集中评分时间的最大值，即初始化时间衰减函数中的 t0
    def __init__(self,datafile):
        self.alpha = 0.5
        self.beta = 0.8
        self.datafile = datafile
        self.train, self.test, self.max_data = self.loadData()

        self.items_sim = self.ItemSimilarityBest()

    # 加载数据集，并拆分成训练集和测试集
    def loadData(self):
        print("Start load Data and Split data ...")
        data = list()
        max_data = 0
        for line in open(self.datafile):
            userid, itemid, record, timestamp = line.split("::")
            data.append((userid, itemid, int(record), int(timestamp)))
            if int(timestamp) > max_data:
                max_data = int(timestamp)
        # 调用sklearn中的train_test_split拆分训练集和测试集
        train_list, test_list = train_test_split(data, test_size=0.1, random_state=40)
        # 将train 和 test 转化为字典格式方便调用
        train_dict = self.transform(train_list)
        test_dict = self.transform(test_list)
        return train_dict, test_dict, max_data

    # 将list转化为dict
    def transform(self, data):
        data_dict = dict()
        for user, item, record, timestamp in data:
            data_dict.setdefault(user, {}).setdefault(item, {})
            data_dict[user][item]["rate"] = record
            data_dict[user][item]["time"] = timestamp
        return data_dict

    # 计算物品之间的相似度
    def ItemSimilarityBest(self):
        print("开始计算物品之间的相似度")
        if os.path.exists("data/item_sim.json"):
            print("从文件加载 ...")
            itemSim = json.load(open("data/item_sim.json", "r"))
        else:
            itemSim = dict()
            item_eval_by_user_count = dict()  # 得到每个物品有多少用户产生过行为
            count = dict()  # 共现矩阵
            for user, items in self.train.items():
                # print("user is {}".format(user))
                for i in items.keys():
                    item_eval_by_user_count.setdefault(i, 0)
                    if self.train[str(user)][i]["rate"] > 0.0:
                        item_eval_by_user_count[i] += 1
                    for j in items.keys():
                        count.setdefault(i, {}).setdefault(j, 0)
                        if self.train[str(user)][i]["rate"] > 0.0 and self.train[str(user)][j]["rate"] > 0.0 and i != j:
                            count[i][j] += 1 * 1 / ( 1+ self.alpha * abs(self.train[user][i]["time"]-self.train[user][i]["time"]) / (24*60*60) )
            # 共现矩阵 -> 相似度矩阵
            for i, related_items in count.items():
                itemSim.setdefault(i, {})
                for j, num in related_items.items():
                    itemSim[i].setdefault(j, 0)
                    itemSim[i][j] = num / math.sqrt(item_eval_by_user_count[i] * item_eval_by_user_count[j])
        json.dump(itemSim, open('data/item_sim.json', 'w'))
        return itemSim

    """
        为用户进行推荐
            user: 用户
            k: k个临近物品
            nitems: 总共返回n个物品
    """
    def recommend(self, user, k=8, nitems=40):
        result = dict()
        u_items = self.train.get(user, {})
        for i, rate_time in u_items.items():
            for j, wj in sorted(self.items_sim[i].items(), key=lambda x: x[1], reverse=True)[0:k]:
                if j in u_items:
                    continue
                result.setdefault(j, 0)
                # result[j] += rate_time["rate"] * wj
                result[j] += rate_time["rate"] * wj * 1/(1+ self.beta * ( self.max_data - abs(rate_time["time"]) ) )

        return dict(sorted(result.items(), key=lambda x: x[1], reverse=True)[0:nitems])

    # 计算准确率,由于测试集数据较大，这里选取10个用户进行测试，如果条件允许的话可以使用全量用户进行测试
    def precision(self, k=8,nitems=10):
        hit = 0
        precision = 0
        print(len(self.test.keys()))
        for user in random.sample( self.test.keys(), 10):
            print(user)
            u_items = self.test.get(user, {})
            result = self.recommend(user, k=k, nitems=nitems)
            for item, rate in result.items():
                if item in u_items:
                    hit += 1
            precision += nitems
        return hit / (precision * 1.0)


if __name__ == "__main__":
    ib = ItemBasedCF("../data/ml-1m/ratings.dat")
    result = ib.recommend("1")
    print("user '1' recommend result is {} ".format(result))

    precision = ib.precision()
    print("precision is {}".format(precision))

