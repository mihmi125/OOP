"""Students."""


class Student:
    """
    Class for students.

    Every student has:
    a name,
    list of courses by title and
    an average overall grade.
    """

    def __init__(self, name: str, courses: list, average_grade: float):
        """Student constructor."""
        self.name = name
        self.courses = courses
        self.average_grade = average_grade

    def __repr__(self):
        """Student representation."""
        return self.name


def filter_by_course(student_list: list, course: str) -> list:
    """
    Return a filtered list of students that are taking a certain course.

    The name of the course is in the list of courses for the student.

    :param student_list: a list of Students
    :param course: the title of the course
    :return: a filtered list of students taking the course
    """
    return [student for student in student_list if course in student.courses]


def is_failing(student: Student) -> bool:
    """
    Return true if the student is failing school.

    They are failing if their average grade is below 1.0.

    :param student: a Student object
    :return: if student is failing
    """
    return student.average_grade < 1.0


def succeeding_students(student_list: list) -> list:
    """
    Return a list of students that are not failing school.

    :param student_list: a list of students
    :return: filtered list of students that are not failing
    """
    return [student for student in student_list if not is_failing(student)]


def failing_students(student_list: list) -> list:
    """
    Return a list of students that are failing school.

    :param student_list: a list of students
    :return: filtered list of students that are failing
    """
    return [student for student in student_list if is_failing(student)]


def sort_by_best_grade(student_list: list) -> list:
    """
    Return a sorted list of students by their average grade in descending order.

    Highest average grade students first.
    If a student is failing school (average grade less than 1.0) then dont return them in the list.
    If students have the same grade, then sort them alphabetically.

    :param student_list: a list of students
    :return: sorted list of succeeding students by average grade in descending order
    """
    succeeding = succeeding_students(student_list)
    return sorted(succeeding, key=lambda student: (-student.average_grade, student.name))


def sort_by_worst_grade(student_list: list) -> list:
    """
    Return a sorted list of students by their average grade in ascending order.

    Lowest average grade students first.
    If a student is failing school (average grade less than 1.0) then dont return them in the list.
    If students have the same grade, then sort them alphabetically.

    :param student_list: a list of students
    :return: sorted list of succeeding students by average grade in ascending order
    """
    succeeding = succeeding_students(student_list)
    return sorted(succeeding, key=lambda student: (student.average_grade, student.name))


if __name__ == '__main__':
    student1 = Student("Ann", ["Programming", "Maths", "Lithology"], 3.2)
    student2 = Student("Josh", ["Maths", "English", "Politics"], 2.0)
    student3 = Student("Bush", ["Politics"], 0.5)
    student4 = Student("Marcus", ["Web application", "Computers", "Artificial Intelligence"], 4.2)
    students = [student1, student2, student3, student4]
    print(filter_by_course(students, "Maths"))  # -> [Ann, Josh]
    print(is_failing(student3))  # -> True
    print(is_failing(student1))  # -> False
    print(succeeding_students(students))  # -> [Ann, Josh, Marcus]
    print(failing_students(students))  # -> [Bush]
    print(sort_by_best_grade(students))  # -> [Marcus, Ann, Josh]
    print(sort_by_worst_grade(students))  # -> [Josh, Ann, Marcus]
