from flask import Flask, Blueprint
import os
from db import db, init_db

from controllers.magical_schools_controller import magical_schools
from controllers.wizards_controller import wizards_bp
from controllers.books_controller import books
from controllers.spells_controller import spells_bp
from controllers.wizard_specializations_controller import wizard_specs_bp



from models.wizards import Wizards
from models.magical_schools import MagicalSchools
from models.books import Books
from models.spells import Spells
from models.wizard_specializations import WizardSpecializations


app = Flask(__name__)


app.register_blueprint(magical_schools)
app.register_blueprint(wizards_bp)
app.register_blueprint(books)
app.register_blueprint(spells_bp)
app.register_blueprint(wizard_specs_bp)


database_scheme = os.environ.get("DATABASE_SCHEME", "sqlite:///")
database_user = os.environ.get("DATABASE_USER", "")
database_address = os.environ.get("DATABASE_ADDRESS", "")
database_port = os.environ.get("DATABASE_PORT", "")
database_name = os.environ.get("DATABASE_NAME", "hogwarts.db")

if "sqlite" in database_scheme:
    app.config["SQLALCHEMY_DATABASE_URI"] = f"{database_scheme}{database_name}"
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = f"{database_scheme}{database_user}@{database_address}:{database_port}/{database_name}"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
init_db(app, db)


def create_tables():
    with app.app_context():
        print("Creating Hogwarts tables...")
        db.create_all()
        print("Tables created successfully!")

if __name__ == "__main__":
    create_tables()
    flask_host = os.environ.get("FLASK_HOST", "127.0.0.1")
    flask_port = os.environ.get("FLASK_PORT", 8086)
    app.run(host=flask_host, port=flask_port, debug=True)
