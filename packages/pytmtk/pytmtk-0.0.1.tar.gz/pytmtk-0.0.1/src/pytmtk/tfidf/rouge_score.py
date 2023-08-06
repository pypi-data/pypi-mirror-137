from rouge import Rouge

import argparse
parser = argparse.ArgumentParser(description='textrank method')
parser.add_argument('--output', '-o', help='output folder', default="../../../examples/data/tfidf")
args = parser.parse_args()

raws=open(f'{args.output}/raw.txt','r',encoding='utf-8').readlines()
refs=open(f'{args.output}/ref.txt','r',encoding='utf-8').readlines()
result=open(f'{args.output}/result.txt','r',encoding='utf-8').readlines()

rouge = Rouge()

fo_result = open(f"{args.output}/rough_result.txt", "w")
fo_result.write("rouge-1-p"+"\t"+"rouge-1-r"+"\t"+"rouge-1-f"+"\t"+"rouge-2-p"+"\t"+"rouge-2-r"+"\t"+"rouge-2-f"+"\t"+"rouge-L-p"+"\t"+"rouge-L-r"+"\t"+"rouge-L-f"+"\n")

agg_results=[]
for idx,raw in enumerate(raws):
    if raw.strip().__len__()!=0:
        scores = rouge.get_scores(result[idx].strip(), refs[idx].strip())
        print(idx, ':')
        print("result:", result[idx].strip())
        print("ref:", refs[idx].strip())
        print(scores)

        rouge_1_p=scores[0]['rouge-l']['p']
        rouge_1_r = scores[0]['rouge-l']['r']
        rouge_1_f = scores[0]['rouge-l']['f']

        rouge_2_p = scores[0]['rouge-2']['p']
        rouge_2_r = scores[0]['rouge-2']['r']
        rouge_2_f = scores[0]['rouge-2']['f']

        rouge_L_p = scores[0]['rouge-l']['p']
        rouge_L_r = scores[0]['rouge-l']['r']
        rouge_L_f = scores[0]['rouge-l']['f']

        results=[rouge_1_p,rouge_1_r,rouge_1_f,rouge_2_p,rouge_2_r,rouge_2_f,rouge_L_p,rouge_L_r,rouge_L_f]
        agg_results.append(results)
        s=""
        for r in results:
            s+=str(r)+"\t"

        fo_result.write(s.strip()+"\n")

fo_result.close()

avg_results=[]
for j in range(len(agg_results[0])):
    sum=0
    for i in range(len(agg_results)):
        sum=sum+agg_results[i][j]
    avg=sum*1.0/len(agg_results)
    avg_results.append(avg)

# average results
fo_result = open(f"{args.output}/rough_result_avg.txt", "w")
fo_result.write("rouge-1-p"+"\t"+"rouge-1-r"+"\t"+"rouge-1-f"+"\t"+"rouge-2-p"+"\t"+"rouge-2-r"+"\t"+"rouge-2-f"+"\t"+"rouge-L-p"+"\t"+"rouge-L-r"+"\t"+"rouge-L-f"+"\n")
s=""
for r in avg_results:
    s+=str(r)+"\t"
fo_result.write(s+"\n")
fo_result.close()
