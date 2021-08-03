# -*-coding:utf-8-*-
"""
    Author: Thinkgamer
    Desc:
        代码10-3：Scikit-learn中的数据拆分-Cross Validate
"""
from sklearn.model_selection import cross_validate
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier

# 使用Cross Validate演示交叉验证数据集的使用
def CrossValidate():
    # 加载乳癌肿瘤数据集
    X, y = datasets.load_breast_cancer(return_X_y=True)
    # 定义KNN模型
    clf = KNeighborsClassifier()

    # 定义需要输出的评价指标
    scoring = ['accuracy', 'f1']

    # 打印每次交叉验证的准确率
    score = cross_validate(clf, X, y, scoring=scoring, cv=5, return_train_score=True)
    print(score)

CrossValidate()