from flask import Blueprint, request, jsonify
import uuid
from db import db
from models.spells import Spells

spells_bp = Blueprint("spells", __name__)

#CREATE Spell
@spells_bp.route("/spell", methods=["POST"])
def add_spell():
    data = request.get_json() or request.form

    if not data.get("spell_name"):
        return jsonify({"message": "spell_name is required"}), 400

    new_spell = Spells(
        spell_id=str(uuid.uuid4()),
        spell_name=data.get("spell_name"),
        incantation=data.get("incantation"),
        difficulty_level=data.get("difficulty_level"),
        spell_type=data.get("spell_type"),
        description=data.get("description")
    )

    db.session.add(new_spell)
    db.session.commit()

    result = {
        "spell_id": new_spell.spell_id,
        "spell_name": new_spell.spell_name,
        "incantation": new_spell.incantation,
        "difficulty_level": new_spell.difficulty_level,
        "spell_type": new_spell.spell_type,
        "description": new_spell.description
    }

    return jsonify({"message": "Spell created successfully", "results": result}), 201


#READ All Spells
@spells_bp.route("/spells", methods=["GET"])
def get_all_spells():
    spells = Spells.query.all()
    if not spells:
        return jsonify({"message": "No spells found"}), 404

    result = []
    for s in spells:
        result.append({
            "spell_id": s.spell_id,
            "spell_name": s.spell_name,
            "incantation": s.incantation,
            "difficulty_level": s.difficulty_level,
            "spell_type": s.spell_type,
            "description": s.description
        })

    return jsonify({"results": result}), 200


#READ Spells by Difficulty Level
@spells_bp.route("/spells/difficulty/<float:difficulty_level>", methods=["GET"])
def get_spells_by_difficulty(difficulty_level):
    spells = Spells.query.filter_by(difficulty_level=difficulty_level).all()
    if not spells:
        return jsonify({"message": f"No spells found with difficulty level {difficulty_level}"}), 404

    result = []
    for s in spells:
        result.append({
            "spell_id": s.spell_id,
            "spell_name": s.spell_name,
            "incantation": s.incantation,
            "difficulty_level": s.difficulty_level,
            "spell_type": s.spell_type,
            "description": s.description
        })

    return jsonify({"results": result}), 200


#UPDATE Spell by ID
@spells_bp.route("/spell/<spell_id>", methods=["PUT"])
def update_spell_by_id(spell_id):
    spell = Spells.query.get(spell_id)
    if not spell:
        return jsonify({"message": "Spell not found"}), 404

    data = request.get_json() or request.form

    for field in ["spell_name", "incantation", "difficulty_level", "spell_type", "description"]:
        if field in data and data[field] is not None:
            setattr(spell, field, data[field])

    db.session.commit()

    updated_spell = {
        "spell_id": spell.spell_id,
        "spell_name": spell.spell_name,
        "incantation": spell.incantation,
        "difficulty_level": spell.difficulty_level,
        "spell_type": spell.spell_type,
        "description": spell.description
    }

    return jsonify({"message": "Spell updated successfully", "results": updated_spell}), 200


# DELETE Spell
@spells_bp.route("/spell/<spell_id>", methods=["DELETE"])
def delete_spell_by_id(spell_id):
    spell = Spells.query.get(spell_id)
    if not spell:
        return jsonify({"message": "Spell not found"}), 404

    db.session.delete(spell)
    db.session.commit()

    return jsonify({"message": "Spell deleted successfully"}), 200
