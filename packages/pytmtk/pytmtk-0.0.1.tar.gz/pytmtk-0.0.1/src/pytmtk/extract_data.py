import json
text=''

with open('datasets/ehealthforumQAs.json', 'r') as content_file:
    text = content_file.read()

#print(text)

data=json.loads(text)

for r in data:
    question=r['question']
    answer=r['answer']
    tags=r['tags']
    print(answer)

