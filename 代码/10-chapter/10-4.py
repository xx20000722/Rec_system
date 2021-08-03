"""
    Author: Thinkgamer
    Desc:
        代码10-4 metrics使用示例
"""
import numpy as np
from sklearn import metrics

# AUC计算
def AUC():
    y = np.array([1,1,2,2])
    pred = np.array([0.1,0.4,0.35,0.8])
    # pos_label参数意义:这个pos_label的值被认为是阳性，而其他值被认为是阴性，然后pred给的是阳性的概率。
    fpr,tpr,thresholds = metrics.roc_curve(y,pred,pos_label=2)
    print(metrics.auc(fpr,tpr))
AUC()