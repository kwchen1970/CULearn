from flask_sqlalchemy import SQLAlchemy

import json
import time

from db import db, Tutor, Student, Rating
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
def base():
    return "hello world"

@app.route("/api/tutors/")
def get_all_tutors():
    """
    Endpoint for getting all tutors
    """
    tutors = []
    return success_response({"tutors": [t.serialize() for t in Tutor.query.all()]})
    # return success_response([t.serialize() for t in Tutor.query.all()])

@app.route("/api/tutors/", methods=["POST"])
def create_tutor():
    """
    Endpoint for creatinf a new course
    """
    body = json.loads(request.data)
    username = body.get("username")
    password = body.get("password")
    name = body.get("name")
    img = body.get("img")
    bio = body.get("bio")
    price = body.get("price")
    availability = body.get("availability")
    subjects = body.get("subjects")
    if username is None or password is None or img is None or bio is None or price is None or availability is None or subjects is None or name is None:
        return failure_response("Invalid input", 400)
    new_tutor = Tutor(
        username = username, 
        password = password, 
        name = name,
        img = img,
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

@app.route("/api/tutors/students/<int:tutor_id>/")
def get_students_of_tutor(tutor_id):
    """
    Endpoint for getting all the students of the tutor
    """
    tutor = Tutor.query.filter_by(id=tutor_id).first()
    if tutor is None:
        return failure_response("Tutor not found")
    return success_response({"students": [s.simple_serialize() for s in tutor.students]})
    # return success_response([s.simple_serialize() for s in tutor.students])

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
    return success_response({"students": [t.serialize() for t in Student.query.all()]})
    # return success_response([t.serialize() for t in Student.query.all()])

@app.route("/api/students/", methods=["POST"])
def create_student():
    """
    create a student
    """
    body = json.loads(request.data)
    name = body.get("name")
    username = body.get("username")
    password = body.get("password")
    img = body.get("img")
    bio = body.get("bio","")
    budget = body.get("budget")
    subjects = body.get("subjects")
    if username is None or password is None or img is None or bio is None or budget is None or subjects is None or name is None:
        return failure_response("Invalid input", 400)
    new_student = Student(
        name = name,
        username = username,
        password = password,
        img = img,
        bio = bio,
        budget = budget,
        subjects = subjects
    )
    db.session.add(new_student)
    db.session.commit()
    return success_response(new_student.serialize(),201)

@app.route("/api/students/<int:student_id>/")
def get_student_by_id(student_id):
    """
    get specific students
    """
    student = Student.query.filter_by(id = student_id).first()
    if student is None:
        return failure_response("student not found")
    return success_response(student.serialize())

@app.route("/api/students/tutors/<int:student_id>/")
def get_tutors_of_student(student_id):
    """
    Endpoint for getting all the tutors of the student
    """
    student = Student.query.filter_by(id=student_id).first()
    if student is None:
        return failure_response("Tutor not found")
    return success_response({"tutors": [t.simple_serialize() for t in student.tutors]})
    # return success_response([t.simple_serialize() for t in student.tutors])

@app.route("/api/students/<int:student_id>/", methods = ["DELETE"])
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

@app.route("/api/students/to/tutor/<int:tutor_id>/", methods = ["POST"])
def add_student_to_tutor(tutor_id):
    """
    Adds a student to a tutor
    """
    tutor = Tutor.query.filter_by(id = tutor_id).first()
    if tutor is None:
        return failure_response("Tutor not found")
    body = json.loads(request.data)
    student_id = body.get("student_id")
    student = Student.query.filter_by(id = student_id).first()
    if student is None:
        return failure_response("student not found")
    else:
        tutor.students.append(student)
    db.session.commit()
    return success_response(student.serialize())

@app.route("/api/tutor/authentication/", methods=["POST"])
def get_tutor_password():
    username = json.loads(request.data).get("username")
    tutor = Tutor.query.filter_by(username = username).first()
    if tutor == None:
        return failure_response("User not found", 404)
    return success_response(tutor.fetch_tutor_pw())

@app.route("/api/student/authentication/", methods=["POST"])
def get_student_password():
    username = json.loads(request.data).get("username")
    student = Student.query.filter_by(username = username).first()
    if student == None:
        return failure_response("User not found", 404)
    return success_response(student.fetch_student_pw())

@app.route("/api/tutors/ratings/<int:student_id>/", methods=["POST"])
def add_rating(student_id):
    student = Student.query.filter_by(id = student_id).first()
    if student is None:
        return failure_response("student not found")
    body = json.loads(request.data)
    comment = body.get("comment")
    rating = body.get("rating")
    tutor_id = body.get("tutor_id")
    tutor = Tutor.query.filter_by(id = tutor_id).first()
    if tutor is None:
        return failure_response("tutor not found")
    new_rating = Rating(
        comment = comment,
        rating = rating,
         tutor_id = tutor_id,
        student_id = student_id
    )
    db.session.add(new_rating)
    db.session.commit()
    return success_response(new_rating.serialize(), 201)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
