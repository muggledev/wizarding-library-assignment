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

def __init__(self, school_id, wizard_name, house, year_enrolled, magical_power_level, active, specializtions):
    self.school_id = school_id
    self.wizard_name = wizard_name
    self.house = house
    self.year_enrolled = year_enrolled
    self.magical_power_level = magical_power_level
    self.active = active
    self.specialization = specializtions