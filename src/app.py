from flask_sqlalchemy import SQLAlchemy

import json
import time

from db import db, Tutor, Student
from flask import Flask, request

app = Flask(__name__)
db_filename = "tutoring.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

# generalized response formats
def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(message, code=404):
    return json.dumps({"error": message}), code

@app.route("/")
@app.route("/api/tutors/")
def get_all_tutors():
    """
    Endpoint for getting all tutors
    """
    tutors = []
    return success_response({"tutors": [t.serialize() for t in Tutor.query.all()]})

@app.route("/api/tutors/", methods=["POST"])
def create_tutor():
    """
    Endpoint for creatinf a new course
    """
    body = json.loads(request.data)
    username = body.get("username")
    password = body.get("password")
    name = body.get("name")
    profile_img = body.get("profile_img")
    bio = body.get("bio")
    price = body.get("price")
    availability = body.get("availability")
    subjects = body.get("subjects")
    if username is None or password is None or profile_img is None or bio is None or price is None or availability is None or subjects is None or name is None:
        return failure_response("Invalid input", 400)
    new_tutor = Tutor(
        username = username, 
        password = password, 
        name = name,
        profile_img = profile_img,
        bio = bio,
        price = price, 
        availability = availability,
        subjects = subjects
    )
    db.session.add(new_tutor)
    db.session.commit()
    
    return success_response(new_tutor.serialize(), 201)

@app.route("/api/tutors/<int:tutor_id>/")
def get_tutor_by_id(tutor_id):
    """
    Endpoint for getting a tutor by id
    """
    tutor = Tutor.query.filter_by(id=tutor_id).first()
    if tutor is None:
        return failure_response("Tutor not found")
    return success_response(tutor.serialize())

@app.route("/api/tutors/<int:tutor_id>/", methods=["DELETE"])
def delete_tutor(tutor_id):
    """
    Endpoint for deleting a tutor by id
    """
    tutor = Tutor.query.filter_by(id=tutor_id).first()
    if tutor is None:
        return failure_response("Tutor not found")
    db.session.delete(tutor)
    db.session.commit()
    return success_response(tutor.serialize())

@app.route("/api/students/")
def get_all_students():
    """
    get all students
    """
    return success_response({"courses": [t.serialize() for t in Student.query.all()]})

app.route("/api/students/<int:student_id>/")
def get_student_by_id(student_id):
    """
    get specific students
    """
    student = Student.query.filter_by(id = student_id).first()
    if student is None:
        return failure_response("student not found")
    return success_response(student.serialize())

app.route("/api/students/<int:student_id>/", methods = ["DELETE"])
def delete_student(student_id):
    """
    delete a student
    """
    student = Student.query.filter_by(id = student_id).first()
    if student is None:
        return failure_response("student not found")
    db.session.delete(student)
    db.session.commit()
    return success_response(student.serialize())

app.route("/api/students/", methods = ["POST"])
def create_student():
    """
    create a student
    """
    body = json.loads(request.data)
    new_student = Student(
        name = body.get("name"),
        username = body.get("username"),
        password = body.get("password"),
        profile_img = body.get("profile_img"),
        bio = body.get("bio",""),
        budget = body.get("budget"),
        subjects = body.get("subjects")
    )
    db.session.add(new_student)
    db.session.commit()
    return success_response(new_student.serialize(),201)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
