# -*-coding:utf-8-*-

"""
    Author: Thinkgamer
    Desc:
        代码4-1 Python实现标准化方法
"""
import numpy as np
import math

class DataNorm:
    def __init__(self):
        self.arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.x_max = max(self.arr)  # 最大值
        self.x_min = min(self.arr)  # 最小值
        self.x_mean = sum(self.arr) / len(self.arr)  # 平均值
        self.x_std = np.std(self.arr)  # 标准差

    def Min_Max(self):
        arr_ = list()
        for x in self.arr:
            # round(x,4) 对x保留4位小数
            arr_.append(round((x - self.x_min) / (self.x_max - self.x_min), 4))
        print("经过Min_Max标准化后的数据为:\n{}".format(arr_))

    def Z_Score(self):
        arr_ = list()
        for x in self.arr:
            arr_.append(round((x - self.x_mean) / self.x_std, 4))
        print("经过Z_Score标准化后的数据为:\n{}".format(arr_))

    # 有点问题，改为如下这样
    # def DecimalScaling(self):
    #     arr_ = list()
    #     j = self.x_max // 10 if self.x_max % 10 == 0 else self.x_max // 10 + 1
    #     for x in self.arr:
    #         arr_.append(round(x / math.pow(10, j), 4))
    #     print("经过Decimal Scaling标准化后的数据为:\n{}".format(arr_))
    def DecimalScaling(self):
        arr_ = list()
        j = 1
        x_max = max([abs(one) for one in self.arr])
        while x_max / 10 >= 1.0:
            j += 1
            x_max = x_max / 10
        for x in self.arr:
            arr_.append(round(x / math.pow(10, j), 4))
        print("经过Decimal Scaling标准化后的数据为:\n{}".format(arr_))

    def Mean(self):
        arr_ = list()
        for x in self.arr:
            arr_.append(round((x - self.x_mean) / (self.x_max - self.x_min), 4))
        print("经过均值标准化后的数据为:\n{}".format(arr_))

    def Vector(self):
        arr_ = list()
        for x in self.arr:
            arr_.append(round(x / sum(self.arr), 4))
        print("经过向量标准化后的数据为:\n{}".format(arr_))

    def exponential(self):
        arr_1 = list()
        for x in self.arr:
            arr_1.append(round(math.log10(x) / math.log10(self.x_max), 4))
        print("经过指数转换法（log10）标准化后的数据为;\n{}".format(arr_1))

        arr_2 = list()
        sum_e = sum([math.exp(one) for one in self.arr])
        for x in self.arr:
            arr_2.append(round(math.exp(x) / sum_e, 4))
        print("经过指数转换法（SoftMax）标准化后的数据为;\n{}".format(arr_2))

        arr_3 = list()
        for x in self.arr:
            arr_3.append(round(1 / (1 + math.exp(-x)), 4))
        print("经过指数转换法（Sigmoid）标准化后的数据为;\n{}".format(arr_3))

if __name__ == "__main__":
    dn = DataNorm()
    dn.Min_Max()
    dn.Z_Score()
    dn.DecimalScaling()
    dn.Mean()
    dn.Vector()
    dn.exponential()
