# -*-coding:utf-8-*-

"""
    Author: Thinkgamer
    Desc:
        代码 4-4 相似度计算
"""
from numpy import *

# 欧式距离
def EuclideanDistance(a,b):
    return sqrt( (a[0]-b[0])**2 + (a[1]-b[1])**2 )

print('a,b 二维欧式距离为：',EuclideanDistance((1,1),(2,2)))

def ManhattanDistance(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])

print('a,b 二维曼哈顿距离为：', ManhattanDistance((1,1),(2,2)))

def ChebyshevDistance(a,b):
    return max( abs(a[0]-b[0]), abs(a[1]-b[1]))

print('a,b二维切比雪夫距离：' , ChebyshevDistance((1,2),(3,4)))

def CosineSimilarity(a,b):
    cos = (a[0]*b[0]+a[1]*b[1]) / (sqrt(a[0]**2 + a[1]**2) * sqrt(b[0]**2 + b[1]**2) )

    return cos
print('a,b 二维夹角余弦距离：',CosineSimilarity((1,1),(2,2)))

def JaccardSimilarityCoefficient(a,b):
    set_a = set(a)
    set_b = set(b)
    dis = float(len(set_a & set_b)  )/ len(set_a | set_b)
    return dis

print('a,b 杰卡德相似系数：', JaccardSimilarityCoefficient((1,2,3),(2,3,4)))

def JaccardSimilarityDistance(a,b):
    set_a = set(a)
    set_b = set(b)
    dis = float(len( (set_a | set_b) - (set_a & set_b) ) )/ len(set_a | set_b)
    return dis

print('a,b 杰卡德距离：', JaccardSimilarityDistance((1,2,3),(2,3,4)))