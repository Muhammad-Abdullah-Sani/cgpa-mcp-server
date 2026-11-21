grade_bands = [
    (85, 4.0), (80, 3.7), (75, 3.3), (70, 3.0), (65, 2.7),
    (61, 2.3), (58, 2.0), (55, 1.7), (50, 1.0), (0, 0.0),
]

courses = {
    1: [
        ("MS-251", "Probability & Statistics", 3.0),
        ("GE-160", "Applications of ICT", 3.0),
        ("GE-169", "Applied Physics", 3.0),
        ("GE-167", "Discrete Structures", 3.0),
        ("HQ-001", "Quran Translation I", 0.5),
        ("GE-190", "Functional English", 3.0),
    ],
    2: [
        ("CC-112", "Programming Fundamentals", 3.0),
        ("CC-112-L", "Programming Fundamentals Lab", 1.0),
        ("CC-110", "Digital Logic Design", 2.0),
        ("CC-110-L", "Digital Logic Design Lab", 1.0),
        ("MS-252", "Linear Algebra", 3.0),
        ("GE-191", "Expository Writing", 3.0),
        ("GE-163", "Islamic Studies", 2.0),
        ("HQ-002", "Quran Translation II", 0.5),
    ],
    3: [
        ("CC-211", "Object Oriented Programming", 3.0),
        ("CC-211-L", "Object Oriented Programming Lab", 1.0),
        ("CC-215", "Database Systems", 3.0),
        ("CC-215-L", "Database Systems Lab", 1.0),
        ("CC-210", "Computer Organization & Assembly Language", 3.0),
        ("GE-162", "Calculus & Analytical Geometry", 3.0),
        ("GE-192", "Introduction to Management", 2.0),
        ("HQ-003", "Quran Translation III", 0.5),
    ],
    4: [
        ("CC-213", "Data Structures", 3.0),
        ("CC-213-L", "Data Structures Lab", 1.0),
        ("CC-312", "Information Security", 3.0),
        ("CC-214", "Computer Networks", 3.0),
        ("CC-212", "Software Engineering", 3.0),
        ("DC-220", "Advanced Database Management Systems", 3.0),
        ("HQ-004", "Quran Translation IV", 0.5),
    ],
    5: [
        ("CC-313", "Analysis of Algorithms", 3.0),
        ("CC-310", "Artificial Intelligence", 3.0),
        ("DC-320", "Theory of Automata and Formal Languages", 3.0),
        ("DC-321", "Human Computer Interaction", 3.0),
        ("DC-322", "Computer Architecture", 3.0),
        ("EC-330", "Web Technologies / Elective", 3.0),
        ("HQ-005", "Quran Translation V", 0.5),
    ],
    6: [
        ("CC-311", "Operating Systems", 3.0),
        ("EC-333", "Mobile Application Development / Elective", 3.0),
        ("EC-324", "Software Construction & Development / Elective", 3.0),
        ("EC-335", "Machine Learning / Elective", 3.0),
        ("EC-334", "Game Design and Development / Elective", 3.0),
        ("MS-253", "Multivariable Calculus", 3.0),
        ("HQ-006", "Quran Translation VI", 0.5),
    ],
    7: [
        ("CC-411", "Final Year Project I", 2.0),
        ("DC-328", "Parallel & Distributed Computing", 3.0),
        ("EC-345", "Computer Vision / Elective", 3.0),
        ("EC-425", "Software Quality Engineering / Elective", 3.0),
        ("MS-254", "Technical and Business Writing", 3.0),
        ("GE-263", "Entrepreneurship", 2.0),
        ("GE-262", "Professional Practices", 2.0),
        ("HQ-007", "Quran Translation VII", 0.5),
    ],
    8: [
        ("CC-412", "Final Year Project II", 4.0),
        ("DC-421", "Compiler Construction", 3.0),
        ("UE-272", "Introduction to Marketing", 3.0),
        ("GE-168", "Ideology and Constitution of Pakistan", 2.0),
        ("GE-363", "Civics and Community Engagement", 2.0),
        ("HQ-008", "Quran Translation VIII", 0.5),
    ],
}


def marks_to_grade_points(marks: int) -> float | str:
    """
    Convert numeric marks (0-100) into PUCIT grade points using the official
    grade band. Use this whenever a student gives you raw marks for a course
    and you need the grade point before computing a GPA.
    """
    if not (0 <= marks <= 100):
        return "Error: marks must be between 0 and 100"
    for threshold, points in grade_bands:
        if marks >= threshold:
            return points


def calculate_semester_gpa(grade_points: list[float], credit_hours: list[float]) -> float | str:
    """
    Calculate one semester's credit-weighted GPA from a list of grade points
    and the matching list of credit hours. Use this once you have grade
    points (not raw marks) and credit hours for every course in a semester.
    """
    if len(grade_points) != len(credit_hours):
        return "Error: grade_points and credit_hours must be the same length"
    if not credit_hours or sum(credit_hours) == 0:
        return "Error: total credit hours cannot be zero"
    total_points = sum(gp * ch for gp, ch in zip(grade_points, credit_hours))
    return round(total_points / sum(credit_hours), 4)


def calculate_new_cgpa(current_cgpa: float, completed_credit_hours: float,
                        semester_gpa: float, semester_credit_hours: float) -> float | str:
    """
    Project a student's new overall CGPA after adding one completed semester
    to their existing record. Use this when you already know the current
    CGPA, hours completed so far, and the GPA just earned this semester.
    """
    if completed_credit_hours < 0 or semester_credit_hours <= 0:
        return "Error: credit hours must be positive"
    total_ch = completed_credit_hours + semester_credit_hours
    total_points = (current_cgpa * completed_credit_hours) + (semester_gpa * semester_credit_hours)
    return round(total_points / total_ch, 4)


def required_gpa_for_target(target_cgpa: float, current_cgpa: float,
                             completed_credit_hours: float, remaining_credit_hours: float) -> float | str:
    """
    Calculate the GPA a student needs across their remaining credit hours to
    reach a target CGPA. Use this for 'what do I need to graduate with X'
    style questions. The result can exceed 4.0 - that just means the target
    is not reachable in that many remaining hours; do not treat it as valid
    advice, widen the horizon instead.
    """
    if remaining_credit_hours <= 0:
        return "Error: remaining credit hours must be positive"
    total_ch = completed_credit_hours + remaining_credit_hours
    needed = (target_cgpa * total_ch) - (current_cgpa * completed_credit_hours)
    return round(needed / remaining_credit_hours, 4)


def get_semester_courses(semester: int) -> str:
    """
    Return the list of courses and credit hours for a given semester (1-8).
    Use this when you need to know what courses a student is taking, or
    their credit hours, for a specific semester.
    """
    if semester not in courses:
        return "Error: semester must be between 1 and 8"
    lines = [f"{code}: {name} ({ch} ch)" for code, name, ch in courses[semester]]
    return "\n".join(lines)


def get_remaining_credit_hours(current_semester: int) -> float | str:
    """
    Total the graded credit hours already completed through the end of the
    given semester (inclusive). Use this to find 'completed_credit_hours'
    when a student tells you what semester they just finished, instead of
    asking them to add it up themselves.
    """
    if current_semester not in courses:
        return "Error: semester must be between 1 and 8"
    total = 0.0
    for sem in range(1, current_semester + 1):
        total += sum(ch for _, _, ch in courses[sem])
    return total


def save_report(filename: str, content: str) -> str:
    """
    Save a summary of a GPA/CGPA calculation to a text file. Only call this
    after the student explicitly asks to save something, and only once a
    real result exists to save.
    """
    if not filename.strip():
        return "Error: filename cannot be empty"
    try:
        with open(filename, "w") as f:
            f.write(content)
        return f"Report saved to {filename}"
    except Exception as e:
        return f"Error: could not save file ({e})"
