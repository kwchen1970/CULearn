from db import db
import json
from flask import Flask,request
from db import Student

app = Flask(__name__)
db_filename = "tutor.db"

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
    return json.dumps(message), code

@app.route("/api/students/")
def get_allstudents():
    """
    get all students
    """
    return success_response({"courses": [t.serialize() for t in Student.query.all()]})

app.route("/api/students/<int:student_id>/")
def get_spec_student(student_id):
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
