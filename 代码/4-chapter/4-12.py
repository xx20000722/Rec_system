# -*-coding:utf-8-*-

"""
    Author: Thinkgamer
    Desc:
        代码4-12 基于Apriori算法实现频繁项集合相关规则挖掘
"""

class Apriori:
    def __init__(self, minSupport, minConfidence):
        # 最小支持度
        self.minSupport = minSupport
        # 最小置信度
        self.minConfidence = minConfidence
        self.data = self.loadData()

    # 加载数据集
    def loadData(self):
        return [[1, 5], [2, 3, 4], [2, 3, 4, 5], [2, 3]]

    # 生成项集C1，不包含项集中每个元素出现的次数
    def createC1(self, data):
        C1 = list()  # C1为大小为1的项的集合
        for items in data:  # 遍历数据集
            for item in items:
                if [item] not in C1:
                    C1.append([item])
        # map函数表示遍历C1中的每一个元素执行forzenset
        # frozenset表示“冰冻”的集合，即不可改变
        return list(map(frozenset, sorted(C1)))

    # 该函数用于从候选项集Ck生成Lk，Lk表示满足最低支持度的元素集合
    def scanD(self, Ck):
        # Data表示数据列表的列表 [set([]), set([]), set([]), set([])]
        Data = list(map(set, self.data))
        CkCount = {}
        # 统计Ck项集中每个元素出现的次数
        for items in Data:
            for one in Ck:
                # issubset：表示如果集合one中的每一元素都在items中则返回true
                if one.issubset(items):
                    CkCount.setdefault(one, 0)
                    CkCount[one] += 1
        numItems = len(list(Data))  # 数据条数
        Lk = []  # 初始化符合支持度的项集
        supportData = {}  # 初始化所有符合条件的项集及对应的支持度
        for key in CkCount:
            # 计算每个项集的支持度，如果满足条件则把该项集加入到Lk列表中
            support = CkCount[key] * 1.0 / numItems
            if support >= self.minSupport:
                Lk.insert(0, key)
            # 构建支持的项集的字典
            supportData[key] = support
        return Lk, supportData

    # generateNewCk的输人参数为频繁项集列表Lk与项集元素个数k，输出为Ck
    def generateNewCk(self, Lk, k):
        nextLk = []
        lenLk = len(Lk)
        # 若两个项集的长度为k-1,则必须前k-2项相同才可连接，即求并集，所以[:k-2]的实际作用为取列表的前k-1个元素
        for i in range(lenLk):
            for j in range(i + 1, lenLk):
                # 前k-2项相同时合并两个集合
                L1 = list(Lk[i])[: k - 2]
                L2 = list(Lk[j])[: k - 2]
                if sorted(L1) == sorted(L2):
                    nextLk.append(Lk[i] | Lk[j])
        return nextLk

    # 生成频繁项集
    def gengrateLK(self):
        # 构建候选项集C1
        C1 = self.createC1(self.data)
        L1, supportData = self.scanD(C1)
        L = [L1]
        k = 2
        while len(L[k - 2]) > 0:
            # 组合项集Lk中的元素，声新的候选项集Ck
            Ck = self.generateNewCk(L[k - 2], k)
            Lk, supK = self.scanD(Ck)
            supportData.update(supK)
            L.append(Lk)
            k += 1
        return L, supportData

    # 生成关联规则
    def generateRules(self, L, supportData):
        ruleResult = []  # 最终记录的关联规则结果
        for i in range(1, len(L)):
            for ck in L[i]:
                Cks = [frozenset([item]) for item in ck]
                # 频繁项集中有三个及以上元素的集合
                self.rulesOfMore(ck, Cks, supportData, ruleResult)
        return ruleResult

    # 频繁项集只有两个元素
    def rulesOfTwo(self, ck, Cks, supportData, ruleResult):
        prunedH = []
        for oneCk in Cks:
            # 计算置信度
            conf = supportData[ck] / supportData[ck - oneCk]
            if conf >= self.minConfidence:
                print(ck - oneCk, "-->", oneCk, "Confidence is:", conf)
                ruleResult.append((ck - oneCk, oneCk, conf))
                prunedH.append(oneCk)
        return prunedH

    # 频繁项集中有三个及以上元素的集合，递归生成关联规则
    def rulesOfMore(self, ck, Cks, supportData, ruleResult):
        m = len(Cks[0])
        while len(ck) > m:
            Cks = self.rulesOfTwo(ck, Cks, supportData, ruleResult)
            if len(Cks) > 1:
                Cks = self.generateNewCk(Cks, m + 1)
                m += 1
            else:
                break


if __name__ == "__main__":
    apriori = Apriori(minSupport=0.5, minConfidence=0.6)
    L, supportData = apriori.gengrateLK()
    for one in L:
        print("项数为 %s 的频繁项集：" % (L.index(one) + 1), one)
    print("supportData:", supportData)
    print("minConf=0.6时：")
    rules = apriori.generateRules(L, supportData)
