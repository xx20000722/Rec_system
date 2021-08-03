
from sklearn import preprocessing

"""
性别特征：["男"，"女"]
运动特征：["足球"，"篮球"，"羽毛球"，"乒乓球"]
祖国特征：["中国"，"美国，"法国"]
"""
# 训练集
test = [[1, 4, 3], [2, 3, 2], [1, 2, 2], [2, 1, 1]]
enc = preprocessing.OneHotEncoder()
enc.fit(test)
array = enc.transform([[2, 2, 2], [1, 4, 3]]).toarray()
print(array)