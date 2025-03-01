import pandas as pd
import ast
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load data
course_pathways = pd.read_csv('./data/course_pathways.csv')
courses = pd.read_csv('./data/courses.csv')
student_courses = pd.read_csv('./data/student_courses.csv')
students = pd.read_csv('./data/students.csv')

# Load the GPT-2 model and tokenizer
model_name = "gpt2"  # You can use "gpt2-medium" or "gpt2-large" for better performance
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

map = {3:"tjb20007",5:"pdd12345",7:"abc12345"}

def recommend_courses(student_id):
    # Get student info
    student_info = students[students["student_id"] == student_id]

    # Debugging: print the length of the dataframe and check if it's empty
    print(f"✅ Student Data Length for ID {student_id}: {len(student_info)}")
    
    if student_info.empty:
        return ["Student not found."]
    
    student_info = student_info.iloc[0]  # Get the first match
    completed_courses = ast.literal_eval(student_info["completed_courses"]) if pd.notna(student_info["completed_courses"]) else []

    # Debugging: print the student's completed courses
    print(f"✅ Student Found! Completed Courses: {completed_courses}")

    # Get student grades
    student_grades = student_courses[student_courses["student_id"] == student_id]
    student_grades_dict = dict(zip(student_grades["course_id"], student_grades["grade"]))

    # Debugging: print out the courses and grades
    print(f"✅ Student has grades for the following courses: {list(student_grades_dict.keys())}")

    # Convert grades to numerical for comparison
    grade_mapping = {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}
    student_grades_dict = {k: grade_mapping.get(v, 0.0) for k, v in student_grades_dict.items()}

    # Filter courses where prerequisites are met and exclude completed courses
    eligible_courses = []

    for _, course in courses.iterrows():
        prerequisites = ast.literal_eval(course["prerequisites"]) if pd.notna(course["prerequisites"]) else []

        # Check if prerequisites were passed with a C or higher (numerically >= 2.0)
        if all(prereq in student_grades_dict and student_grades_dict[prereq] >= 2.0 for prereq in prerequisites):
            # Exclude courses that the student has already taken
            if course["course_id"] not in completed_courses:
                eligible_courses.append(course["name"])

    if not eligible_courses:
        print("⚠️ No courses found! Check prerequisites and grades.")
        return ["No suitable courses found."]
    
    return eligible_courses

def generate_recommendation(student_id):
    # Get eligible courses
    eligible_courses = recommend_courses(student_id)

    if eligible_courses == ["Student not found."] or eligible_courses == ["No suitable courses found."]:
        return eligible_courses[0]  # Return the error message directly

    # Prepare the prompt for GPT-2
    if student_id in map:
        student_id = map[student_id]
    prompt = (
        f"As an AI academic advisor, I recommend the following courses for student {student_id}:\n"
        f"Eligible Courses: {', '.join(eligible_courses)}\n"
        f"These courses are recommended based on the student's completed courses and academic performance. "
        f"Here is a personalized recommendation:\n"
    )

    # Tokenize the prompt
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)

    # Generate the response
    outputs = model.generate(
        inputs["input_ids"],
        max_length=200,  # Adjust the length of the response
        num_return_sequences=1,  # Generate one response
        no_repeat_ngram_size=2,  # Avoid repeating phrases
        top_p=0.9,  # Use nucleus sampling
        top_k=50,  # Limit the number of tokens to consider
        temperature=0.7,  # Control randomness
        do_sample=True,  # Enable sampling for more diverse responses
    )

    # Decode the generated text
    recommendation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return recommendation

def chatbot():
    print("Welcome to the AI Academic Advisor!")
    student_id = input("Enter your student ID: ")

    recommendation = generate_recommendation(int(student_id))
    print("How can I help you today?")
    str1=input()
    print("\nAI Recommendation:")
    print(recommendation)
    
def chatbot2(id):
    student_id = id
    recommendation = generate_recommendation(int(student_id))
    return {"response": recommendation}
    
# Run the chatbot
#chatbot()