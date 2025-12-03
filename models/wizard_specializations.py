from db import db
from datetime import datetime, timezone

class WizardSpecializations(db.Model):
    __tablename__ = "wizard_specializations"

    wizard_id = db.Column(db.String(36), db.ForeignKey("wizards.wizard_id"), primary_key=True)
    spell_id = db.Column(db.String(36), db.ForeignKey("spells.spell_id"), primary_key=True)
    proficiency_level = db.Column(db.Float)
    date_learned = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

def __init__(self, spell_id, proficiency_level, date_learned):
    self.spell_id = spell_id
    self.proficiency_level = proficiency_level
    self.date_learned = date_learned