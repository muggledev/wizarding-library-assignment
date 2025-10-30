from flask import jsonify, request, Blueprint
import uuid
from db import db
from models.magical_schools import MagicalSchools

magical_schools = Blueprint('magical_schools', __name__)

#CREATE School
@magical_schools.route("/school", methods=["POST"])
def add_school():
    post_data = request.get_json() or request.form

    if not post_data.get("school_name"):
        return jsonify({"message": "school_name is required"}), 400

    new_school = MagicalSchools(
        school_id=str(uuid.uuid4()),
        school_name=post_data.get("school_name"),
        location=post_data.get("location"),
        founded_year=post_data.get("founded_year"),
        headmaster=post_data.get("headmaster")
    )

    db.session.add(new_school)
    db.session.commit()

    return jsonify({
        "message": "school created",
        "results": {
            "school_id": new_school.school_id,
            "school_name": new_school.school_name,
            "location": new_school.location,
            "founded_year": new_school.founded_year,
            "headmaster": new_school.headmaster
        }
    }), 201


# READ All Schools
@magical_schools.route("/schools", methods=["GET"])
def get_all_schools():
    schools = MagicalSchools.query.all()

    if not schools:
        return jsonify({"message": "No schools found"}), 404

    result = []
    for s in schools:
        result.append({
            "school_id": s.school_id,
            "school_name": s.school_name,
            "location": s.location,
            "founded_year": s.founded_year,
            "headmaster": s.headmaster
        })

    return jsonify({"results": result}), 200


# READ School by ID
@magical_schools.route("/school/<school_id>", methods=["GET"])
def get_school_by_id(school_id):
    school = MagicalSchools.query.get(school_id)
    if not school:
        return jsonify({"message": "School not found"}), 404

    result = {
        "school_id": school.school_id,
        "school_name": school.school_name,
        "location": school.location,
        "founded_year": school.founded_year,
        "headmaster": school.headmaster
    }
    return jsonify({"results": result}), 200


# UPDATE School
@magical_schools.route("/school/<school_id>", methods=["PUT"])
def update_school_by_id(school_id):
    school = MagicalSchools.query.get(school_id)
    if not school:
        return jsonify({"message": "School not found"}), 404

    data = request.get_json() or request.form

    for field in ["school_name", "location", "founded_year", "headmaster"]:
        if field in data and data[field] is not None:
            setattr(school, field, data[field])

    db.session.commit()

    return jsonify({
        "message": "School updated successfully",
        "results": {
            "school_id": school.school_id,
            "school_name": school.school_name,
            "location": school.location,
            "founded_year": school.founded_year,
            "headmaster": school.headmaster
        }
    }), 200


# DELETE School (cascade delete)
@magical_schools.route("/school/<school_id>", methods=["DELETE"])
def delete_school_by_id(school_id):
    school = MagicalSchools.query.get(school_id)
    if not school:
        return jsonify({"message": "School not found"}), 404

    db.session.delete(school)
    db.session.commit()

    return jsonify({"message": "School and related wizards/books deleted"}), 200
