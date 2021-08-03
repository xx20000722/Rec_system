# -*-coding:utf-8-*-

"""
    Author: Thinkgamer
    Desc:
        代码4-5 利用KNN算法实现性别预测
"""

import numpy as np

class KNN:
    def __init__(self, k):
        # k为最近邻个数
        self.K = k

    # 准备数据
    def createData(self):
        features = np.array([[180, 76], [158, 43], [176, 78], [161, 49]])
        labels = ["男", "女", "男", "女"]
        return features, labels

    # 数据进行Min-Max标准化
    def Normalization(self, data):
        maxs = np.max(data, axis=0)
        mins = np.min(data, axis=0)
        new_data = (data - mins) / (maxs - mins)
        return new_data, maxs, mins

    # 计算k近邻
    def classify(self, one, data, labels):
        # 计算新样本与数据集中每个样本之间的距离，这里距离采用的欧式距离计算方法
        differenceData = data - one
        squareData = (differenceData ** 2).sum(axis=1)
        distance = squareData ** 0.5
        sortDistanceIndex = distance.argsort()
        # 统计K近邻的label
        labelCount = dict()
        for i in range(self.K):
            label = labels[sortDistanceIndex[i]]
            labelCount.setdefault(label, 0)
            labelCount[label] += 1
        # 计算结果
        sortLabelCount = sorted(labelCount.items(), key=lambda x: x[1], reverse=True)
        print(sortLabelCount)
        return sortLabelCount[0][0]


if __name__ == "__main__":
    # 初始化类对象
    knn = KNN(3)
    # 创建数据集
    features, labels = knn.createData()
    # 数据集标准化
    new_data, maxs, mins = knn.Normalization(features)
    # 新数据的标准化
    one = np.array([176, 76])
    new_one = (one - mins) / (maxs - mins)
    # 计算新数据的性别
    result = knn.classify(new_one, new_data, labels)
    print("数据 {} 的预测性别为 : {}".format(one, result))
