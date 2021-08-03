"""
    Author: Thinkgamer
    Desc:
        代码10-4 metrics使用示例-类预测分类准确度
"""

from sklearn import metrics
from sklearn.metrics import confusion_matrix
y_true = [0, 1, 1, 0, 0, 1, 0, 0, 0, 0]
y_pred = [0, 0, 1, 1, 0, 1, 1, 0, 1, 1]

# 混淆矩阵 横为label 纵为预测值
print("混淆矩阵:")
print(confusion_matrix(y_true, y_pred))
# AUC
print("AUC is {}".format(metrics.roc_auc_score(y_true, y_pred)))
# 精确率
print("Precision is {}".format(metrics.precision_score(y_true, y_pred)))
# 召回率
print("Recall is {}".format(metrics.recall_score(y_true, y_pred)))
# f1值
print("F1 is {}".format(metrics.f1_score(y_true, y_pred)))

from sklearn.metrics import classification_report
# 分类报告
print("分类报告：")
print(classification_report(y_true, y_pred))