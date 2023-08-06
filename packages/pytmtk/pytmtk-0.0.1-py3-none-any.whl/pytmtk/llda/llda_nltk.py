#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Labeled LDA using nltk.corpus.reuters as dataset
# This code is available under the MIT License.
# (c)2013 Nakatani Shuyo / Cybozu Labs Inc.

import nltk
from pytmtk.config import MethodConfig
import sys, numpy
from llda import LLDA
from optparse import OptionParser
from functools import reduce

import argparse
parser = argparse.ArgumentParser(description='LLDA method')
parser.add_argument('--input', '-i', help='input folder', default="../../../examples/data/datasets/ehealthforumQAs.json")
parser.add_argument('--output', '-o', help='output folder', default="../../../examples/data/llda")
args = parser.parse_args()

import os
if not os.path.exists(args.output):
    os.mkdir(args.output)

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

K=300
iteration=100
alpha=0.001
beta=0.001

corpus=[]
labels=[]
import json
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

with open(args.input, 'r',encoding='utf-8') as content_file:
    text = content_file.read()
    text = bytes(text, 'utf-8').decode('utf-8', 'ignore')

    for r in json.loads(text):
        question = r['question']
        answer = r['answer']
        tag = r['tags']
        # print(answer)
        filtered_sentence = [w.lower() for w in question.split(' ') if not w.lower() in stop_words]
        corpus.append(filtered_sentence)
        labels.append(tag)

labelset = list(set(reduce(list.__add__, labels)))

llda = LLDA(K, alpha, beta)
llda.set_corpus(labelset, corpus, labels)

print("M=%d, V=%d, L=%d, K=%d" % (len(corpus), len(llda.vocas), len(labelset), K))
fo_progress = open(f"{args.output}/perplexity-"+str(K)+".txt", "w",encoding='utf-8')
for i in range(iteration):
    perplexity = llda.perplexity()
    sys.stderr.write("-- %d : %.4f\n" % (i + 1, perplexity))
    fo_progress.write(str(i + 1) + "\t" + str(K) + "\t" + str(alpha) + "\t" + str(beta) + "\t" + str(perplexity) + "\n")
    llda.inference()
fo_progress.close()
print("perplexity : %.4f" % llda.perplexity())

'''
phi = llda.phi()
for k, label in enumerate(labelset):
    print("\n-- label %d : %s" % (k, label))
    for w in numpy.argsort(-phi[k])[:20]:
        print("%s: %.4f" % (llda.vocas[w], phi[k,w]))
'''

'''
max_label,label_term,label_weight,label_words,label_word_weights=llda.predict('could extra caffeine consumption be a cause of mild unilateral breast tenderness',10)

label_term,label_weight=sort_result(label_term,label_weight)

print("result: ",max_label)
print("topK result: ",label_term[:10])

'''

fo_result = open(f"{args.output}/result.txt", "w",encoding='utf-8')
fo_raw = open(f"{args.output}/raw.txt", "w",encoding='utf-8')
fo_ref = open(f"{args.output}/ref.txt", "w",encoding='utf-8')

for i,text in enumerate(corpus):
    tt=' '.join(text)
    max_label, label_term, label_weight, label_words, label_word_weights = llda.predict(
        tt, 10)
    label_term, label_weight = sort_result(label_term, label_weight)
    fo_raw.write(tt + "\n")
    fo_ref.write(' '.join(labels[i]) + "\n")
    fo_result.write(' '.join(label_term[:10]) + "\n")

fo_raw.close()
fo_result.close()
fo_ref.close()
