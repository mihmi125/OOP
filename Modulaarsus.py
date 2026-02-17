"""School class which stores information about courses and students."""
from student import Student
from course import Course


class School:
    """A class representing a school system."""

    def __init__(self, name: str):
        """Initialize the school with a name."""
        self.name = name
        self.students = []
        self.courses = []
        self._next_id = 1

    def add_course(self, course: Course):
        """Add a course to the school's list of courses."""
        if course not in self.courses:
            self.courses.append(course)

    def add_student(self, student: Student):
        """Assign an ID and add a student to the school."""
        if student not in self.students:
            student.set_id(self._next_id)
            self._next_id += 1
            self.students.append(student)

    def add_student_grade(self, student: Student, course: Course, grade: int):
        """Record a grade for a student in a specific course."""
        if student in self.students and course in self.courses:
            student.add_grade(course, grade)
            course.add_grade(student, grade)

    def get_students(self):
        """Return the list of students."""
        return self.students

    def get_courses(self):
        """Return the list of courses."""
        return self.courses

    def get_students_ordered_by_average_grade(self):
        """Return students sorted by their average grade in descending order."""
        return sorted(self.students, key=lambda s: s.get_average_grade(), reverse=True)