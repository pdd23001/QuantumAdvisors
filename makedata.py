import json
import random

def randletter():
    return chr(random.randint(97,122))

def randomItem(arr):
    return arr[random.randint(0,len(arr)-1)]

def randomClass():
    x = random.random()
    if x < .6:
        return random.randint(0,10)
    if x < .9:
        return random.randint(11,30)
    else:
        return random.randint(31,44)
    
class Class:
    
    def __init__(self, subject, number, building, prof, classId, time):
        self.subject = subject
        self.number = number
        self.building = building
        self.prof = prof
        self.classId = classId
        self.time = time
    
    def todict(self):
        return self.__dict__
        
class Student:
    
    def __init__(self, netid, classes, year):
        self.netid = netid
        self.classes = classes
        self.year = year
        
    def todict(self):
        return self.__dict__
        
subjects = [
    "MATH","CSE","ACCT","ANSC","BIOL","CHEM","BUSI","ART","FNCE","MENT","CHIN","COMM","ERTH","ECON","GERM","HIST"
 ,"LING","MKTG","MSE","MUSI","PHYS","PHIL","STAT","WGSS","PATH","NURS","NRE","AFRI"]

first_names = [
    "Aaron", "Abigail", "Adam", "Alexander", "Alice", "Amanda", "Andrew", "Angela", 
    "Anthony", "Benjamin", "Brandon", "Brian", "Caroline", "Charlotte", "Christopher", 
    "Daniel", "David", "Diana", "Dominic", "Edward", "Eleanor", "Elizabeth", "Emily", 
    "Emma", "Ethan", "Evelyn", "Gabriel", "Grace", "Hannah", "Isabella", "Jacob", 
    "James", "Jennifer", "John", "Jonathan", "Joseph", "Katherine", "Kevin", "Laura", 
    "Lucas"
]

last_names = [
    "Anderson", "Bailey", "Baker", "Bennett", "Brown", "Campbell", "Carter", "Clark", 
    "Collins", "Cooper", "Cox", "Davis", "Diaz", "Edwards", "Evans", "Flores", 
    "Foster", "Garcia", "Gonzalez", "Green", "Hall", "Harris", "Hill", "Hughes", 
    "Jackson", "Jenkins", "Johnson", "Kelly", "King", "Lee", "Lewis", "Martinez", 
    "Miller", "Mitchell", "Morgan", "Nelson", "Parker", "Perez", "Richardson", "Roberts"
]

buildings = [
    "BUSN", "SHH", "MCHU", "ITE", "GANT", "TLS", "GENT", "CHEM", "DRMU", "E2", "PBS",
    "MUSB", "MONT", "AUST", "BCH"
]


classes = []

for i in range(45):
    subject = randomItem(subjects)
    num = 10*random.randint(100,399)
    building = randomItem(buildings)
    prof = randomItem(first_names)+" " + randomItem(last_names)
    time = random.randint(9,18)
    classes.append(Class(subject, num, building, prof, i, time))

users = []

for i in range(500):
    lets = randletter()+randletter()+randletter()
    nums = str(random.randint(10000,29999))
    netid = lets+nums
    myclasses = set()
    while len(myclasses)<5:
        x = randomClass()
        myclasses.add(randomClass())
    myclasses = list(myclasses)
    year = random.randint(2025,2029)
    users.append(Student(netid, myclasses,year))

data = {
    "classes": [c.__dict__ for c in classes],
    "students": [s.__dict__ for s in users]
}  

with open("studentdata.json", "w") as json_file:
    json.dump({}, json_file, indent=4)  # Overwrites with an empty JSON object
    
with open("studentdata.json", "w") as json_file:
    json.dump(data, json_file, indent=4)