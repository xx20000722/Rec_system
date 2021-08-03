# -*-coding:utf-8-*-
"""
    Author: Thinkgamer
    Desc:
        代码7-4 实例21：创建一个基于地域和热度的酒店推荐系统
"""
import pandas as pd

class RecBasedAH:
    def __init__(self,path=None,addr="朝阳区",type="score",k=10, sort=False):
        self.path = path
        self.addr = addr
        self.type = type
        self.k = k
        self.sort = sort
        self.data = self.load_mess()

    # 使用pandas加载数据
    def load_mess(self):
        data =pd.read_csv(self.path,header=0,sep=",",encoding='GBK')
        return data[data["addr"]==self.addr]

    def reccomend(self):
        if self.type in ["score","comment_num","lowest_price","decoration_time","open_time"]:
            data = self.data.sort_values(by=[self.type, "lowest_price"], ascending=self.sort)[:self.k]
            return dict(data.filter(items=["name",self.type]).values)
        elif self.type == "combine":      # 综合排序，综合以上五种因素
            # 过滤得到使用的信息
            data = self.data.filter(items=["name","score","comment_num","decoration_time","open_time","lowest_price"])
            # 对装修时间做处理
            data["decoration_time"] = data["decoration_time"].apply(lambda  x: int(x) - 2018)
            data["open_time"] = data["open_time"].apply(lambda  x: 2018 - int(x))
            # 数据归一化
            for col in data.keys():
                if col !="name":
                    data[col]  = ( data[col] - data[col].min() ) / (data[col].max() - data[col].min() )

            # 这里认为 评分的权重为1，评论数目权重为2，装修和开业时间权重为0.5，最低价权重为1.5
            data[self.type]=1 * data["score"] + 2 * data["comment_num"] + \
                            0.5 * data["decoration_time"] + 0.5 * data["open_time"] + 1.5 * data["lowest_price"]
            data = data.sort_values(by=self.type, ascending=self.sort)[:self.k]
            return dict(data.filter(items=["name", self.type]).values)

if __name__ == "__main__":
    path = "../data/hotel-mess/hotel-mess.csv"
    """
    参数说明
    addr: 酒店所在地区，有朝阳区，丰台区，东城区，西城区，海淀区，顺义区，石景山区，延庆区，房山区，通州区
    type：排序字段，默认为 评分：score
          支持 评论数目：comment_num，装修时间：decoration_time，开业时间：open_time，最低价格：lowest_price，综合排序：combine
    k：返回结果的数目
    sort：按照指定字段的排序方式，默认为降序， True为升序  False为降序
    """

    hotel_rec = RecBasedAH(path,addr="丰台区",type="combine",k=10,sort=False)
    results = hotel_rec.reccomend()
    print(results)
