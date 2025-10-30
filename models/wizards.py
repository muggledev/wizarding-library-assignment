from db import db
import uuid

class Wizards(db.Model):
    __tablename__ = "wizards"

    wizard_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    school_id = db.Column(db.String(36), db.ForeignKey("magical_schools.school_id"), nullable=False)
    wizard_name = db.Column(db.String(100), nullable=False, unique=True)
    house = db.Column(db.String(50))
    year_enrolled = db.Column(db.Integer)
    magical_power_level = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True)

    specializations = db.relationship("WizardSpecializations", backref="wizard", cascade="all, delete-orphan")
