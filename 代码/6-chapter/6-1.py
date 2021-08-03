# -*-coding:utf-8-*-

"""
    Author: Thinkgamer
    Desc:
        代码6-1 实例18 基于TF-IDF的关键词提取
"""
import jieba
import math
import jieba.analyse

class TF_IDF:
    def __init__(self, file, stop_file):
        self.file = file
        self.stop_file = stop_file
        self.stop_words = self.getStopWords()

    # 获取停用词列表
    def getStopWords(self):
        swlist = list()
        for line in open(self.stop_file, "r", encoding="utf-8").readlines():
            swlist.append(line.strip())
        print("加载停用词完成...")
        return swlist

    # 加载商品和其对应的短标题，使用jieba进行分词并去除停用词
    def loadData(self):
        dMap = dict()
        for line in open(self.file, "r", encoding="utf-8").readlines():
            id, title = line.strip().split("\t")
            dMap.setdefault(id, [])
            for word in list(jieba.cut(str(title).replace(" ", ""), cut_all=False)):
                if word not in self.stop_words:
                    dMap[id].append(word)
        print("加载商品和对应的短标题，并使用jieba分词和去除停用词完成...")
        return dMap

    # 获取一个短标题中的词频
    def getFreqWord(self, words):
        freqWord = dict()
        for word in words:
            freqWord.setdefault(word, 0)
            freqWord[word] += 1
        return freqWord

    # 统计单词在所有短标题中出现的次数
    def getCountWordInFile(self, word, dMap):
        count = 0
        for key in dMap.keys():
            if word in dMap[key]:
                count += 1
        return count

    # 计算TFIDF值
    def getTFIDF(self, words, dMap):
        # 记录单词关键词和对应的tfidf值
        outDic = dict()
        freqWord = self.getFreqWord(words)
        for word in words:
            # 计算TF值，即单个word在整句中出现的次数
            tf = freqWord[word] * 1.0 / len(words)
            # 计算IDF值，即log(所有的标题数/(包含单个word的标题数+1))
            idf = math.log(len(dMap) / (self.getCountWordInFile(word, dMap) + 1))
            tfidf = tf * idf
            outDic[word] = tfidf
        # 给字典排序
        orderDic = sorted(outDic.items(), key=lambda x: x[1], reverse=True)
        return orderDic

    def getTag(self, words):
        # withWeight 用来设置是否打印权重
        print(jieba.analyse.extract_tags(words, topK=20, withWeight=True))


if __name__ == "__main__":
    # 数据集
    file = "../data/phone-title/id_title.txt"
    # 停用词文件
    stop_file = "../data/phone-title/stop_words.txt"

    tfidf = TF_IDF(file, stop_file)
    # tfidf.getTag("小米 红米6Pro 异形全面屏， 后置1200万双摄， 4000mAh超大电池")

    # dMap 中key为商品id，value为去除停用词后的词
    dMap = tfidf.loadData()
    for id in dMap.keys():
        tfIdfDic = tfidf.getTFIDF(dMap[id],dMap)
        print(id,tfIdfDic)
