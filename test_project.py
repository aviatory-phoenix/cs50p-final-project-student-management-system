import pytest
from project import (calculate_student_rankings,
    calculate_teacher_averages,
    calculate_class_average,
    calculate_student_ranks_in_subjects,
    calculate_overall_rank,
    Student)

def test_calculate_student_rankings():
    # Tests student ranking calculation with sample data
    users_data = [{"grn": "1", "name": "Student A"}, {"grn": "2", "name": "Student B"}]
    students = {
        "1": Student(math=[80, 90], phy=[70, 80]),
        "2": Student(math=[85, 95], phy=[75, 85])
    }
    ranked_students = calculate_student_rankings(users_data, students)
    assert len(ranked_students) == 2
    # Checks that Student B ranks higher than Student A
    assert ranked_students[0]["name"] == "Student B"

def test_calculate_class_average():
    # Tests class average calculation with sample student data
    student_averages = [{"average": 80.0}, {"average": 90.0}, {"average": 85.0}]
    class_avg = calculate_class_average(student_averages)
    assert class_avg == 85.0

def test_calculate_overall_rank():
    # Tests overall rank calculation for a student
    student_row = {"grn": "1"}
    students = {
        "1": Student(math=[80, 90]),
        "2": Student(math=[85, 95]),
        "3": Student(math=[70, 80])
    }
    rank = calculate_overall_rank(student_row, students)
    # Checks that student 1 ranks 2nd
    assert rank == 2

def test_student_average_calculation():
    # Tests Student class average calculation methods
    student = Student(math=[80, 90, None], phy=[70, 80, 90])
    assert student.math_average() == 85.0
    assert student.phy_average() == 80.0
    assert student.average() == 82.5

def test_student_empty_scores():
    # Checks that averages for students who are not enrolled in a subject or
    # have no scores entered yet default to 0
    student = Student(math=[None, None], phy=[])
    assert student.math_average() == 0
    assert student.phy_average() == 0
    assert student.average() == 0

