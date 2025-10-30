from flask import Blueprint, request, jsonify
from db import db
from models.wizards import Wizards
import uuid

wizards_bp = Blueprint("wizards", __name__)

#CREATE Wizard
@wizards_bp.route("/wizard", methods=["POST"])
def add_wizard():
    data = request.get_json() or request.form

    required_fields = ["wizard_name", "school_id"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"message": f"{field} is required"}), 400

    new_wizard = Wizards(
        wizard_id=str(uuid.uuid4()),
        school_id=data.get("school_id"),
        wizard_name=data.get("wizard_name"),
        house=data.get("house"),
        year_enrolled=data.get("year_enrolled"),
        magical_power_level=data.get("magical_power_level", 1),
        active=data.get("active", True)
    )

    db.session.add(new_wizard)
    db.session.commit()

    result = {
        "wizard_id": new_wizard.wizard_id,
        "wizard_name": new_wizard.wizard_name,
        "house": new_wizard.house,
        "year_enrolled": new_wizard.year_enrolled,
        "magical_power_level": new_wizard.magical_power_level,
        "active": new_wizard.active,
        "school_id": new_wizard.school_id
    }

    return jsonify({"message": "Wizard created successfully", "results": result}), 201


#READ All Wizards
@wizards_bp.route("/wizards", methods=["GET"])
def get_all_wizards():
    wizards = Wizards.query.all()
    if not wizards:
        return jsonify({"message": "No wizards found"}), 404

    result = [{
        "wizard_id": w.wizard_id,
        "wizard_name": w.wizard_name,
        "house": w.house,
        "year_enrolled": w.year_enrolled,
        "magical_power_level": w.magical_power_level,
        "active": w.active,
        "school_id": w.school_id
    } for w in wizards]

    return jsonify({"results": result}), 200


#READ Active Wizards
@wizards_bp.route("/wizards/active", methods=["GET"])
def get_active_wizards():
    wizards = Wizards.query.filter_by(active=True).all()
    if not wizards:
        return jsonify({"message": "No active wizards found"}), 404

    result = [{
        "wizard_id": w.wizard_id,
        "wizard_name": w.wizard_name,
        "house": w.house,
        "year_enrolled": w.year_enrolled,
        "magical_power_level": w.magical_power_level,
        "school_id": w.school_id
    } for w in wizards]

    return jsonify({"results": result}), 200


#READ Wizard by ID
@wizards_bp.route("/wizards/<wizard_id>", methods=["GET"])
def get_wizard_by_id(wizard_id):
    wizard = Wizards.query.get(wizard_id)
    if not wizard:
        return jsonify({"message": "Wizard not found"}), 404

    result = {
        "wizard_id": wizard.wizard_id,
        "wizard_name": wizard.wizard_name,
        "house": wizard.house,
        "year_enrolled": wizard.year_enrolled,
        "magical_power_level": wizard.magical_power_level,
        "active": wizard.active,
        "school_id": wizard.school_id
    }
    return jsonify({"results": result}), 200


#READ Wizards by House
@wizards_bp.route("/wizards/house/<house>", methods=["GET"])
def get_wizards_by_house(house):
    wizards = Wizards.query.filter_by(house=house).all()
    if not wizards:
        return jsonify({"message": f"No wizards found in house {house}"}), 404

    result = [{
        "wizard_id": w.wizard_id,
        "wizard_name": w.wizard_name,
        "year_enrolled": w.year_enrolled,
        "magical_power_level": w.magical_power_level,
        "active": w.active,
        "school_id": w.school_id
    } for w in wizards]

    return jsonify({"results": result}), 200


#READ Wizards by Magical Power Level
@wizards_bp.route("/wizards/magic/<int:magical_power_level>", methods=["GET"])
def get_wizards_by_power(magical_power_level):
    wizards = Wizards.query.filter_by(magical_power_level=magical_power_level).all()
    if not wizards:
        return jsonify({"message": f"No wizards found with power level {magical_power_level}"}), 404

    result = [{
        "wizard_id": w.wizard_id,
        "wizard_name": w.wizard_name,
        "house": w.house,
        "year_enrolled": w.year_enrolled,
        "active": w.active,
        "school_id": w.school_id
    } for w in wizards]

    return jsonify({"results": result}), 200


#UPDATE Wizard
@wizards_bp.route("/wizard/<wizard_id>", methods=["PUT"])
def update_wizard_by_id(wizard_id):
    wizard = Wizards.query.get(wizard_id)
    if not wizard:
        return jsonify({"message": "Wizard not found"}), 404

    data = request.get_json() or request.form
    for key in ["wizard_name", "house", "year_enrolled", "magical_power_level", "active", "school_id"]:
        if key in data:
            setattr(wizard, key, data[key])

    db.session.commit()

    result = {
        "wizard_id": wizard.wizard_id,
        "wizard_name": wizard.wizard_name,
        "house": wizard.house,
        "year_enrolled": wizard.year_enrolled,
        "magical_power_level": wizard.magical_power_level,
        "active": wizard.active,
        "school_id": wizard.school_id
    }

    return jsonify({"message": "Wizard updated successfully", "results": result}), 200


#DELETE Wizard
@wizards_bp.route("/wizard/<wizard_id>", methods=["DELETE"])
def delete_wizard_by_id(wizard_id):
    wizard = Wizards.query.get(wizard_id)
    if not wizard:
        return jsonify({"message": "Wizard not found"}), 404

    db.session.delete(wizard)
    db.session.commit()

    return jsonify({"message": "Wizard deleted successfully"}), 200
