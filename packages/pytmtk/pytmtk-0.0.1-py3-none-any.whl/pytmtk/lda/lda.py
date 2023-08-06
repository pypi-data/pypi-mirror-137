import json
from nltk.corpus import stopwords

import argparse
parser = argparse.ArgumentParser(description='LDA method')
parser.add_argument('--input', '-i', help='input folder', default="../../../examples/data/datasets/ehealthforumQAs.json")
parser.add_argument('--output', '-o', help='output folder', default="../../../examples/data/lda")

args = parser.parse_args()

import os
if not os.path.exists(args.output):
    os.mkdir(args.output)

corpus = []
tags = []

with open(args.input, 'r', encoding='utf-8') as content_file:
    text = content_file.read()
    text = bytes(text, 'utf-8').decode('utf-8', 'ignore')

stop_words = set(stopwords.words('english'))

for r in json.loads(text):
    question = r['question']
    answer = r['answer']
    tag = r['tags']
    # print(answer)
    filtered_sentence = [w for w in question.split(' ') if not w in stop_words]
    corpus.append(' '.join(filtered_sentence))
    tags.append(tag)

from nltk.stem.wordnet import WordNetLemmatizer
import string

exclude = set(string.punctuation)
lemma = WordNetLemmatizer()

doc_clean = [doc.split(' ') for doc in corpus]

import gensim
from gensim import corpora

# 创建语料的词语词典，每个单独的词语都会被赋予一个索引
dictionary = corpora.Dictionary(doc_clean)

# 使用上面的词典，将转换文档列表（语料）变成 DT 矩阵
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

# 使用 gensim 来创建 LDA 模型对象
Lda = gensim.models.ldamodel.LdaModel

NumberOfTopics = 20
NumberOfWords = 10

# 在 DT 矩阵上运行和训练 LDA 模型
ldamodel = Lda(doc_term_matrix, num_topics=NumberOfTopics, id2word=dictionary)

# 输出结果
# print(ldamodel.print_topics(num_topics=5, num_words=3))

fo_result = open(f"{args.output}/result.txt", "w", encoding='utf-8')
fo_raw = open(f"{args.output}/raw.txt", "w", encoding='utf-8')
fo_ref = open(f"{args.output}/ref.txt", "w", encoding='utf-8')

def sort_result(word_list, weight_list):
    for i in range(len(weight_list) - 1):
        for j in range(i + 1, len(weight_list)):
            if weight_list[i] < weight_list[j]:
                temp_w = weight_list[i]
                weight_list[i] = weight_list[j]
                weight_list[j] = temp_w
                temp_s = word_list[i]
                word_list[i] = word_list[j]
                word_list[j] = temp_s
    return word_list, weight_list

# 预测主题
for i, text in enumerate(corpus):
    doc_bow = dictionary.doc2bow(text.split(' '))
    doc_lda = ldamodel[doc_bow]
    print("doc: ", text)
    important_keywords = []

    max_topic_prob = -1
    max_topic_prob_index = -1
    for idx, topic in enumerate(doc_lda):
        topic_prob = topic[1]
        topic_keywords = ldamodel.print_topic(topic[0])
        print("---desc----")
        print(topic_prob)
        print(topic_keywords)
        if topic_prob > max_topic_prob:
            max_topic_prob = topic_prob
            max_topic_prob_index = idx

    '''
    print('-----detail------')

    for idx, topic in ldamodel.show_topics(formatted=False, num_words=3):
        print('Topic: {}, Words: {}, Weights: {}'.format(idx, [w[0] for w in topic], [w[1] for w in topic]))
        if idx==max_topic_prob_index:
            important_keywords=[w[0] for w in topic]
    '''

    from gensim.parsing.preprocessing import preprocess_string, strip_punctuation, strip_numeric, \
        strip_non_alphanum, strip_short
    lda_topics = ldamodel.show_topics(num_words=NumberOfWords, num_topics=NumberOfTopics)

    topics = []
    filters = [lambda x: x.lower(), strip_punctuation, strip_numeric]
    topic_weights = []
    for topic in lda_topics:
        print("each topic: ")
        # print(topic[1])
        weights = []
        topic_list = topic[1].split('+')
        for idx, w in enumerate(topic_list):
            weights.append(float(topic_list[idx].strip().split('*')[0].strip()))
        print("weight: ", weights)
        # print(topic[1].split('*')[0])
        topic_weights.append(weights)
        tt = preprocess_string(topic[1], filters)
        print("topics:", tt)
        topics.append(tt)

    topics, topic_weights = sort_result(topics, topic_weights)

    # print(topics)
    # print(max_topic_prob_index)
    for t in topics[:3]:
        for w in t[:5]:
            important_keywords.append(w)

    fo_raw.write(corpus[i].replace('\n', ' ').strip() + "\n")
    fo_ref.write(' '.join(tags[i]) + "\n")
    fo_result.write(' '.join(important_keywords) + "\n")

fo_raw.close()
fo_result.close()
fo_ref.close()


