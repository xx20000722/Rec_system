# -*-coding:utf-8-*-

"""
    Author: Thinkgamer
    Desc:
        代码4-8 sk-learn中分类器效果评估
"""
from sklearn.metrics import classification_report
y_true = [0, 1, 2, 2, 2]
y_pred = [0, 0, 2, 2, 1]
target_names = ['class0', 'class1', 'class2']
print(classification_report(y_true, y_pred, target_names=target_names))
