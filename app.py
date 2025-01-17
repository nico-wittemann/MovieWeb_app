import os
from flask import Flask
from flask_cors import CORS
from data_management.data_models import db, User, Movie
from data_management.SQLite_data_manager import SQLiteDataManager

# Initialize Flask and CORS
app = Flask(__name__)
CORS(app)

# Configuration function
def configure_app(app):
    current_directory = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(current_directory, "data", "library.sqlite")}'

# Initialize the database function
def initialize_database(app, db):
    db.init_app(app)
    with app.app_context():
        db.create_all()

# Set configuration and initialize database
configure_app(app)
initialize_database(app, db)


# Define routes
@app.route('/')
def home():
    pass #render_template('home.html', authors=authors), 200

def main():    # DELETE LATER
    print("main")
    data_manager = SQLiteDataManager("library.sqlite")
    data_manager.add_movie("Inception", "Christopher Nolan", 2010, 8.8)
    print("Filme hinzugefügt!")

if __name__ == '__main__':
    main()   # DELETE Later
    app.run(host="127.0.0.1", port=5000, debug=True)