from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False)
    username = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    profile_img = db.Column(db.String, nullable = False)
    bio = db.Column(db.String, nullable = False)
    budget = db.Column(db.Integer, nullable = False)
    subjects = db.Column(db.String, nullable = False) #make this a string list

    def __init__(self,**kwargs):
        """
        Initialize a Student object
        """
        self.name = kwargs.get("name","")
        self.username = kwargs.get("username","")
        self.password = kwargs.get("password","")
        self.profile_img = kwargs.get("profile_img","")
        self.bio = kwargs.get("bio","")
        self.budget = kwargs.get("budget","")
        self.subjects = kwargs.get("subjects","")
    
    def serialize(self):
        return{
            "id":self.id,
            "name": self.name,
            "username":self.username,
            "profile_img":self.profile_img,
            "bio":self.bio,
            "budget":self.budget,
            "subjects":self.subjects
        }
    def simple_serialize(self):
        """
        Serialize a student object.
        """
        return{
            "id":self.id,
            "name": self.name,
            "username":self.username,
            "profile_img":self.profile_img,
            "bio":self.bio,
            "budget":self.budget,
            "subjects":self.subjects
        }
