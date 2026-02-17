"""Encapsulation exercise."""


class Student:
    """Student: represent a student with a name, identifier, and enrollment status."""

    def __init__(self, name, student_id):
        """Initialize a Student with a name and student_id and set the default status to "Active"."""
        self.__name = name
        self.__id = student_id
        self.__status = "Active"

    def get_id(self):
        """Return the student's unique identifier."""
        return self.__id

    def set_name(self, name):
        """Set the student's name to the provided value."""
        self.__name = name

    def get_name(self):
        """Return the student's name."""
        return self.__name

    def set_status(self, status):
        """Set the student's status to the provided value if it is either "Active", "Expelled", "Finished", or "Inactive", otherwise do nothing."""
        if status in ["Active", "Expelled", "Finished", "Inactive"]:
            self.__status = status

    def get_status(self):
        """Return the student's current enrollment status."""
        return self.__status