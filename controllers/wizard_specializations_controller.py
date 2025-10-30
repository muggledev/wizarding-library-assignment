from flask import Blueprint, request, jsonify
from db import db
from models.wizard_specializations import WizardSpecializations
from datetime import datetime
import uuid

wizard_specs_bp = Blueprint("wizard_specializations", __name__)

#CREATE Wizard Specialization
@wizard_specs_bp.route("/wizard/specialize", methods=["POST"])
def add_wizard_specialization():
    data = request.get_json() or request.form

    required_fields = ["wizard_id", "spell_id", "proficiency_level", "date_learned"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"message": f"{field} is required"}), 400

    try:
        date_learned = datetime.strptime(data.get("date_learned"), "%Y-%m-%d")
    except ValueError:
        return jsonify({"message": "date_learned must be in YYYY-MM-DD format"}), 400

    new_spec = WizardSpecializations(
        wizard_id=data.get("wizard_id"),
        spell_id=data.get("spell_id"),
        proficiency_level=data.get("proficiency_level"),
        date_learned=date_learned
    )

    db.session.add(new_spec)
    db.session.commit()

    result = {
        "wizard_id": new_spec.wizard_id,
        "spell_id": new_spec.spell_id,
        "proficiency_level": new_spec.proficiency_level,
        "date_learned": new_spec.date_learned.strftime("%Y-%m-%d")
    }

    return jsonify({"message": "Specialization added successfully", "results": result}), 201


#READ All Wizard Specializations
@wizard_specs_bp.route("/wizard/specializations", methods=["GET"])
def get_all_wizard_specializations():
    specs = WizardSpecializations.query.all()
    if not specs:
        return jsonify({"message": "No specializations found"}), 404

    result = []
    for s in specs:
        result.append({
            "wizard_id": s.wizard_id,
            "spell_id": s.spell_id,
            "proficiency_level": s.proficiency_level,
            "date_learned": s.date_learned.strftime("%Y-%m-%d")
        })

    return jsonify({"results": result}), 200


#READ Specializations by Wizard ID
@wizard_specs_bp.route("/wizard/specialization/<wizard_id>", methods=["GET"])
def get_wizard_specialization_by_id(wizard_id):
    specs = WizardSpecializations.query.filter_by(wizard_id=wizard_id).all()
    if not specs:
        return jsonify({"message": f"No specializations found for wizard {wizard_id}"}), 404

    result = []
    for s in specs:
        result.append({
            "wizard_id": s.wizard_id,
            "spell_id": s.spell_id,
            "proficiency_level": s.proficiency_level,
            "date_learned": s.date_learned.strftime("%Y-%m-%d")
        })

    return jsonify({"results": result}), 200


#UPDATE Wizard Specialization
@wizard_specs_bp.route("/wizard/specialization/<wizard_id>", methods=["PUT"])
def update_wizard_specialization_by_id(wizard_id):
    data = request.get_json() or request.form

    if not data.get("spell_id"):
        return jsonify({"message": "spell_id is required to update specialization"}), 400

    spec = WizardSpecializations.query.filter_by(
        wizard_id=wizard_id, spell_id=data.get("spell_id")
    ).first()

    if not spec:
        return jsonify({"message": "Specialization not found"}), 404

    if "proficiency_level" in data:
        spec.proficiency_level = data["proficiency_level"]

    if "date_learned" in data:
        try:
            spec.date_learned = datetime.strptime(data["date_learned"], "%Y-%m-%d")
        except ValueError:
            return jsonify({"message": "date_learned must be in YYYY-MM-DD format"}), 400

    db.session.commit()

    updated_spec = {
        "wizard_id": spec.wizard_id,
        "spell_id": spec.spell_id,
        "proficiency_level": spec.proficiency_level,
        "date_learned": spec.date_learned.strftime("%Y-%m-%d")
    }

    return jsonify({"message": "Specialization updated successfully", "results": updated_spec}), 200


#DELETE Wizard Specializations by Wizard ID
@wizard_specs_bp.route("/wizard/specialization/<wizard_id>", methods=["DELETE"])
def delete_wizard_specialization_by_id(wizard_id):
    specs = WizardSpecializations.query.filter_by(wizard_id=wizard_id).all()

    if not specs:
        return jsonify({"message": f"No specializations found for wizard {wizard_id}"}), 404

    for spec in specs:
        db.session.delete(spec)

    db.session.commit()

    return jsonify({"message": f"All specializations for wizard {wizard_id} deleted successfully"}), 200
