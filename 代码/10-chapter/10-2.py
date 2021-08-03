# -*-coding:utf-8-*-
"""
    Author: Thinkgamer
    Desc:
        代码10-2： Scikit-learn中的数据拆分-KFold
"""
from sklearn.model_selection import KFold
import numpy as np

# 以生成器的方式产生每次需要的训练集和测试集
def KFoldTest():
    X = np.random.randint(1, 10, 20)
    # n_splits K折交叉验证
    kf = KFold(n_splits=5)
    # 返回的数据的下标
    i = 1
    for train_index, test_index in kf.split(X):
        print("第 {} 次：".format(i))
        print("train 数据为：{}".format(train_index))
        print("test 数据为：{}".format(test_index))
        i += 1


# 交叉验证
KFoldTest()
