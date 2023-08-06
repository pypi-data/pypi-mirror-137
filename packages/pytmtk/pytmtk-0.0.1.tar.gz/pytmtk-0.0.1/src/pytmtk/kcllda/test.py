import os
print(os.path.abspath(os.curdir))
os.chdir(os.path.abspath(os.curdir))
os.system("python rouge_score.py")