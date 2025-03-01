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
        for j in range(i+1,5):
            x = arr[i]
            y = arr[j]
            if x>y:
                x,y=y,x
            if (x,y) not in conflict_val:
                conflict_val[(x,y)]=0
            conflict_val[(x,y)]+=1
        
exams = []
"""
for c in classes:
    exams.append(c['subject']+str(c['number']))
    
days = ["M","T","W","TH","F"]
times = [10,12,2,4,6,8]

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
"""

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

def rate_array(arr,flag=0):
    s = 0
    n = len(arr[0])
    for k in range(len(arr)):
        for i in range(n):
            for j in range(i+1,n):
                x = arr[k][i]
                y = arr[k][j]
                if x>y:
                    x,y=y,x
                s += conflict_val.get((x,y),0)

    return s

N = 1000
def find_best():
    best = random_arr(54,18)
    best_score = rate_array(best)
    total = best_score 
    n = 1
    for i in range(N):
        cur = random_arr(54,18)
        cur_score = rate_array(cur)
        if cur_score<best_score:
            best_score = cur_score
        total += cur_score
        n+=1
    res = f"Optimal:\n"
    for i in range(len(best)):
        res += "{"
        res += str([str(classes[best[i][j]]['subject'])+str(classes[best[i][j]]['number']) for j in range(len(best[i]))])
        res += "}"
    res += "\nBest: " + str(best_score/100)
    
    return {'response':res}
