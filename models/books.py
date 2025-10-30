from db import db
import uuid

class Books(db.Model):
    __tablename__ = "books"

    book_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    school_id = db.Column(db.String(36), db.ForeignKey("magical_schools.school_id"), nullable=False)
    title = db.Column(db.String(150), nullable=False, unique=True)
    author = db.Column(db.String(100))
    subject = db.Column(db.String(50))
    rarity_level = db.Column(db.Integer)
    magical_properties = db.Column(db.String(255))
    available = db.Column(db.Boolean, default=True)
