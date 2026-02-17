"""Simple class."""


class Student:
    """Represents a student with a name and finished status."""

    def __init__(self, name):
        """Initialize a new Student instance."""
        self.name = name
        self.finished = False