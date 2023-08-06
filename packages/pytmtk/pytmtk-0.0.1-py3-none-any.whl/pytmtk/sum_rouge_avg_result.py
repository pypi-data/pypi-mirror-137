import os
import argparse

parser = argparse.ArgumentParser(description='run all method')
parser.add_argument('--rootfolder', '-r', help='root folder', default="../../../examples/data")
parser.add_argument('--method', '-m', help='method', default="tfidf")
args = parser.parse_args()

methods=['word_freq','tfidf','textrank','rake','lda','llda','kcllda']

print("summary of rouge metrics for methods")

print("method\trouge-1-p\trouge-1-r\trouge-1-f\trouge-2-p\trouge-2-r\trouge-2-f\trouge-L-p\trouge-L-r\trouge-L-f")


for method in methods:
    if method!=args.method:
        continue
    # print("------------"+method+"----------------")
    rough_path=args.rootfolder+"/"+method+'/rough_result_avg.txt'
    lines=open(rough_path,'r',encoding='utf-8').readlines()
    avg_results=lines[1].strip().split('\t')[:9]
    print(method+"\t"+'\t'.join(avg_results))
