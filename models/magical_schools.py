from db import db
import uuid

class MagicalSchools(db.Model):
    __tablename__ = "magical_schools"

    school_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    school_name = db.Column(db.String(100), nullable=False, unique=True)
    location = db.Column(db.String(100))
    founded_year = db.Column(db.Integer)
    headmaster = db.Column(db.String(100))

    wizards = db.relationship("Wizards", backref="school", cascade="all, delete-orphan")
    books = db.relationship("Books", backref="school", cascade="all, delete-orphan")
