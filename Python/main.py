"""
main.py — Course Registration System (Python)
Use case: Enroll in Course (with full validation flow)

Run: python main.py
"""

from data_manager import load_data, save_data
from enrollment_service import enroll_student, drop_course


# ── helpers ──────────────────────────────────────────────────────────────────

def print_header(title: str) -> None:
    width = 50
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


def print_catalog(courses: dict) -> None:
    print_header("Course Catalog")
    print(f"{'ID':<10} {'Name':<28} {'Slots':<6} {'Time':<18} {'Prereqs'}")
    print("-" * 80)
    for c in courses.values():
        seats = f"{c['enrolled']}/{c['capacity']}"
        prereqs = ", ".join(c["prerequisites"]) if c["prerequisites"] else "None"
        print(f"{c['id']:<10} {c['name']:<28} {seats:<6} {c['timeSlot']:<18} {prereqs}")


def print_student_info(student: dict, courses: dict) -> None:
    print_header(f"Profile: {student['name']}")
    print(f"  ID      : {student['id']}")
    print(f"  Email   : {student['email']}")
    print(f"  Balance : ${student['balance']:,.2f}")
    enrolled = student.get("enrolledCourses", [])
    if enrolled:
        print(f"\n  Enrolled courses:")
        for cid in enrolled:
            c = courses.get(cid, {})
            slot = next((s["timeSlot"] for s in student["schedule"] if s["courseId"] == cid), "")
            print(f"    • {cid}: {c.get('name', '?')}  [{slot}]")
    else:
        print("  Enrolled courses: none")
    completed = student.get("completedCourses", [])
    print(f"\n  Completed: {', '.join(completed) if completed else 'none'}")


# ── menus ─────────────────────────────────────────────────────────────────────

def student_menu(student: dict, students: dict, courses: dict) -> None:
    while True:
        print_header(f"Student Menu — {student['name']}")
        print("  [1] View catalog")
        print("  [2] Enroll in course")
        print("  [3] Drop a course")
        print("  [4] View my schedule / profile")
        print("  [5] Billing summary")
        print("  [6] Save & logout")
        choice = input("\nSelect option: ").strip()

        if choice == "1":
            print_catalog(courses)

        elif choice == "2":
            print_catalog(courses)
            code = input("\nEnter course ID to enroll in: ").strip().upper()
            ok, msg = enroll_student(student["id"], code, students, courses)
            print(f"\n{'✓' if ok else '✗'} {msg}")

        elif choice == "3":
            enrolled = student.get("enrolledCourses", [])
            if not enrolled:
                print("\nYou have no enrolled courses to drop.")
            else:
                print("\nYour enrolled courses:", ", ".join(enrolled))
                code = input("Enter course ID to drop: ").strip().upper()
                ok, msg = drop_course(student["id"], code, students, courses)
                print(f"\n{'✓' if ok else '✗'} {msg}")

        elif choice == "4":
            print_student_info(student, courses)

        elif choice == "5":
            print_header("Billing Summary")
            print(f"  Student : {student['name']}")
            print(f"  Balance : ${student['balance']:,.2f}")

        elif choice == "6":
            save_data(students, courses)
            print("\nData saved. Goodbye!")
            break
        else:
            print("Invalid option.")


def admin_menu(students: dict, courses: dict) -> None:
    while True:
        print_header("Admin Menu")
        print("  [1] View catalog")
        print("  [2] View all students")
        print("  [3] Add course")
        print("  [4] Save & logout")
        choice = input("\nSelect option: ").strip()

        if choice == "1":
            print_catalog(courses)

        elif choice == "2":
            print_header("All Students")
            for s in students.values():
                enrolled = ", ".join(s.get("enrolledCourses", [])) or "none"
                print(f"  {s['id']}  {s['name']:<22}  enrolled: {enrolled}  balance: ${s['balance']:,.2f}")

        elif choice == "3":
            print_header("Add Course")
            cid = input("Course ID       : ").strip().upper()
            if cid in courses:
                print("Course ID already exists.")
                continue
            name = input("Course name     : ").strip()
            credits = int(input("Credits         : ").strip())
            capacity = int(input("Capacity        : ").strip())
            time_slot = input("Time slot (e.g. MWF 9:00-10:00): ").strip()
            prereqs_raw = input("Prerequisites (comma-separated, or blank): ").strip()
            prereqs = [p.strip().upper() for p in prereqs_raw.split(",") if p.strip()]
            cost = float(input("Cost per credit : ").strip())
            courses[cid] = {
                "id": cid, "name": name, "credits": credits,
                "capacity": capacity, "enrolled": 0,
                "prerequisites": prereqs, "timeSlot": time_slot,
                "costPerCredit": cost,
            }
            print(f"Course {cid} added.")

        elif choice == "4":
            save_data(students, courses)
            print("\nData saved. Goodbye!")
            break
        else:
            print("Invalid option.")


# ── login ─────────────────────────────────────────────────────────────────────

def login(students: dict, courses: dict) -> None:
    while True:
        print_header("Login Menu")
        print("  [1] Student login")
        print("  [2] Admin login")
        print("  [3] Exit")
        choice = input("\nSelect option: ").strip()

        if choice == "1":
            sid = input("Enter student ID (or 'new' to register): ").strip()
            if sid.lower() == "new":
                sid = input("Choose a student ID: ").strip().upper()
                if sid in students:
                    print("ID already taken.")
                    continue
                name = input("Full name : ").strip()
                email = input("Email     : ").strip()
                students[sid] = {
                    "id": sid, "name": name, "email": email,
                    "completedCourses": [], "enrolledCourses": [],
                    "schedule": [], "balance": 0.0,
                }
                print(f"Profile created for {name}.")
            student = students.get(sid.upper())
            if student is None:
                print("Student ID not found.")
                continue
            student_menu(student, students, courses)

        elif choice == "2":
            pw = input("Admin password: ").strip()
            if pw != "admin123":
                print("Incorrect password.")
                continue
            admin_menu(students, courses)

        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


# ── entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    print_header("Course Registration System")
    students, courses = load_data()
    print("  Data loaded successfully.")
    login(students, courses)


if __name__ == "__main__":
    main()
