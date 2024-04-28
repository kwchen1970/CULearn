from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Tutor(db.Model):
    """
    Tutor Model
    """
    __tablename__ = "tutors"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    profile_img = db.Column(db.String, nullable=False)
    bio = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    availability = db.Column(db.String, nullable=False)
    #Students = 
    subjects = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        """
        Initialize Tutor object/entry
        """
        self.username = kwargs.get("username", "")
        self.password = kwargs.get("password", "")
        self.name = kwargs.get("name", "")
        self.profile_img = kwargs.get("profile_img", "")
        self.bio = kwargs.get("bio", "")
        self.price = kwargs.get("price")
        self.availability = kwargs.get("availibility", "")
        self.subjects = kwargs.get("subjects", "")

    def serialize(self):
        """
        Serialize a tutor object
        """
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "bio": self.bio,
            "price": self.price,
            "availability": self.availability,
            "subjects": self.subjects
        }
