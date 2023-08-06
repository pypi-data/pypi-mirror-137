# coding:utf-8
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
# 语料
corpus = [
    'This is the first document.',
    'This is the second second document.',
    'And the third one.',
    'Is this the first document?',
]
# 将文本中的词语转换为词频矩阵
vectorizer = CountVectorizer()
# 计算个词语出现的次数
X = vectorizer.fit_transform(corpus)
# 获取词袋中所有文本关键词
word = vectorizer.get_feature_names()
print(word)
# 查看词频结果
print(X.toarray())

from sklearn.feature_extraction.text import TfidfTransformer

# 类调用
transformer = TfidfTransformer()
print(transformer)
# 将词频矩阵X统计成TF-IDF值
tfidf = transformer.fit_transform(X)
# 查看数据结构 tfidf[i][j]表示i类文本中的tf-idf权重

print(tfidf.toarray())

# obtain the top K keywords
feature_array = np.array(vectorizer.get_feature_names())
tfidf_sorting = np.argsort(tfidf.toarray()).flatten()[::-1]

n = 3
top_n = feature_array[tfidf_sorting][:n]

print("top keywords: ")
print(top_n)

