import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
STUDENTS_FILE = os.path.join(DATA_DIR, "students.json")
COURSES_FILE = os.path.join(DATA_DIR, "courses.json")


def load_data() -> tuple[dict, dict]:
    """Load students and courses from JSON files. Returns (students_map, courses_map)."""
    with open(STUDENTS_FILE, "r") as f:
        students_list = json.load(f)
    with open(COURSES_FILE, "r") as f:
        courses_list = json.load(f)

    students = {s["id"]: s for s in students_list}
    courses = {c["id"]: c for c in courses_list}
    return students, courses


def save_data(students: dict, courses: dict) -> None:
    """Persist students and courses back to JSON files."""
    with open(STUDENTS_FILE, "w") as f:
        json.dump(list(students.values()), f, indent=2)
    with open(COURSES_FILE, "w") as f:
        json.dump(list(courses.values()), f, indent=2)
