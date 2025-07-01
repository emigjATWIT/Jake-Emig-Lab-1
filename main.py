
from fastapi import FastAPI
from typing import Optional
import random

app = FastAPI()


students = {
    1: {"name": "Alex", "major": "Computer Networking", "year": "Senior"},
    2: {"name": "Jamie", "major": "Business", "year": "Junior"}
}

cafeteria_menu = {
    "monday": ["Pasta", "Salad", "Soup"],
    "tuesday": ["Tacos", "Rice", "Beans"],
    "wednesday": ["Burger", "Fries", "Soda"],
    "thursday": ["Chicken", "Mashed Potatoes", "Corn"],
    "friday": ["Pizza", "Wings", "Brownies"]
}

quotes = [
    "Keep going, you're almost there!",
    "The grind never stops!",
    "You're smarter than you think!",
    "Don’t watch the clock; do what it does. Keep going."
]

classes = {
    "COMP101": {"title": "Intro to CS", "credits": 3},
    "NET305": {"title": "Advanced Networking", "credits": 4},
    "ENG202": {"title": "English Composition", "credits": 3}
}

resources = [
    "Writing Center", "Tutoring Lab", "Counseling Services", "Career Center"
]


@app.get("/")
def read_root():
    return {"message": "Welcome to the College Life API!"}


@app.get("/motivation")
def get_quote():
    return {"quote": random.choice(quotes)}


@app.get("/student/{student_id}")
def get_student(student_id: int):
    return students.get(student_id, {"error": "Student not found"})


@app.get("/cafeteria/{day}")
def get_menu(day: str):
    return {"menu": cafeteria_menu.get(day.lower(), "No menu for this day")}


@app.get("/class/{course_code}")
def get_class(course_code: str):
    return classes.get(course_code.upper(), {"error": "Class not found"})


@app.get("/gpa")
def calc_gpa(grades: str):
    try:
        grade_points = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'F': 0}
        grade_list = grades.upper().split(",")
        total = sum(grade_points[g] for g in grade_list)
        return {"gpa": round(total / len(grade_list), 2)}
    except:
        return {"error": "Invalid grade input. Use letters A-F separated by commas."}


@app.get("/studytime")
def study_time(hours: float):
    if hours >= 5:
        return {"message": "You're a study machine!"}
    elif hours >= 2:
        return {"message": "Solid effort. Keep it up!"}
    else:
        return {"message": "Might want to hit the books more."}


@app.get("/events")
def get_events(club: Optional[str] = None):
    return {"events": f"Events for {club} club coming soon!" if club else "No club specified."}


@app.get("/sleepcheck")
def sleep_check(hours: float):
    if hours >= 8:
        return {"message": "You're well rested!"}
    elif hours >= 5:
        return {"message": "You're surviving..."}
    else:
        return {"message": "You're running on empty!"}


@app.get("/resources")
def get_resources():
    return {"campus_resources": resources}
