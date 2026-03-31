"""
enrollment_service.py
Implements the Enroll-in-Course validation flow:
  1. Student ID found?
  2. Course code found?
  3. Already enrolled?
  4. Course full? (seats check)
  5. All prerequisites met?
  6. Time conflict? (TimeSlotOverlaps)
  7. Enroll student -> update Student + Course maps
"""


def _parse_time_slot(slot: str) -> tuple[set[str], int, int]:
    """Parse a time slot string like 'MWF 9:00-10:00' into (days_set, start_min, end_min)."""
    try:
        days_str, time_range = slot.split(" ")
        start_str, end_str = time_range.split("-")

        days = set(days_str)  # e.g. {'M', 'W', 'F'}

        def to_minutes(t: str) -> int:
            h, m = t.split(":")
            return int(h) * 60 + int(m)

        return days, to_minutes(start_str), to_minutes(end_str)
    except Exception:
        return set(), 0, 0


def time_slot_overlaps(slot_a: str, slot_b: str) -> bool:
    """Return True if two time slot strings overlap on any shared day."""
    days_a, start_a, end_a = _parse_time_slot(slot_a)
    days_b, start_b, end_b = _parse_time_slot(slot_b)

    if not days_a & days_b:
        return False
    return start_a < end_b and start_b < end_a


def enroll_student(
    student_id: str,
    course_id: str,
    students: dict,
    courses: dict,
) -> tuple[bool, str]:
    """
    Attempt to enroll a student in a course.
    Returns (success: bool, message: str).
    """

    # 1. Student ID found?
    student = students.get(student_id)
    if student is None:
        return False, f"Student ID '{student_id}' not found."

    # 2. Course code found?
    course = courses.get(course_id)
    if course is None:
        return False, f"Course code '{course_id}' not found."

    # 3. Already enrolled?
    if course_id in student.get("enrolledCourses", []):
        return False, f"You are already enrolled in {course_id} ({course['name']})."

    # 4. Course full?
    if course["enrolled"] >= course["capacity"]:
        return False, f"{course_id} ({course['name']}) is full ({course['capacity']}/{course['capacity']} seats)."

    # 5. Prerequisites met?
    completed = set(student.get("completedCourses", []))
    missing = [p for p in course.get("prerequisites", []) if p not in completed]
    if missing:
        return False, f"Missing prerequisites for {course_id}: {', '.join(missing)}."

    # 6. Time conflict?
    new_slot = course.get("timeSlot", "")
    for existing in student.get("schedule", []):
        if time_slot_overlaps(new_slot, existing["timeSlot"]):
            return False, (
                f"Time conflict: {course_id} ({new_slot}) overlaps with "
                f"{existing['courseId']} ({existing['timeSlot']})."
            )

    # 7. Enroll — update Student + Course maps
    student.setdefault("enrolledCourses", []).append(course_id)
    student.setdefault("schedule", []).append(
        {"courseId": course_id, "timeSlot": new_slot}
    )
    cost = course["credits"] * course["costPerCredit"]
    student["balance"] = round(student.get("balance", 0) + cost, 2)
    course["enrolled"] += 1

    return True, (
        f"Successfully enrolled in {course_id}: {course['name']}. "
        f"Tuition charged: ${cost:,.2f}. New balance: ${student['balance']:,.2f}."
    )


def drop_course(
    student_id: str,
    course_id: str,
    students: dict,
    courses: dict,
) -> tuple[bool, str]:
    """Drop a student from a course."""
    student = students.get(student_id)
    if student is None:
        return False, f"Student ID '{student_id}' not found."

    course = courses.get(course_id)
    if course is None:
        return False, f"Course code '{course_id}' not found."

    if course_id not in student.get("enrolledCourses", []):
        return False, f"You are not enrolled in {course_id}."

    student["enrolledCourses"].remove(course_id)
    student["schedule"] = [s for s in student.get("schedule", []) if s["courseId"] != course_id]
    refund = course["credits"] * course["costPerCredit"]
    student["balance"] = round(student.get("balance", 0) - refund, 2)
    course["enrolled"] -= 1

    return True, (
        f"Dropped {course_id}: {course['name']}. "
        f"Refund applied: ${refund:,.2f}. New balance: ${student['balance']:,.2f}."
    )
