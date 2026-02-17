"""Constructor exercise."""


class Empty:
    """An empty class without constructor."""

    pass


class Person:
    """Represent person with firstname, lastname and age."""

    firstname = ""
    lastname = ""
    age = 0


class Student:
    """Represent student with firstname, lastname and age."""

    def __init__(self, firstname, lastname, age):
        """Student firstname, lastname and age."""
        self.firstname = firstname
        self.lastname = lastname
        self.age = age


if __name__ == '__main__':
    empty = Empty()

    person1 = Person()
    person1.firstname = "Mati"
    person1.lastname = "Kaal"
    person1.age = 30

    person2 = Person()
    person2.firstname = "Johannes"
    person2.lastname = "Kukk"
    person2.age = 30

    person3 = Person()
    person3.firstname = "Rasmus"
    person3.lastname = "Reinomägi"
    person3.age = 30

    student1 = Student("Kati", "Karu", 20)
    student2 = Student("Siim", "Heinsaar", 20)
    student3 = Student("Mikk", "Lember", 20)