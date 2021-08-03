# -*-coding:utf-8-*-
"""
    Author: Thinkgamer
    Desc:
        代码10-1: Scikit-learn中的数据拆分-train_test_split
"""
from sklearn.model_selection import train_test_split
from sklearn import datasets
import pandas as pd

# 演示model_select中的train_test_split
def TrainTestSplit(is_stratify):
    # 加载鸢尾花数据集
    X, y = datasets.load_iris(return_X_y=True)
    # 进行数据集拆分
    if is_stratify:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, stratify=y, random_state=10
        )
    else:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, stratify=None, random_state=10
        )
    print("X_train 的数据维度为：{}".format(X_train.shape))
    print("X_test 的数据维度为：{}".format(X_test.shape))
    print("y_train 的数据维度为：{}".format(y_train.shape))
    print("y_test 的数据维度为：{}".format(y_test.shape))

    # 打印出训练和测试集中的各类别类目情况
    print("y_train中各类目对应的次数统计为：\n{}".format(pd.value_counts(y_train)))
    print("y_test中各类目对应的次数统计为：\n{}".format(pd.value_counts(y_test)))


# 调用train_test_split
print("数据不分层：")
TrainTestSplit(is_stratify=False)  # 不分层
print("\n数据分层：")
TrainTestSplit(is_stratify=True)  # 分层
