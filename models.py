from pony.orm import *
from db import db

class Person(db.Entity):
    name = Required(str)
    email = Optional(str)
    assignments = Set("Assignment")

class Role(db.Entity):
    name = Required(str, unique=True)
    assignments = Set("Assignment")

class Assignment(db.Entity):
    person = Required(Person)
    role = Required(Role)
    year = Required(int)
    semester = Required(int)

    def semester_str(self):
        if self.semester == 1:
            return "V"
        else:
            return "H"

db.generate_mapping()

