from flask import Blueprint, request, jsonify
import uuid
from db import db
from models.books import Books

books = Blueprint("books", __name__)

#CREATE Book
@books.route("/book", methods=["POST"])
def add_book():
    data = request.get_json() or request.form

    if not data.get("title"):
        return jsonify({"message": "title is required"}), 400

    new_book = Books(
        book_id=str(uuid.uuid4()),
        school_id=data.get("school_id"),
        title=data.get("title"),
        author=data.get("author"),
        subject=data.get("subject"),
        rarity_level=data.get("rarity_level"),
        magical_properties=data.get("magical_properties", ""),
        available=data.get("available", True)
    )

    db.session.add(new_book)
    db.session.commit()

    result = {
        "book_id": new_book.book_id,
        "title": new_book.title,
        "author": new_book.author,
        "subject": new_book.subject,
        "rarity_level": new_book.rarity_level,
        "magical_properties": new_book.magical_properties,
        "available": new_book.available,
        "school_id": new_book.school_id
    }

    return jsonify({"message": "Book created successfully", "results": result}), 201


#READ All Books
@books.route("/books", methods=["GET"])
def get_all_books():
    books_list = Books.query.all()
    if not books_list:
        return jsonify({"message": "No books found"}), 404

    result = []
    for b in books_list:
        result.append({
            "book_id": b.book_id,
            "title": b.title,
            "author": b.author,
            "subject": b.subject,
            "rarity_level": b.rarity_level,
            "magical_properties": b.magical_properties,
            "available": b.available,
            "school_id": b.school_id
        })

    return jsonify({"results": result}), 200


#READ Available Books Only
@books.route("/books/available", methods=["GET"])
def get_available_books():
    available_books = Books.query.filter_by(available=True).all()
    if not available_books:
        return jsonify({"message": "No available books found"}), 404

    result = []
    for b in available_books:
        result.append({
            "book_id": b.book_id,
            "title": b.title,
            "author": b.author,
            "subject": b.subject,
            "rarity_level": b.rarity_level,
            "magical_properties": b.magical_properties,
            "school_id": b.school_id
        })

    return jsonify({"results": result}), 200


#UPDATE Book by ID
@books.route("/book/<book_id>", methods=["PUT"])
def update_book_by_id(book_id):
    book = Books.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    data = request.get_json() or request.form

    for field in ["title", "author", "subject", "rarity_level", "magical_properties", "available", "school_id"]:
        if field in data and data[field] is not None:
            setattr(book, field, data[field])

    db.session.commit()

    updated_book = {
        "book_id": book.book_id,
        "title": book.title,
        "author": book.author,
        "subject": book.subject,
        "rarity_level": book.rarity_level,
        "magical_properties": book.magical_properties,
        "available": book.available,
        "school_id": book.school_id
    }

    return jsonify({"message": "Book updated successfully", "results": updated_book}), 200


# DELETE Book
@books.route("/book/<book_id>", methods=["DELETE"])
def delete_book_by_id(book_id):
    book = Books.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    db.session.delete(book)
    db.session.commit()

    return jsonify({"message": "Book deleted successfully"}), 200
