from db import db
import uuid

class Spells(db.Model):
    __tablename__ = "spells"

    spell_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    spell_name = db.Column(db.String(100), nullable=False, unique=True)
    incantation = db.Column(db.String(100))
    difficulty_level = db.Column(db.Float)
    spell_type = db.Column(db.String(50))
    description = db.Column(db.String(255))

    wizard_specializations = db.relationship("WizardSpecializations", backref="spell", cascade="all, delete-orphan")

def __init__(self, spell_name, incantation, difficulty_level, spell_type, description):
    self.spell_name = spell_name
    self.incantation = incantation
    self.difficulty_level = difficulty_level
    self.spell_type = spell_type
    self.description = description