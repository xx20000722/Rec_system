# -*-coding:utf-8-*-
"""
    Author: Thinkgamer
    Desc:
      代码8-2：Sigmoid函数演示
"""

import math
import matplotlib.pyplot as plt

def sigmoid(x):
    return 1 / (1 + math.exp(-x))


# python2 中range生成的是一个数组，py3中生成的是一个迭代器，可以使用list进行转换
X = list(range(-10, 10))
Y = list(map(sigmoid, X))

fig = plt.figure(figsize=(4, 4))
ax = fig.add_subplot(111)

# 隐藏上边和右边
ax.spines["top"].set_color("none")
ax.spines["right"].set_color("none")

# 移动另外两个轴
ax.yaxis.set_ticks_position("left")
ax.spines["left"].set_position(("data", 0))
ax.xaxis.set_ticks_position("bottom")
ax.spines["bottom"].set_position(("data", 0.5))

ax.plot(X, Y)
plt.show()
