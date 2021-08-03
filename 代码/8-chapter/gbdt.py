# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 16:26:53 2021

@author: Yang Ming
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import metrics
from sklearn.model_selection import GridSearchCV

import matplotlib.pylab as plt

train = pd.read_csv('./data/train_modified.csv')
target='Disbursed' # Disbursed的值就是二元分类的输出
IDcol = 'ID'
train['Disbursed'].value_counts() 

x_columns = [x for x in train.columns if x not in [target, IDcol]]
X = train[x_columns]
y = train['Disbursed']

gbm0 = GradientBoostingClassifier(random_state=10)
gbm0.fit(X,y)
y_pred = gbm0.predict(X)
y_predprob = gbm0.predict_proba(X)[:,1]
print ("Accuracy : %.4g" % metrics.accuracy_score(y.values, y_pred))
print ("AUC Score (Train): %f" % metrics.roc_auc_score(y, y_predprob))

#选择基学习器数目
#首先我们从步长(learning rate)和迭代次数(n_estimators)入手
#这里，我们将步长初始值设置为0.1。对于迭代次数进行网格搜索如下
param_test1 = {'n_estimators':range(20,81,10)}

gsearch1 = GridSearchCV(estimator = GradientBoostingClassifier(learning_rate=0.1, min_samples_split=300,
                        min_samples_leaf=20,max_depth=8,max_features='sqrt', subsample=0.8,random_state=2019),
                        param_grid = param_test1, scoring='roc_auc',iid=False,cv=5)
gsearch1.fit(X, y)

print(gsearch1.cv_results_['mean_test_score'], gsearch1.best_params_, gsearch1.best_score_)

#首先我们对决策树最大深度max_depth和内部节点再划分所需最小样本数min_samples_split进行网格搜索

param_test2 = {'max_depth':range(3,14,2),
               'min_samples_split':range(100,801,200)}

gsearch2 = GridSearchCV(estimator = GradientBoostingClassifier(learning_rate=0.1, n_estimators=60, min_samples_leaf=20,
                        max_features='sqrt', subsample=0.8, random_state=2019),
                        param_grid = param_test2, scoring='roc_auc',iid=False, cv=5)

gsearch2.fit(X, y)

print(gsearch2.cv_results_['mean_test_score'], gsearch2.best_params_, gsearch2.best_score_)

#选择min_samples_split和min_samples_leaf
param_test3 = {'min_samples_split':range(800,1900,200),
               'min_samples_leaf':range(60,101,10)}

gsearch3 = GridSearchCV(estimator = GradientBoostingClassifier(learning_rate=0.1, n_estimators=60,max_depth=7,
                        max_features='sqrt', subsample=0.8, random_state=2019),
                        param_grid = param_test3, scoring='roc_auc',iid=False, cv=5, verbose=3)

gsearch3.fit(X, y)

print(gsearch3.cv_results_['mean_test_score'], gsearch3.best_params_, gsearch3.best_score_)

#调了这么多参数了，终于可以都放到GBDT类里面去看看效果了。现在我们用新参数拟合数据
gbm1 = GradientBoostingClassifier(learning_rate=0.1, n_estimators=60,max_depth=7, min_samples_leaf =60,
                                min_samples_split =1200, max_features='sqrt', subsample=0.8, random_state=2019)
x_train,y_train=X,y
gbm1.fit(x_train, y_train)

print("tr-accuracy: %.4g" % metrics.accuracy_score(y_train.values, gbm1.predict(x_train)))      # Accuracy : 0.9841
print("tr-AUC: %f" % metrics.roc_auc_score(y_train, gbm1.predict_proba(x_train)[:, 1]))      # AUC Score (Train): 0.907378

#选择max_features：特征采样
param_test4 = {'max_features':range(7,20,2)}

gsearch4 = GridSearchCV(estimator = GradientBoostingClassifier(learning_rate=0.1, n_estimators=60,max_depth=7, min_samples_leaf =60,
                        min_samples_split =1200, subsample=0.8, random_state=2019),
                        param_grid = param_test4, scoring='roc_auc',iid=False, cv=5)
gsearch4.fit(X, y)

print(gsearch4.cv_results_['mean_test_score'], gsearch4.best_params_, gsearch4.best_score_)

#选择subsample：样本采样
param_test5 = {'subsample':[0.6,0.7,0.75,0.8,0.85,0.9]}

gsearch5 = GridSearchCV(estimator = GradientBoostingClassifier(learning_rate=0.1, n_estimators=60,max_depth=7, min_samples_leaf =60,
                        min_samples_split =1200, max_features=9, random_state=2019),
                        param_grid = param_test5, scoring='roc_auc',iid=False, cv=5)
gsearch5.fit(X, y)

print(gsearch5.cv_results_['mean_test_score'], gsearch5.best_params_, gsearch5.best_score_)

#现在我们基本已经得到所有调优的参数结果。放到GBDT里面去看看效果
gbm2 = GradientBoostingClassifier(learning_rate=0.1, n_estimators=60,max_depth=7, min_samples_leaf =60,
               min_samples_split =1200, max_features=9, subsample=0.7, random_state=2019)
gbm2.fit(x_train, y_train)

print("tr-accuracy: %.4g" % metrics.accuracy_score(y_train.values, gbm2.predict(x_train)))      # Accuracy : 0.9841
print("tr-AUC: %f" % metrics.roc_auc_score(y_train, gbm2.predict_proba(x_train)[:, 1]))      # AUC Score (Train): 0.898388

#提高拟合能力和泛化能力
gbm3 = GradientBoostingClassifier(learning_rate=0.05, n_estimators=120,max_depth=7, min_samples_leaf =60,
               min_samples_split =1200, max_features=9, subsample=0.7, random_state=2019)
gbm3.fit(x_train, y_train)

print("tr-accuracy: %.4g" % metrics.accuracy_score(y_train.values, gbm3.predict(x_train)))      # Accuracy : 0.9841
print("tr-AUC: %f" % metrics.roc_auc_score(y_train, gbm3.predict_proba(x_train)[:, 1]))      # AUC Score (Train): 0.904004

#继续将步长缩小5倍，最大迭代次数增加5倍，继续拟合我们的模型
gbm4 = GradientBoostingClassifier(learning_rate=0.01, n_estimators=600,max_depth=7, min_samples_leaf =60,
               min_samples_split =1200, max_features=9, subsample=0.7, random_state=2019)
gbm4.fit(x_train, y_train)

print("tr-accuracy: %.4g" %  metrics.accuracy_score(y_train.values, gbm4.predict(x_train)))      # Accuracy : 0.9841
print("tr-AUC: %f" %  metrics.roc_auc_score(y_train, gbm4.predict_proba(x_train)[:, 1]))      # AUC Score (Train): 0.907238

def plot_feature_importance(dataset, model_bst):
    list_feature_name = list(dataset.columns[:])
    # list_feature_importance = list(model_bst.feature_importance(importance_type='split', iteration=-1))
    list_feature_importance = list(model_bst.feature_importances_)
    dataframe_feature_importance = pd.DataFrame(
        {'feature_name': list_feature_name, 'importance': list_feature_importance})
    dataframe_feature_importance20 = dataframe_feature_importance.sort_values(by='importance', ascending=False)[:20]
    print(dataframe_feature_importance20)
    x = range(len(dataframe_feature_importance20['feature_name']))
    plt.xticks(x, dataframe_feature_importance20['feature_name'], rotation=90, fontsize=8)
    plt.plot(x, dataframe_feature_importance20['importance'])
    plt.xlabel("Feature name")
    plt.ylabel("Importance")
    plt.title("The importance of features")
    plt.show()


gbm6 = GradientBoostingClassifier(learning_rate=0.05, n_estimators=160,max_depth=7, min_samples_leaf =60,
                   min_samples_split =1200, max_features=9, subsample=0.7, random_state=2019)

gbm6.fit(x_train, y_train)

plot_feature_importance(x_train, gbm6)