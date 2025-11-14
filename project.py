# Importing the necessary modules
import csv
import sys
from tabulate import tabulate

# The Student class represents a student with their test scores in five subjects
# Each subject stores a list of percentage scores, with None for missing tests
class Student:
    def __init__(self, math=None, phy=None, chem=None, bio=None, cs=None):
        self.math = math or []
        self.phy = phy or []
        self.chem = chem or []
        self.bio = bio or []
        self.cs = cs or []

    # Calculate average for each subject, ignoring None values
    # Returns 0 if no valid scores exist

    def math_average(self):
        valid_scores = [score for score in self.math if score]
        return sum(valid_scores) / len(valid_scores) if valid_scores else 0

    def phy_average(self):
        valid_scores = [score for score in self.phy if score]
        return sum(valid_scores) / len(valid_scores) if valid_scores else 0

    def chem_average(self):
        valid_scores = [score for score in self.chem if score]
        return sum(valid_scores) / len(valid_scores) if valid_scores else 0

    def bio_average(self):
        valid_scores = [score for score in self.bio if score]
        return sum(valid_scores) / len(valid_scores) if valid_scores else 0

    def cs_average(self):
        valid_scores = [score for score in self.cs if score]
        return sum(valid_scores) / len(valid_scores) if valid_scores else 0

    # Calculate overall average across all subjects
    # Only includes subjects with positive averages (a 0 average is assumed to be for a student of the subject with no entered scores)
    # Returns 0 if no subjects have valid averages
    def average(self):
        subject_averages = [
            self.math_average(),
            self.phy_average(),
            self.chem_average(),
            self.bio_average(),
            self.cs_average()
        ]
        valid_averages = [avg for avg in subject_averages if avg > 0]
        return sum(valid_averages) / len(valid_averages) if valid_averages else 0

# Load password data from CSV file into a list of dictionaries
# Each dictionary contains 'name', 'email', and 'password' keys
def load_passwords():
    passwords = []
    with open("passwords.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            passwords.append(row)
    return passwords

# Load user data from CSV file into a list of dictionaries
# Each dictionary contains user information including GRN, name, and subject enrollments
def load_users_data():
    users_data = []
    with open("users.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            users_data.append(row)
    return users_data

# Load subject data from CSV file and convert test scores to percentages
# Returns a dictionary mapping GRN to list of percentage scores for each test
# Missing scores are stored as None values
def load_subject(filename):
    data = {}
    with open(filename) as file:
        reader = csv.DictReader(file)
        for row in reader:
            marks = []
            for test in reader.fieldnames[1:]:
                if row[test]:
                    a, b = map(int, row[test].split("/"))
                    marks.append((a / b) * 100)
                else:
                    marks.append(None)
            data[row["grn"]] = marks
    return data

# Load all subject data files and return them as separate dictionaries
# Each dictionary contains GRN to test score mappings for that subject
def load_all_subjects():
    math_data = load_subject("math.csv")
    phy_data = load_subject("phy.csv")
    chem_data = load_subject("chem.csv")
    bio_data = load_subject("bio.csv")
    cs_data = load_subject("cs.csv")
    return math_data, phy_data, chem_data, bio_data, cs_data

# Create Student objects for all users who have GRNs
# Returns a dictionary mapping GRN to Student objects
# Each Student object contains test scores for enrolled subjects
def load_students(math_data, phy_data, chem_data, bio_data, cs_data, users_data):
    students = {}
    for row in users_data:
        if row["grn"]:
            students[row["grn"]] = Student(
                math_data.get(row["grn"], []),
                phy_data.get(row["grn"], []),
                chem_data.get(row["grn"], []),
                bio_data.get(row["grn"], []),
                cs_data.get(row["grn"], [])
            )
    return students

# Calculate ranked list of all students based on their overall averages
# Returns a list of dictionaries with 'name' and 'average' keys, sorted by average descending
def calculate_student_rankings(users_data, students):
    all_students = []
    for user in users_data:
        if user["grn"]:
            avg = students[user["grn"]].average()
            student_name = user["name"]
            all_students.append({"name": student_name, "average": avg})
    ranked_students = sorted(all_students, key=lambda student: student["average"], reverse=True)
    return ranked_students

# Calculate average scores for each teacher's subject
# Returns a list of dictionaries with teacher names and their subject averages
def calculate_teacher_averages(users_data, math_data, phy_data, chem_data, bio_data, cs_data, students):
    teacher_results = []
    for user in users_data:
        if not user["grn"]:
            for sub in ["math","phy","chem","bio","cs"]:
                if user[sub] == "1":
                    teacher_subject = sub
                    teacher_name = user["name"]
            subject_data = {
                "math": math_data,
                "phy": phy_data,
                "chem": chem_data,
                "bio": bio_data,
                "cs": cs_data
            }[teacher_subject]
            student_averages = []
            for grn in subject_data:
                student_averages.append(getattr(students[grn], f"{teacher_subject}_average")())
            teacher_average = sum(student_averages) / len(student_averages)
            teacher_results.append({"name": teacher_name, "average": teacher_average})
    return teacher_results

# Calculate the average of all student averages in a class
# Takes a list of student dictionaries with 'average' keys
def calculate_class_average(student_averages):
    sum_student_averages = 0
    for student in student_averages:
        sum_student_averages += student["average"]
    return sum_student_averages / len(student_averages)

# Calculate a student's rank in each enrolled subject
# Returns a list of dictionaries with subject, rank, and total students in that subject
def calculate_student_ranks_in_subjects(student_row, enrolled_subjects, users_data, students):
    subject_ranks = []
    for sub in enrolled_subjects:
        student_avg = getattr(students[student_row["grn"]], f"{sub}_average")()
        rank = 1
        total_sub_students = 0
        for user in users_data:
            if user["grn"]:
                if user[f"{sub}"] == "1":
                    total_sub_students += 1
                    avg = getattr(students[user["grn"]], f"{sub}_average")()
                    if avg > student_avg:
                        rank += 1
        subject_ranks.append({"subject": sub, "rank": rank, "total_students": total_sub_students})
    return subject_ranks

# Calculate a student's overall rank among all students
# Compares the student's average against all other students' averages
def calculate_overall_rank(student_row, students):
    student_avg = students[student_row["grn"]].average()
    rank = 1
    for student in students.values():
        avg = student.average()
        if avg > student_avg:
            rank += 1
    return rank

# Initialize global data structures by loading all required data
passwords = load_passwords()
users_data = load_users_data()
math_data, phy_data, chem_data, bio_data, cs_data = load_all_subjects()
students = load_students(math_data, phy_data, chem_data, bio_data, cs_data, users_data)

# Handle user authentication by verifying username and password
# Returns the user's name and email domain for menu display
def login():
    print("\nWelcome! Please enter your username and password to log in")
    print("Press Ctrl+D at any time to exit")
    is_username = False
    while not is_username:
        try:
            username = input("Username: ")
            for password in passwords:
                if username == password["email"]:
                    is_username = True
                    name = password["name"]
                    dotname, domain = password["email"].split("@")
                    correct_password = password["password"]
                    break
            if not is_username:
                print("Invalid email address! Please re-enter")
        except EOFError:
            print("\nExiting...")
            sys.exit()

    is_password = False
    while not is_password:
        try:
            password = input("Password: ")
            if password == correct_password:
                is_password = True
                break
            if not is_password:
                print("Incorrect password! Please re-enter")
        except EOFError:
            print("\nExiting...")
            sys.exit()

    return name, domain

# Print all student averages with their rankings in descending order
def admin_print_student_averages():
    ranked_students = calculate_student_rankings(users_data, students)
    rank = 1
    for student in ranked_students:
        print(f"{rank}. {student['name']} - {student['average']:.2f}%")
        rank += 1

# Print all teacher averages with their names
def admin_print_teacher_averages():
    teacher_results = calculate_teacher_averages(users_data, math_data, phy_data, chem_data, bio_data, cs_data, students)
    number = 1
    for teacher in teacher_results:
        print(f"{number}. {teacher['name']}; Average: {teacher['average']:.2f}")
        number += 1

# Create a new student account by gathering information and writing to CSV files
# Generates email, GRN, and default password for the new student
def admin_create_student_account():
    first_name = input("Enter student's first name: ").strip()
    last_name = input("Enter student's last name: ").strip()
    full_name = f"{first_name} {last_name}"
    email = f"{first_name.lower()}.{last_name.lower()}@student.edu"

    max_grn = 0
    for user in users_data:
        if user["grn"]:
            max_grn = max(max_grn, int(user["grn"]))
    new_grn = str(max_grn + 1)

    print("\nEnroll student in subjects (enter 'y' for yes, 'n' for no):")
    subjects = {"math": "0", "phy": "0", "chem": "0", "bio": "0", "cs": "0"}
    for subject in subjects:
        while True:
            choice = input(f"Enroll in {subject}? (y/n): ").lower()
            if choice in ['y', 'n']:
                subjects[subject] = "1" if choice == 'y' else "0"
                break
            else:
                print("Please enter 'y' or 'n'!")

    with open("users.csv", "a", newline='') as file:
        fieldnames = ["grn", "name", "math", "phy", "chem", "bio", "cs"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow({
            "grn": new_grn,
            "name": full_name,
            "math": subjects["math"],
            "phy": subjects["phy"],
            "chem": subjects["chem"],
            "bio": subjects["bio"],
            "cs": subjects["cs"]
        })

    for subject in subjects:
        if subjects[subject] == "1":
            with open(f"{subject}.csv", 'r') as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames
            with open(f"{subject}.csv", 'a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                new_row = {"grn": new_grn}
                for field in fieldnames[1:]:
                    new_row[field] = ""
                writer.writerow(new_row)

    with open("passwords.csv", "a", newline='') as file:
        fieldnames = ["name", "email", "password"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow({
            "name": full_name,
            "email": email,
            "password": "password123"
        })

    print(f"\nStudent account created successfully!")
    print(f"Name: {full_name}")
    print(f"GRN: {new_grn}")
    print(f"Email: {email}")
    print(f"Default password: password123")

# Admin menu providing options to view student/teacher data or create new accounts
def admin_menu(name):
    print(f"Welcome, {name}! What would you like to do today?")
    while True:
        try:
            print("\nPress Ctrl+D at any time to exit")
            op = input("1. Print all student averages with names and ranks\n2. Print all teacher averages with names\n3. Create a new student account\nEnter choice (1-3): ")
            if op in ["1", "2", "3"]:
                match op:
                    case "1":
                        print("\nAll student averages with ranks:")
                        admin_print_student_averages()
                        print()
                    case "2":
                        print("\nAll teacher averages with names:")
                        admin_print_teacher_averages()
                        print()
                    case "3":
                        print("\nCreating new student account...")
                        admin_create_student_account()
                        print()
            else:
                print("Please choose from the options available!")
        except EOFError:
            print("\nExiting...")
            sys.exit()

# Determine which subject a teacher teaches by checking their user data
def get_teacher_subject(name, users_data):
    for row in users_data:
        if row["name"] == name:
            for sub in ["math","phy","chem","bio","cs"]:
                if row[sub] == "1":
                    return sub
    return None

# Prepare student data for a teacher's specific subject including averages and rankings
def prepare_teacher_data(teacher_subject, math_data, phy_data, chem_data, bio_data, cs_data, students, users_data):
    student_averages = []
    subject_data = {
        "math": math_data,
        "phy": phy_data,
        "chem": chem_data,
        "bio": bio_data,
        "cs": cs_data
    }[teacher_subject]

    for grn in subject_data:
        student_averages.append({"grn": grn, "name": None, "scores": getattr(students[grn], f"{teacher_subject}"), "average": getattr(students[grn], f"{teacher_subject}_average")()})

    for student in student_averages:
        for row in users_data:
            if row["grn"] == student["grn"]:
                student["name"] = row["name"]
                break

    sorted_averages = sorted(student_averages, key=lambda student: student["average"], reverse=True)
    rank = 1
    for student in sorted_averages:
        student["rank"] = rank
        rank += 1

    return student_averages, sorted_averages

# Print all student scores in the teacher's subject in tabular format
def teacher_print_scores(teacher_subject, student_averages):
    headers = ["Student Name"]
    table_data = []
    max_test = 0
    for student in student_averages:
        if len(student["scores"]) > max_test:
            max_test = len(student["scores"])
        row = [student["name"]]
        for score in student["scores"]:
            if score:
                row.append(f"{score:.2f}%")
            else:
                row.append("N/A")
        row.append(f"{student['average']:.2f}%")
        table_data.append(row)
    for i in range(max_test):
        headers.append(f"Test {i+1}")
    headers.append("Average")
    print(f"\nAll {teacher_subject.upper()} Scores:")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

# Find a specific student in the teacher's class by GRN
def teacher_find_student(student_averages):
    is_student = False
    while not is_student:
        try:
            student_id = input("Enter student GRN: ")
            for row in student_averages:
                if student_id == row["grn"]:
                    return row
            print("Please enter a valid student ID!")
        except EOFError:
            print("\nExiting...")
            sys.exit()
    return None

# Teacher menu providing class-wide and individual student operations
def teacher_menu(name):
    print(f"Welcome, {name}! What would you like to do today?")
    teacher_subject = get_teacher_subject(name, users_data)
    student_averages, sorted_averages = prepare_teacher_data(teacher_subject, math_data, phy_data, chem_data, bio_data, cs_data, students, users_data)

    while True:
        try:
            print("\nPress Ctrl+D at any time to exit")
            op = input("FOR THE WHOLE CLASS:\n1.Print all available student test scores in a tabular form\n2.Calculate class average\n3.Calculate class ranks\n4.Display all the students enrolled in your course\nFOR A PARTICULAR STUDENT:\n5.Find student average\n6.Display student rank\nEnter choice (1-6): ")
            if op in ["1","2","3","4","5","6"]:
                match op:
                    case "1":
                        teacher_print_scores(teacher_subject, student_averages)
                    case "2":
                        class_avg = calculate_class_average(student_averages)
                        print(f"The average score of your class is {class_avg:.2f}%")
                        print()
                    case "3":
                        for s in sorted_averages:
                            print(f"{s['rank']}. {s['name']} - {s['average']:.2f}%")
                        print()
                    case "4":
                        number = 1
                        for s in sorted(student_averages, key=lambda s: s["name"]):
                            print(f"{number}. {s['name']}")
                            number += 1
                        print()
                    case "5" | "6":
                        student_row = teacher_find_student(student_averages)
                        if student_row:
                            match op:
                                case "5":
                                    print(f"Name: {student_row['name']}\nAverage: {student_row['average']:.2f}")
                                    print()
                                case "6":
                                    for student in sorted_averages:
                                        if student["grn"] == student_row["grn"]:
                                            print(f"{student['name']} is ranked {student['rank']} out of {len(sorted_averages)} in {teacher_subject} with {student['average']:.2f}%")
                                            print()
                                            break
            else:
                print("Please choose from the options available!")
        except EOFError:
            print("\nExiting...")
            sys.exit()

# Find student data by name in the users_data list
def get_student_row(name, users_data):
    for user in users_data:
        if name == user["name"]:
            return user
    return None

# Get list of subjects a student is enrolled in based on their user data
def get_enrolled_subjects(student_row):
    subjects = ["math","phy","chem","bio","cs"]
    return [sub for sub in subjects if student_row[sub]=="1"]

# Print student's scores in all enrolled subjects in tabular format
def student_print_scores(student_row, enrolled_subjects, math_data, phy_data, chem_data, bio_data, cs_data, students):
    headers = ["Subject"]
    grn = student_row["grn"]
    max_test = 0
    for subject in enrolled_subjects:
        subject_data = {
            "math": math_data,
            "phy": phy_data,
            "chem": chem_data,
            "bio": bio_data,
            "cs": cs_data
        }[subject]
        test_count = len(subject_data[f"{grn}"])
        if test_count > max_test:
            max_test = test_count
    headers.extend([f"Test {i+1}" for i in range(max_test)])
    headers.append("Average")
    table_data = []
    for subject in enrolled_subjects:
        subject_data = {
            "math": math_data,
            "phy": phy_data,
            "chem": chem_data,
            "bio": bio_data,
            "cs": cs_data
        }[subject]
        row = [subject.upper()]
        for score in subject_data[grn]:
            if score:
                row.append(f"{score:.2f}%")
            else:
                row.append("N/A")
        subject_avg = getattr(students[grn], f"{subject}_average")()
        row.append(f"{subject_avg:.2f}%")
        table_data.append(row)
    print(f"\nAll Your Scores - {student_row['name']}:")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

# Print student's subject-wise and overall averages
def student_print_averages(student_row, enrolled_subjects, students):
    print("Your averages are as follows:")
    subject_averages = []
    for sub in enrolled_subjects:
        avg = getattr(students[student_row["grn"]], f"{sub}_average")()
        print(f"{sub}: {avg:.2f}%")
        subject_averages.append(avg)
    overall_avg = students[student_row["grn"]].average()
    print(f"Overall average: {overall_avg:.2f}%")

# Print student's ranks in each subject and overall rank
def student_print_ranks(student_row, enrolled_subjects, users_data, students):
    print("Your ranks are as follows:")
    subject_ranks = calculate_student_ranks_in_subjects(student_row, enrolled_subjects, users_data, students)
    for rank_info in subject_ranks:
        print(f"{rank_info['subject']}: Rank {rank_info['rank']} out of {rank_info['total_students']}")
    overall_rank = calculate_overall_rank(student_row, students)
    print(f"Overall: Rank {overall_rank} out of {len(students)}")

# Student menu providing access to personal academic information
def student_menu(name):
    print(f"Welcome, {name}! What would you like to do today?")
    student_row = get_student_row(name, users_data)
    enrolled_subjects = get_enrolled_subjects(student_row)

    while True:
        try:
            print("\nPress Ctrl+D at any time to exit")
            op = input("1. Print a list of all your courses\n2. Calculate course-wise and overall averages\n3. Print all your scores and averages in a tabular format\n4. Display your rank in each subject and overall\nEnter choice (1-4): ")
            if op in ["1","2","3","4"]:
                match op:
                    case "1":
                        print("You are enrolled in the following courses:")
                        number = 1
                        for sub in enrolled_subjects:
                            print(f"{number}. {sub}")
                            number += 1
                        print()
                    case "2":
                        student_print_averages(student_row, enrolled_subjects, students)
                        print()
                    case "3":
                        student_print_scores(student_row, enrolled_subjects, math_data, phy_data, chem_data, bio_data, cs_data, students)
                        print()
                    case "4":
                        student_print_ranks(student_row, enrolled_subjects, users_data, students)
                        print()
            else:
                print("Please choose from the options available!")
        except EOFError:
            print("\nExiting...")
            sys.exit()

# Directs user to appropriate menu based on their email domain
def launch_menu(name, domain):
    match domain:
        case "admin.edu":
            admin_menu(name)
        case "teacher.edu":
            teacher_menu(name)
        case "student.edu":
            student_menu(name)

# Main program handling login and menu navigation
def main():
    try:
        name, domain = login()
        launch_menu(name, domain)
    except EOFError:
        print("\nExiting...")
        sys.exit()

# Calling the main function 
if __name__ == "__main__":
    main()
