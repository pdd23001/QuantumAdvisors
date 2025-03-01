import pandas as pd
import random
import faker
from collections import defaultdict

fake = faker.Faker()

# -------------------------------
# 2️⃣ Generate Course Data
# -------------------------------
course_levels = [1000, 2000, 3000, 4000]
course_difficulty = ["Easy", "Medium", "Hard"]

courses = {
    "CSE1010": {"name": "Intro to CS", "level": 1000, "prerequisites": []},
    "CSE2010": {"name": "Data Structures", "level": 2000, "prerequisites": ["CSE1010"]},
    "CSE2100": {"name": "Discrete Math", "level": 2000, "prerequisites": ["MATH1131"]},
    "CSE3500": {"name": "Algorithms", "level": 3000, "prerequisites": ["CSE2010", "CSE2100"]},
    "MATH1131": {"name": "Calculus I", "level": 1000, "prerequisites": []},
    "MATH2210": {"name": "Linear Algebra", "level": 2000, "prerequisites": ["MATH1131"]},
    "STAT3025": {"name": "Probability & Stats", "level": 3000, "prerequisites": ["MATH2210"]},
}

course_list = []
for course_id, details in courses.items():
    course_list.append({
        "course_id": course_id,
        "name": details["name"],
        "level": details["level"],
        "prerequisites": details["prerequisites"],
        "credits": random.choice([3, 4]),
        "difficulty": random.choice(course_difficulty),
        "semester_offered": random.choice(["Fall", "Spring", "Both"]),
    })

df_courses = pd.DataFrame(course_list)
df_courses.to_csv("courses.csv", index=False)
print("✅ Course data generated!")


# -------------------------------
# 1️⃣ Generate Student Data
# -------------------------------
NUM_STUDENTS = 500  # Adjust as needed

majors = ["Computer Science", "Finance", "Mathematics", "Biology", "Engineering"]
academic_standing = ["Good", "Probation", "Suspended"]

students = []
for i in range(1, NUM_STUDENTS + 1):
    # Generate random GPA and academic standing
    gpa = round(random.uniform(2.0, 4.0), 2)
    standing = random.choice(academic_standing)
    
    # Initialize completed_courses
    completed_courses = []
    
    # Simulate course progression based on semester
    semester = random.randint(1, 6)  # Randomly assign a semester (1-6)
    
    if semester >= 1:
        # Semester 1-2: Take 1000-level courses
        available_courses = [course_id for course_id, details in courses.items() if details["level"] == 1000]
        completed_courses.extend(random.sample(available_courses, min(2, len(available_courses))))
    
    if semester >= 3:
        # Semester 3-4: Take 2000-level courses (if prerequisites are met)
        available_courses = [course_id for course_id, details in courses.items() 
                            if details["level"] == 2000 and 
                            all(prereq in completed_courses for prereq in details["prerequisites"])]
        completed_courses.extend(random.sample(available_courses, min(2, len(available_courses))))
    
    if semester >= 5:
        # Semester 5-6: Take 3000-level courses (if prerequisites are met)
        available_courses = [course_id for course_id, details in courses.items() 
                            if details["level"] == 3000 and 
                            all(prereq in completed_courses for prereq in details["prerequisites"])]
        completed_courses.extend(random.sample(available_courses, min(2, len(available_courses))))
    
    # Append student data
    students.append({
        "student_id": i,
        "name": fake.name(),
        "major": random.choice(majors),
        "gpa": gpa,
        "standing": standing,
        "completed_courses": completed_courses,
        "preferred_courses": [],
        "semester": semester  # Add semester to track progress
    })




# -------------------------------
# 3️⃣ Generate Student Course Progression
# -------------------------------
grades = ["A", "B", "C", "D", "F", "W"]
NUM_SEMESTERS = 6  # Simulating multiple semesters

student_courses = []

for student in students:
    completed_courses = []
    major = student["major"]
    
    for semester in range(1, NUM_SEMESTERS + 1):
        available_courses = [c for c in courses if courses[c]["level"] <= 1000]  # Start with 1000-level

        # Unlock next levels if prerequisites are met
        for course_id, details in courses.items():
            if all(prereq in completed_courses for prereq in details["prerequisites"]):
                available_courses.append(course_id)

        if not available_courses:
            continue

        # Select random courses (2-4 per semester)
        taken_courses = random.sample(available_courses, min(4, len(available_courses)))
        
        for course in taken_courses:
            student_courses.append({
                "student_id": student["student_id"],
                "course_id": course,
                "grade": random.choice(grades),
                "semester": f"Semester {semester}"
            })
            completed_courses.append(course)

df_student_courses = pd.DataFrame(student_courses)
df_student_courses.to_csv("student_courses.csv", index=False)
print("✅ Student course progression data generated!")


# -------------------------------
# 4️⃣ Generate Course Pathway Patterns
# -------------------------------
pathways = defaultdict(list)

for student in students:
    student_id = student["student_id"]
    completed_courses = df_student_courses[df_student_courses["student_id"] == student_id]["course_id"].tolist()

    if len(completed_courses) > 1:
        for i in range(len(completed_courses) - 1):
            pathways[tuple(completed_courses[:i + 1])].append(completed_courses[i + 1])

# Create dataset for ML training
ml_data = []
for path, next_courses in pathways.items():
    ml_data.append({
        "completed_courses": list(path),
        "next_recommended": list(set(next_courses))
    })

df_ml_data = pd.DataFrame(ml_data)
df_ml_data.to_csv("course_pathways.csv", index=False)
print("✅ Course pathways data generated!")
