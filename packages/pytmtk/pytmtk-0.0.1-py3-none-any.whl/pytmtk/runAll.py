import os
import argparse

def run_and_evaluate(rootfolder,input_data_path,knowlege="",inputknowledge="",stopwords="",method="tfidf"):

    methods = ['word_freq', 'tfidf', 'textrank', 'rake', 'lda', 'llda', 'kcllda']
    files = ['word_freq.py', 'tfidf_main2.py', 'textrank_summa.py', 'rake.py', 'lda.py', 'llda_nltk.py', 'llda_nltk.py']

    # methods=['rake','lda','llda','kcllda']
    # files=['rake.py','lda.py','llda_nltk.py','llda_nltk.py']
    current_path = os.path.dirname(os.path.realpath(__file__))

    for idx, m in enumerate(methods):
        if m!=method:
            continue
        output_folder=rootfolder + "/" + m
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)
        os.chdir(current_path+"/"+m)
        if m in ['kcllda']:
            os.system(f"python {files[idx]} --input {input_data_path} --output {output_folder} --inputknowledge {inputknowledge} --knowledge {knowlege} --stopwords {stopwords}")
        elif m in ['rake']:
            os.system(
                f"python {files[idx]} --input {input_data_path} --output {output_folder}  --stopwords {stopwords}")
        else:
            os.system(f"python {files[idx]} --input {input_data_path} --output {output_folder}")
        os.system(f"python rouge_score.py --output {output_folder}")

    os.chdir(current_path)
    os.system(f"python sum_rouge_avg_result.py --rootfolder {rootfolder} --method {method}")

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='run all method')
    parser.add_argument('--rootfolder', '-r', help='root folder', default=r"pytmtk\examples\data")
    parser.add_argument('--input', '-i', help='input file', default=r"")
    parser.add_argument('--knowledge', '-k', help='knowledge dict', default=r"")
    parser.add_argument('--inputknowledge', '-ik', help='input knowledge', default=r"")
    parser.add_argument('--stopwords', '-s', help='stopwords', default=r"")
    parser.add_argument('--method', '-m', help='method', default=r"tfidf")
    args = parser.parse_args()
    run_and_evaluate(args.rootfolder,args.input,args.knowledge,args.inputknowledge,args.stopwords,args.method)

