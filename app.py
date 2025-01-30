import os
from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
from datamanager.data_models import db
from datamanager.SQLite_data_manager import SQLiteDataManager

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
@app.route('/')
def home():
    """Renders the home page of the application."""
    return render_template('home.html'), 200


@app.route('/users')
def list_users():
    """
    Renders a list of all users.

    This route fetches all users from the data manager and passes them to
    the 'users.html' template. The users are displayed in
    a list format.
    """
    users = data_manager.get_all_users()
    return render_template('users.html', users=users), 200


@app.route('/users/<int:user_id>')
def list_user_movies(user_id):
    """
    Renders a list of movies for a specific user.

    This route retrieves the movies associated with the user (identified by
    user_id) and displays them in the 'user_favourites.html' template. It shows
    the movie title, director, publication year, and rating (if available).
    Users can also delete or update movies with buttons.

    Args:
        user_id (int): The ID of the user.
    """
    action_result_add_movie = request.args.get('action_result_add_movie')
    user_movies = data_manager.get_user_movies(user_id)
    user = data_manager.get_user(user_id)
    return render_template('user_favourites.html', user_movies=user_movies, user=user, user_id=user_id, action_result_add_movie=action_result_add_movie), 200


@app.route('/add_user', methods=['GET', 'POST']) # add_user 4
def add_user():
    """
    Renders a form to add a new user.

    - GET request: Displays the user creation form ('add_user.html').
    - POST request: Retrieves the entered username, adds the user to the database,
      and shows a success message on the homepage.

    Args:
        username (str): The name of the user to be created (for POST).
    """
    if request.method == 'GET':
        return render_template('add_user.html'), 200

    if request.method == 'POST':
        username = request.form['username']
        data_manager.add_user(username)
        success_message = f"User '{username}' has successfully been created."
        return render_template('home.html', success_message=success_message)


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST']) # add_movie_to_user 5
def add_movie_to_user(user_id):
    """
    Renders a form to add a new movie to a user's movie list and handles the form.

    - GET request: Displays the movie addition form ('add_movie.html').
    - POST request: Retrieves the entered movie name, adds the movie to the user's list,
      and redirects to the user's movie list page with a success message.

    Args:
        user_id (int): The ID of the user to which the movie will be added.
    """
    if request.method == 'GET':
        return render_template('add_movie.html', user_id=user_id), 200

    if request.method == 'POST':
        movie_name = request.form['movie_name']
        action_result_add_movie = data_manager.add_movie_to_user(user_id, movie_name)
        return redirect(url_for('list_user_movies', action_result_add_movie=action_result_add_movie, user_id=user_id))


@app.route('/users/<int:user_id>/remove_movie/<int:movie_id>', methods=['POST'])
def remove_movie_from_user(movie_id, user_id):
    """
    Removes a movie from a user's favourites and redirects to the user's movie list.

    This route is triggered when the user submits the "Delete" button for a specific movie.
    The movie is removed from the user's list of favourites, and the page is redirected
    to the user's movie list with an updated action result message.

    Args:
        movie_id (int): The ID of the movie to be removed.
        user_id (int): The ID of the user whose movie list is being modified.
    """
    action_result_add_movie = data_manager.remove_movie_from_favourites(movie_id, user_id)
    return redirect(url_for('list_user_movies', action_result_add_movie=action_result_add_movie, user_id=user_id))


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST']) # update_movie 6
def update_movie(movie_id, user_id):
    """
    Updates the details of a specific movie for a user.

    - GET: Displays the current details of the movie in an editable form.
    - POST: Updates the movie's details based on the user's input and redirects
      to the user's movie list with a success message.

    Args:
        movie_id (int): The ID of the movie to be updated.
        user_id (int): The ID of the user whose movie list is being modified.
    """
    if request.method == 'GET':
        user = data_manager.get_user(user_id)
        movie = data_manager.get_movie(movie_id)
        return render_template('update.html', user=user, movie=movie)

    if request.method == 'POST':
        new_title = request.form['title']
        new_director = request.form['director']
        new_publication_year = request.form['publication_year']
        new_rating = request.form['rating']
        action_result_add_movie = data_manager.update_movie(user_id, movie_id, new_title, new_director, new_publication_year, new_rating)
        return redirect(url_for('list_user_movies', action_result_add_movie=action_result_add_movie, user_id=user_id))


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)











