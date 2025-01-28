import os
from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
from datamanager.data_models import db, User, Movie
from datamanager.SQLite_data_manager import SQLiteDataManager
from API_Movies import api_request_data

# Initialize Flask and CORS
app = Flask(__name__)
CORS(app)


# Configuration function
def configure_app(app):
    current_directory = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', f'sqlite:///{os.path.join(current_directory, "data", "library.sqlite")}')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database function
def initialize_database(app, db):
    db.init_app(app)
    with app.app_context():
        db.create_all()

# Set configuration and initialize database/
configure_app(app)
initialize_database(app, db)
data_manager = SQLiteDataManager(db)


# Flask Routes
@app.route('/')  # Navigation!
def home():
    return render_template('home.html'), 200


@app.route('/users') # get_all_users 2
def list_users():
    """"""
    users = data_manager.get_all_users()
    return render_template('users.html', users=users), 200


@app.route('/users/<int:user_id>') # get_user_movies 3 Bearbeiten das richtige werte ausgegeben werden
def list_user_movies(user_id):
    """"""
    action_result_add_movie = request.args.get('action_result_add_movie')
    user_movies = data_manager.get_user_movies(user_id)
    username = data_manager.get_username_by_id(user_id)
    return render_template('user_favourites.html', user_movies=user_movies, username=username, user_id=user_id, action_result_add_movie=action_result_add_movie), 200


@app.route('/add_user', methods=['GET', 'POST']) # add_user 4
def add_user():
    if request.method == 'GET':
        return render_template('add_user.html'), 200

    if request.method == 'POST':
        username = request.form['username']
        data_manager.add_user(username)
        success_message = f"User '{username}' has successfully been created."
        return render_template('home.html', success_message=success_message)



@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST']) # add_movie_to_user 5
def add_movie_to_user(user_id):
    """"""
    if request.method == 'GET':
        return render_template('add_movie.html', user_id=user_id), 200

    if request.method == 'POST':
        movie_name = request.form['movie_name']
        action_result_add_movie = data_manager.add_movie_to_user(user_id, movie_name)
        print(action_result_add_movie)
        return redirect(url_for('list_user_movies', action_result_add_movie=action_result_add_movie, user_id=user_id))




@app.route('/users/<int:user_id>/update_movie/<int:movie_id>') # update_movie 6
def update_movie():
    pass


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>') # delete_movie_from_favourites 7
def delete_movie():
    pass






if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)



#todo Implement OMDB API!
#todo Use OMDB API in user_favourites!


