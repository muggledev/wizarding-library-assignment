from db import db
from datetime import datetime

class WizardSpecializations(db.Model):
    __tablename__ = "wizard_specializations"

    wizard_id = db.Column(db.String(36), db.ForeignKey("wizards.wizard_id"), primary_key=True)
    spell_id = db.Column(db.String(36), db.ForeignKey("spells.spell_id"), primary_key=True)
    proficiency_level = db.Column(db.Float)
    date_learned = db.Column(db.DateTime, default=datetime.utcnow)