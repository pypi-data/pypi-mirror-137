#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Labeled LDA using nltk.corpus.reuters as dataset
# This code is available under the MIT License.
# (c)2013 Nakatani Shuyo / Cybozu Labs Inc.
import json
from nltk.corpus import stopwords
import nltk
import sys, numpy
from llda import LLDA
from optparse import OptionParser
from functools import reduce
from nltk.stem import WordNetLemmatizer
wnl = WordNetLemmatizer()

def obtain_tags(w):
    tokens = nltk.word_tokenize(w)
    pos_tags = nltk.pos_tag(tokens)
    for word, pos in pos_tags:
        if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):
            return 'n'
        if (pos=='VB' or pos=='VBG' or pos=='VBD' or pos=='VBN' or pos=='VBP' or pos=='VBZ'):
            return 'v'
        if (pos=='JJ' or pos=='JJR' or pos=='JJS'):
            return 'a'
    return None

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

def LLDA_Main(
        input_file,
        input_knowledge,
        output_folder,
        stopwords_file,
        knowledge_dict_path
):
    K = 50
    iteration = 20
    alpha = 0.001
    beta = 0.001

    corpus = []
    labels = []

    stop_words = set(stopwords.words('english'))

    # load icd-11 code
    fo_info = open(f'{input_knowledge}', 'r', encoding='utf-8')

    icd11_titles = {}

    for line in fo_info.readlines():
        ls = line.strip().split(',')
        if len(ls) > 4:
            icd11_code = ls[1].strip()
            icd11_title = ls[2].strip()
            icd11_titles[icd11_code] = icd11_title

    fo_info.close()

    icd11_terms = {}
    icd11_terms_codes = {}

    from pytmtk.rake.rake import Rake

    rake = Rake(stop_words_path=stopwords_file)

    for line in open(knowledge_dict_path, 'r', encoding='utf-8'):
        if len(line.strip()) != 0:
            ls = line.split('\t')
            icd11_word = ls[0]
            icd11_freq = ls[1]
            icd11_codes = ls[2].split(' ')

            new_w = icd11_word
            if icd11_word.lower() not in stop_words:
                pos = obtain_tags(icd11_word.lower())
                if pos is None:
                    pos = 'n'
                new_w = wnl.lemmatize(icd11_word.lower(), pos)
                if new_w is not None:
                    new_w = new_w
                else:
                    new_w = icd11_word.lower()

            icd11_terms[new_w] = icd11_freq
            icd11_terms_codes[new_w] = icd11_codes

    with open(input_file, 'r', encoding='utf-8') as content_file:
        text = content_file.read()
        text = bytes(text, 'utf-8').decode('utf-8', 'ignore')
        for r in json.loads(text):
            question = r['question']
            answer = r['answer']
            tag = r['tags']
            # print(answer)
            # filtered_sentence = [w.lower() for w in question.split(' ') if not w.lower() in stop_words]
            filtered_sentence = []
            for w in question.split(' '):
                if w.lower() not in stop_words:
                    pos = obtain_tags(w.lower())
                    if pos is None:
                        pos = 'n'

                    pos = 'n'
                    new_w = wnl.lemmatize(w.lower(), pos)
                    if new_w is not None:
                        filtered_sentence.append(new_w)
                    # else:
                    #    filtered_sentence.append(w.lower())
            # filtered_sentence = [w.lower() for w in filtered_sentence if w in icd11_terms.keys()]
            new_sentence = []
            for w in filtered_sentence:
                if not icd11_terms.__contains__(w):
                    new_sentence.append(w)
                    continue
                codes = icd11_terms_codes[w]
                for code in codes:
                    if len(code.strip()) <= 0:
                        continue
                    if not icd11_titles.__contains__(code.strip()):
                        continue
                    title = icd11_titles[code.strip()]
                    filtered_title = [a.lower() for a in title.split(' ') if not a.lower() in stop_words]
                    for x in filtered_title:
                        new_sentence.append(x)
            if len(new_sentence) == 0:
                continue
            ks = rake.run(' '.join(new_sentence))
            word_list = []
            weight_list = []
            for w in ks:
                word_list.append(w[0])
                weight_list.append(w[1])
            word_list, weight_list = sort_result(word_list, weight_list)

            new_word_list = []

            topKnowledgeN = 10
            if len(word_list) > topKnowledgeN:
                new_word_list = new_word_list[:topKnowledgeN]
            else:
                new_word_list = new_word_list

            for x in new_word_list:
                if x not in filtered_sentence:
                    filtered_sentence.append(x)

            corpus.append(filtered_sentence)
            labels.append(tag)

    labelset = list(set(reduce(list.__add__, labels)))

    llda = LLDA(K, alpha, beta, icd11_terms, icd11_terms_codes)
    llda.set_corpus(labelset, corpus, labels)

    print("M=%d, V=%d, L=%d, K=%d" % (len(corpus), len(llda.vocas), len(labelset), K))

    fo_progress = open(f"{output_folder}/perplexity-" + str(K) + ".txt", "w", encoding='utf-8')
    for i in range(iteration):
        perplexity = llda.perplexity()
        sys.stderr.write("-- %d : %.4f\n" % (i + 1, perplexity))
        fo_progress.write(
            str(i + 1) + "\t" + str(K) + "\t" + str(alpha) + "\t" + str(beta) + "\t" + str(perplexity) + "\n")
        llda.inference()
    print("perplexity : %.4f" % llda.perplexity())
    fo_progress.close()
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

    fo_result = open(f"{output_folder}/result.txt", "w", encoding='utf-8')
    fo_raw = open(f"{output_folder}/raw.txt", "w", encoding='utf-8')
    fo_ref = open(f"{output_folder}/ref.txt", "w", encoding='utf-8')

    for i, text in enumerate(corpus):
        if len(text) == 0:
            continue

        tt = ' '.join(text)
        if len(tt.strip()) == 0:
            continue
        max_label, label_term, label_weight, label_words, label_word_weights = llda.predict(
            tt, 10)
        label_term, label_weight = sort_result(label_term, label_weight)
        fo_raw.write(tt + "\n")
        fo_ref.write(' '.join(labels[i]) + "\n")
        fo_result.write(' '.join(label_term[:10]) + "\n")

    fo_raw.close()
    fo_result.close()
    fo_ref.close()

    fo_K = open(f"{output_folder}/K.txt", "w", encoding='utf-8')
    fo_K.write(str(K) + "\t" + str(alpha) + "\t" + str(beta))
    fo_K.close()

    # stat_results
    import os

    os.chdir(os.path.abspath(os.curdir))
    os.system(f"python rouge_score.py --output {output_folder}")


import argparse
parser = argparse.ArgumentParser(description='KCLLDA method')
parser.add_argument('--input', '-i', help='input folder', default="../../../examples/data/datasets/ehealthforumQAs.json")
parser.add_argument('--inputknowledge', '-ik', help='input knowledge file',default='../../../examples/knowledge/data/graph_nodes_import.txt')
parser.add_argument('--output', '-o', help='output folder', default="../../../examples/data/kcllda")
parser.add_argument('--stopwords', '-s', help='stopwords file', default="SmartStopList.txt")
parser.add_argument('--knowledge', '-k', help='knowledge file', default="../../../examples/knowledge/icd11_dict.txt")
args = parser.parse_args()

import os
if not os.path.exists(args.output):
    os.mkdir(args.output)

if __name__=="__main__":
    try:
        LLDA_Main(args.input,args.inputknowledge, args.output,args.stopwords,args.knowledge)
    except Exception as e:
        print(e)

