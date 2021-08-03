# -*-coding:utf-8-*-

"""
    Author: Thinkgamer
    Desc:
        代码4-11 sk-learn中聚类效果评估
"""

from sklearn import metrics

labels_true = [0, 0, 0, 1, 1, 1]
labels_pred = [0, 0, 1, 1, 2, 2]

# 以下预测结果均是  值越大 预测结果与真实结果越吻合

# 兰德系数
print(metrics.adjusted_rand_score(labels_true, labels_pred))
# 互信息
print(metrics.adjusted_mutual_info_score(labels_true, labels_pred))

# 同质性
print(metrics.homogeneity_score(labels_true, labels_pred))
# 完整性
print(metrics.completeness_score(labels_true, labels_pred))
# 同质性与完整性的调和平均
print(metrics.v_measure_score(labels_true, labels_pred) )

# FMI
print( metrics.fowlkes_mallows_score(labels_true, labels_pred) )
