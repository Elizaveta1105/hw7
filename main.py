from sqlalchemy import func

from conf.db import session
from conf.models import Teacher, Student, Group, Subject, Note


def select_01():
    """
    select s.id, s.fullname, ROUND(AVG(n.note), 2) as average_note
    from students s
    join notes n on s.id = n.student_id
    group by s.id
    order by average_note DESC
    limit 5
    """

    result = session.query(
        Student.id,
        Student.fullname,
        func.round(func.avg(Note.note), 2).label('average_note')
    ).join(Note, Student.id == Note.student_id) \
        .group_by(Student.id) \
        .order_by(func.round(func.avg(Note.note), 2).desc()) \
        .limit(5).all()

    return result


def select_02():
    """
    select s.group_id, ROUND(AVG(n.note), 2) as average_note, s2."name", g."name"
    from students s
    join notes n on s.id = n.student_id
    join subjects s2 on n.subject_id = s2.id
    join "groups" g on s.group_id = g.id
    group by s.group_id , s2."name", g."name"
    order by average_note DESC
    """
    result = (
        session.query(
            Student.group_id,
            func.round(func.avg(Note.note), 2).label('average_note'),
            Subject.name.label('subject_name'),
            Group.name.label('group_name')
        )
        .join(Note, Student.id == Note.student_id)
        .join(Subject, Note.subjects_id == Subject.id)
        .join(Group, Student.group_id == Group.id)
        .group_by(Student.group_id, Subject.name, Group.name)
        .order_by(func.round(func.avg(Note.note), 2).desc())
    ).all()

    return result


def select_03():
    """
    SELECT g."name" AS group_name, ROUND(AVG(n.note), 2) AS average_note
    FROM notes n
    JOIN students s ON n.student_id = s.id
    JOIN "groups" g ON s.group_id = g.id
    GROUP BY g."name"
    ORDER BY average_note DESC
    """

    result = (
        session.query(
            Group.name.label('group_name'),
            func.round(func.avg(Note.note), 2).label('average_note')
        )
        .join(Student, Group.id == Student.group_id)
        .join(Note, Student.id == Note.student_id)
        .group_by(Group.name)
        .order_by(func.round(func.avg(Note.note), 2).desc())
    ).all()

    return result


def select_04():
    """
    SELECT ROUND(AVG(n.note), 2) AS average_note
    FROM notes n
    """

    result = (
        session.query(
            func.round(func.avg(Note.note), 2).label('average_note')
        )
    ).scalar()

    return result


def select_05():
    """
    SELECT t.fullname, MIN(s."name") AS subject_name
    FROM teachers t
    join subjects s on s.teacher_id = t.id
    group by t.fullname
    """

    result = (
        session.query(
            Teacher.fullname,
            func.min(Subject.name).label('subject_name')
        )
        .join(Subject, Teacher.id == Subject.teacher_id)
        .group_by(Teacher.fullname)
    ).all()

    return result


def select_07():
    """
    SELECT s.fullname, AVG(n.note) as average_grade, g."name" as group_name
    from notes n
    join students s on n.student_id = s.id
    join subjects s2 on n.subject_id = s2.id
    join "groups" g on s.group_id = g.id
    where g.id = 1 and s2.name = 'harness integrated deliverables'
    group by s.fullname , g."name"
    """

    result = (
        session.query(
            Student.fullname,
            func.avg(Note.note).label('average_grade'),
            Group.name.label('group_name')
        )
        .join(Student, Note.student_id == Student.id)
        .join(Subject, Note.subjects_id == Subject.id)
        .join(Group, Student.group_id == Group.id)
        .filter(Group.id == 1)
        .filter(Subject.name == 'harness integrated deliverables')
        .group_by(Student.fullname, Group.name)
    ).all()

    return result


def select_08():
    """
    SELECT t.fullname as teacher_name, s."name" as subject_name, AVG(n.note) as average_grade
    FROM teachers t
    LEFT JOIN subjects s ON t.id = s.teacher_id
    LEFT JOIN notes n ON s.id = n.subject_id
    GROUP BY s."name", t.fullname
    """
    result = (
        session.query(
            Teacher.fullname.label('teacher_name'),
            Subject.name.label('subject_name'),
            func.avg(Note.note).label('average_grade')
        )
        .outerjoin(Subject, Teacher.id == Subject.teacher_id)
        .outerjoin(Note, Subject.id == Note.subjects_id)
        .group_by(Subject.name, Teacher.fullname)
    ).all()

    return result


def select_09():
    """
    SELECT s.fullname as student_name, s2.name as subject_name
    FROM subjects s2
    LEFT JOIN notes n ON s2.id = n.subject_id
    LEFT JOIN students s ON n.student_id = s.id
    GROUP BY s.fullname, s2.name
    ORDER BY s.fullname ASC
    """
    result = (
        session.query(
            Student.fullname.label('student_name'),
            Subject.name.label('subject_name')
        )
        .outerjoin(Note, Subject.id == Note.subjects_id)
        .outerjoin(Student, Note.student_id == Student.id)
        .group_by(Student.fullname, Subject.name)
        .order_by(Student.fullname.asc())
    ).all()

    return result


def select_10():
    """
    SELECT t.fullname as teacher_name, s.fullname as student_name, s2.name as subject_name
    FROM subjects s2
    LEFT JOIN notes n ON s2.id = n.subject_id
    LEFT JOIN students s ON n.student_id = s.id
    LEFT JOIN teachers t ON s2.teacher_id = t.id
    where s.fullname = 'Adam Park'
    GROUP BY s.fullname, s2.name, t.fullname
    """

    result = (
        session.query(
            Teacher.fullname.label('teacher_name'),
            Student.fullname.label('student_name'),
            Subject.name.label('subject_name')
        )
        .outerjoin(Note, Subject.id == Note.subjects_id)
        .outerjoin(Student, Note.student_id == Student.id)
        .outerjoin(Teacher, Subject.teacher_id == Teacher.id)
        .filter(Student.fullname == 'Adam Park')
        .group_by(Student.fullname, Subject.name, Teacher.fullname)
    ).all()

    return result


if __name__ == '__main__':
    print(select_10())
