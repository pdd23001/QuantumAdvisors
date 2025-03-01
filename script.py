import json
import random

with open('studentdata.json', 'r') as file:
    data = json.load(file)

classes = data['classes']
students = data['students']

conflict_val = {}

for s in students:
    arr = s['classes']
    for i in range(5):
        for j in range(i,5):
            x = arr[i]
            y = arr[j]
            if x>y:
                x,y=y,x
            if (x,y) not in conflict_val:
                conflict_val[(x,y)]=0
            conflict_val[(x,y)]+=1
        
exams = []

for c in classes:
    exams.append(c['subject']+str(c['number']))
    
days = ["M","T","W","TH","F"]
times = [12,3,6]

slots = []
for d in days:
    for t in times:
        slots.append(d+str(t)+":00")

conflicts = []
for i in range(len(exams)):
    for j in range(i+1,len(exams)):
        conflicts.append({(exams[i],exams[j]): conflict_val.get((i,j),0)})
        
#print(slots)
#print(exams)
#print(conflicts)

def random_arr(m,n):    # size m, into n partitions    
    if m%n!=0:
        raise ValueError
    k = m//n            # partition size
    res = []
    l = list(range(m))
    random.shuffle(l)
    for i in range(n):
        res.append(l[i*k:i*k+k])
    return res

def rate_array(arr):
    s = 0
    n = len(arr)
    for i in range(n):
        for j in range(1,n):
            x = arr[i]
            y = arr[j]
            if x>y:
                x,y=y,x
            s += conflict_val(x,y)
    return s

N = 100000
def find_best():
    best = random_arr()
    score = rate_array(best)
    total = score 
    n = 1
    for i in range(N):
        cur = random_arr()
        cur_score = rate_array(random_arr)
        if cur_score<score:
            score = cur_score
        total += cur_score
        n+=1
    print()
    