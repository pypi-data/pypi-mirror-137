import json


import argparse
parser = argparse.ArgumentParser(description='textrank method')
parser.add_argument('--input', '-i', help='input folder', default="../../../examples/data/datasets/ehealthforumQAs.json")
parser.add_argument('--output', '-o', help='output folder', default="../../../examples/data/textrank")
args = parser.parse_args()

import os
if not os.path.exists(args.output):
    os.mkdir(args.output)

corpus = []
tags = []
with open(args.input, 'r', encoding='utf-8') as content_file:
    text = content_file.read()
    text=bytes(text,'utf-8').decode('utf-8','ignore')

for r in json.loads(text):
    question = r['question']
    answer = r['answer']
    tag = r['tags']
    # print(answer)
    corpus.append(question)
    tags.append(tag)

from summa import keywords
fo_result = open(f"{args.output}/result.txt", "w",encoding='utf-8')
fo_raw = open(f"{args.output}/raw.txt", "w",encoding='utf-8')
fo_ref = open(f"{args.output}/ref.txt", "w",encoding='utf-8')

for i,text in enumerate(corpus):
    # keyword extraction
    print("=====doc: "+text)

    ks=keywords.keywords(text,split=True)
    print(ks)
    if len(ks)==0:
        ks=text.split(' ')

    fo_raw.write(corpus[i].replace('\n', ' ').strip() + "\n")
    fo_ref.write(' '.join(tags[i]) + "\n")
    fo_result.write(' '.join(ks) + "\n")

fo_raw.close()
fo_result.close()
fo_ref.close()
