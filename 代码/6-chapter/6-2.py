# -*-coding:utf-8-*-

"""
    Author: Thinkgamer
    Desc:
        代码6-2 实例19 利用标签推荐算法实现艺术家的推荐
"""

import pandas as pd
import math

class RecBasedTag:
    # 由于从文件读取为字符串，统一格式为整数，方便后续计算
    def __init__(self):
        # 用户听过艺术次数文件
        self.user_rate_file = "../data/lastfm-2k/user_artists.dat"
        # 用户打标签信息
        self.user_tag_file = "../data/lastfm-2k/user_taggedartists.dat"

        # 获取所有的艺术家ID
        self.artistsAll = list(
            pd.read_table("../data/lastfm-2k/artists.dat", delimiter="\t")["id"].values
        )
        # 用户对艺术家的评分
        self.userRateDict = self.getUserRate()
        # 艺术家与标签的相关度
        self.artistsTagsDict = self.getArtistsTags()
        # 用户对每个标签打标的次数统计和每个标签被所有用户打标的次数统计
        self.userTagDict, self.tagUserDict = self.getUserTagNum()
        # 用户最终对每个标签的喜好程度
        self.userTagPre = self.getUserTagPre()

    # 获取用户对艺术家的评分信息
    def getUserRate(self):
        userRateDict = dict()
        fr = open(self.user_rate_file, "r", encoding="utf-8")
        for line in fr.readlines():
            if not line.startswith("userID"):
                userID, artistID, weight = line.split("\t")
                userRateDict.setdefault(int(userID), {})
                # 对听歌次数进行适当比例的缩放，避免计算结果过大
                userRateDict[int(userID)][int(artistID)] = float(weight) / 10000
        return userRateDict

    # 获取艺术家对应的标签基因,这里的相关度全部为1
    # 由于艺术家和tag过多，存储到一个矩阵中维度太大，这里优化存储结构
    # 如果艺术家有对应的标签则记录，相关度为1，否则不为1
    def getArtistsTags(self):
        artistsTagsDict = dict()
        for line in open(self.user_tag_file, "r", encoding="utf-8"):
            if not line.startswith("userID"):
                artistID, tagID = line.split("\t")[1:3]
                artistsTagsDict.setdefault(int(artistID), {})
                artistsTagsDict[int(artistID)][int(tagID)] = 1
        return artistsTagsDict

    # 获取每个用户打标的标签和每个标签被所有用户打标的次数
    def getUserTagNum(self):
        userTagDict = dict()
        tagUserDict = dict()
        for line in open(self.user_tag_file, "r", encoding="utf-8"):
            if not line.startswith("userID"):
                userID, artistID, tagID = line.strip().split("\t")[:3]
                # 统计每个标签被打标的次数
                if int(tagID) in tagUserDict.keys():
                    tagUserDict[int(tagID)] += 1
                else:
                    tagUserDict[int(tagID)] = 1
                # 统计每个用户对每个标签的打标次数
                userTagDict.setdefault(int(userID), {})
                if int(tagID) in userTagDict[int(userID)].keys():
                    userTagDict[int(userID)][int(tagID)] += 1
                else:
                    userTagDict[int(userID)][int(tagID)] = 1
        return userTagDict, tagUserDict

    # 获取用户对标签的最终兴趣度
    def getUserTagPre(self):
        userTagPre = dict()
        userTagCount = dict()
        # Num 为用户打标总条数
        Num = len(open(self.user_tag_file, "r", encoding="utf-8").readlines())
        for line in open(self.user_tag_file, "r", encoding="utf-8").readlines():
            if not line.startswith("userID"):
                userID, artistID, tagID = line.split("\t")[:3]
                userTagPre.setdefault(int(userID), {})
                userTagCount.setdefault(int(userID), {})
                rate_ui = (
                    self.userRateDict[int(userID)][int(artistID)]
                    if int(artistID) in self.userRateDict[int(userID)].keys()
                    else 0
                )
                if int(tagID) not in userTagPre[int(userID)].keys():
                    userTagPre[int(userID)][int(tagID)] = (
                        rate_ui * self.artistsTagsDict[int(artistID)][int(tagID)]
                    )
                    userTagCount[int(userID)][int(tagID)] = 1
                else:
                    userTagPre[int(userID)][int(tagID)] += (
                        rate_ui * self.artistsTagsDict[int(artistID)][int(tagID)]
                    )
                    userTagCount[int(userID)][int(tagID)] += 1

        for userID in userTagPre.keys():
            for tagID in userTagPre[userID].keys():
                tf_ut = self.userTagDict[int(userID)][int(tagID)] / sum(
                    self.userTagDict[int(userID)].values()
                )
                idf_ut = math.log(Num * 1.0 / (self.tagUserDict[int(tagID)] + 1))
                userTagPre[userID][tagID] = (
                    userTagPre[userID][tagID]/userTagCount[userID][tagID] * tf_ut * idf_ut
                )
        return userTagPre

    # 对用户进行艺术家推荐
    def recommendForUser(self, user, K, flag=True):
        userArtistPreDict = dict()
        # 得到用户没有打标过的艺术家
        for artist in self.artistsAll:
            if int(artist) in self.artistsTagsDict.keys():
                # 计算用户对艺术的喜好程度
                for tag in self.userTagPre[int(user)].keys():
                    rate_ut = self.userTagPre[int(user)][int(tag)]
                    rel_it = (
                        0
                        if tag not in self.artistsTagsDict[int(artist)].keys()
                        else self.artistsTagsDict[int(artist)][tag]
                    )
                    if artist in userArtistPreDict.keys():
                        userArtistPreDict[int(artist)] += rate_ut * rel_it
                    else:
                        userArtistPreDict[int(artist)] = rate_ut * rel_it
        newUserArtistPreDict = dict()
        if flag:
            # 对推荐结果进行过滤，过滤掉用户已经听过的艺术家
            for artist in userArtistPreDict.keys():
                if artist not in self.userRateDict[int(user)].keys():
                    newUserArtistPreDict[artist] = userArtistPreDict[int(artist)]
            return sorted(
                newUserArtistPreDict.items(), key=lambda k: k[1], reverse=True
            )[:K]
        else:
            # 表示是用来进行效果评估
            return sorted(
                userArtistPreDict.items(), key=lambda k: k[1], reverse=True
            )[:K]

    # 效果评估 重合度
    def evaluate(self, user):
        K = len(self.userRateDict[int(user)])
        recResult = self.recommendForUser(user, K=K, flag=False)
        count = 0
        for (artist, pre) in recResult:
            if artist in self.userRateDict[int(user)]:
                count += 1
        return count * 1.0 / K

if __name__ == "__main__":
    rbt = RecBasedTag()
    print(rbt.recommendForUser("2", K=20))
    print(rbt.evaluate("2"))
