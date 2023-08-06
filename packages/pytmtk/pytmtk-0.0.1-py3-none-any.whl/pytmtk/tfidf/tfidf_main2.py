# coding:utf-8

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

def sort_result(word_list,weight_list):
    for i in range(len(weight_list)-1):
        for j in range(i+1,len(weight_list)):
            if weight_list[i] < weight_list[j]:
                temp_w=weight_list[i]
                weight_list[i]=weight_list[j]
                weight_list[j]=temp_w
                temp_s = word_list[i]
                word_list[i] = word_list[j]
                word_list[j] = temp_s
    return word_list,weight_list

import json

def main():
    '''
    corpus = [
        'This is the first document.',
        'This is the second second document.',
        'And the third one.',
        'Is this the first document?',
    ]
    '''

    import argparse
    parser = argparse.ArgumentParser(description='tfidf method')
    parser.add_argument('--input', '-i', help='input folder',
                        default="../../../examples/data/datasets/ehealthforumQAs.json")
    parser.add_argument('--output', '-o', help='output folder', default="../../../examples/data/tfidf")
    args = parser.parse_args()
    import os
    if not os.path.exists(args.output):
        os.mkdir(args.output)

    corpus=[]
    tags=[]
    with open(args.input, 'r',encoding='utf-8') as content_file:
        text = content_file.read()
        text = bytes(text, 'utf-8').decode('utf-8', 'ignore')
    for r in json.loads(text):
        question = r['question']
        answer = r['answer']
        tag = r['tags']
        #print(answer)
        corpus.append(question)
        tags.append(tag)

    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))

    vectorizer = CountVectorizer(stop_words=stop_words)  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    tfidf = transformer.fit_transform(
        vectorizer.fit_transform(corpus))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语

    print(word)

    weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重

    fo_result = open(f"{args.output}/result.txt", "w")
    fo_raw = open(f"{args.output}/raw.txt", "w")
    fo_ref=open(f"{args.output}/ref.txt", "w")

    for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        print(u"-------这里输出第", i, u"类文本的词语tf-idf权重------")
        word_list=[]
        weight_list=[]
        for j in range(len(word)):
            #print(word[j], weight[i][j])
            word_list.append(word[j])
            weight_list.append(weight[i][j])

        word_list,weight_list=sort_result(word_list,weight_list)

        topK=10
        #print(word_list[:topK])
        #print(weight_list[:topK])

        print(corpus[i])
        print(word_list[:topK])
        print(weight_list[:topK])
        print()
        important_keywords=[]
        for idx, w in enumerate(weight_list[:topK]):
            if w!=0:
                important_keywords.append(word_list[idx])

        fo_raw.write(corpus[i].replace('\n',' ').strip() + "\n")
        fo_ref.write(' '.join(tags[i])+"\n")
        fo_result.write(' '.join(important_keywords)+"\n")

    fo_raw.close()
    fo_result.close()
    fo_ref.close()

main()