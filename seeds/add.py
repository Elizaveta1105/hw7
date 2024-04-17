import random

from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

from conf.db import session
from conf.models import Teacher, Student, TeacherStudent

fake = Faker('uk-UA')


def insert_students():
    for _ in range(45):
        student = Student(
            fullname=fake.name()
        )
        session.add(student)


def insert_teachers():
    for _ in range(4):
        teacher = Teacher(
            fullname=fake.name()
        )
        session.add(teacher)


def insert_rel():
    students = session.query(Student).all()
    teachers = session.query(Teacher).all()

    for student in students:
        rel = TeacherStudent(teacher_id=random.choice(teachers).id, student_id=student.id)
        session.add(rel)


if __name__ == '__main__':
    try:
        insert_students()
        insert_teachers()
        session.commit()
        insert_rel()
        session.commit()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        session.close()
