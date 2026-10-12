import pytest

class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


@pytest.fixture
def default_student():
    return Student('John', 'Doe', 'Computer Science', 3)


def test_student_attributes(default_student):
    assert default_student.first_name == 'John', 'First name should be John'
    assert default_student.last_name == 'Doe', 'Last name should be Doe'
    assert default_student.major == 'Computer Science'
    assert default_student.years == 3

def test_student_full_name_method(default_student):
    assert default_student.full_name() == 'John Doe', 'Full name method failed'