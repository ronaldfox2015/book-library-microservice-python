from flask import Blueprint, url_for, redirect, request, jsonify

from project.server import db
from project.server.models import Students, Parrent

students_blueprint = Blueprint("students", __name__)


def get_students():
    students = Students.query.all()  # -> select * from Students
    return jsonify(students=[student.serializer for student in students])


def create_student(request=None):

    parrent = Parrent(name='PEPE')

    student = Students(None, name=request.args.get('name'),
                       last_name=request.args.get('last_name'),
                       age=request.args.get('age'),
                       email=request.args.get('email'),
                       fk=parrent)
    db.session.add(student)
    db.session.commit()

    return get_students()


def delete_student(request=None):
    students = Students.query.filter_by(
        name=request.args.get('name')).all()  # -> select * from Student where name=request...
    # .one()
    for student in students:
        db.session.delete(student)
        db.session.commit()

    return get_students()


def update_student(request=None):
    students = Students.query.filter_by(
        name=request.args.get('name')).all()  # -> select * from Student where name=request...
    for student in students:
        student.name = 'Jose'
        db.session.commit()

    return get_students()


# por pruebas esta post
@students_blueprint.route("/estudiantes/", methods=["GET", "POST", "DELETE", "PUT"])
def list_students_view():
    if request.method == 'GET':
        return get_students()
    elif request.method == 'POST':
        return create_student(request)
    elif request.method == 'DELETE':
        return delete_student(request)
    else:
        return update_student(request)
