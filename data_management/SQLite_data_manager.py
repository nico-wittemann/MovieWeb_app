from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from data_management.data_manager_interface import DataManagerInterface
from data_management.data_models import User, Movie, db


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db):
        self.db = db


    def get_all_users(self):
        try:
            list_of_all_users = self.db.session.query(User.name).all()
            return list_of_all_users

        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"A database error occurred at getting all users: {e}")


    def get_all_movies(self):
        try:
            list_of_all_movies = self.db.session.query(Movie.title).all()
            return list_of_all_movies

        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"A database error occurred at getting all movies: {e}")


    def get_user_movies(self, user_id):
        try:
            user = self.db.session.query(User).get(user_id)
            if not user:
                raise ValueError(f"User with ID {user_id} not found.")
            movies = user.movies
            return movies # Careful it returns the object now (for loop and movie.title or .director) to get specificts

        except ValueError as e:
            self.db.session.rollback()
            print(e)
        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"A database error occurred getting the assigned movies from a user: {e}")


    def add_user(self, input_username):
        if self.input_not_string(input_username):
            raise TypeError("Username must be a string.")
        if self.username_already_used(input_username):
            raise ValueError("Username is already used.")

        try:
            user = User(
                name = input_username,
            )
            self.db.session.add(user)
            self.db.session.commit()

        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"A database error occurred while adding the user: {e}")


    def add_movie(self,input_title, input_director, input_publication_year, input_rating):
        if self.input_not_string(input_title):
            raise TypeError("Title must be a string.")
        if self.input_not_string(input_director):
            raise TypeError("Director must be a string.")
        if self.input_not_int(input_publication_year):
            raise TypeError("Publication year must be an integer.")
        if self.input_not_float(input_rating):
            raise TypeError("Rating must be a float.")

        try:
            movie = Movie(
                title = input_title,
                director = input_director,
                publication_year = input_publication_year,
                rating = input_rating
            )
            self.db.session.add(movie)
            self.db.session.commit()

        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"A database error occurred while adding the movie: {e}")


    def add_movie_to_user(self, user_id, movie_id): # Change later to title maybe, or make sure to display id in flask!
        try:
            user = self.db.session.query(User).get(user_id)
            if not user:
                raise ValueError(f"User with ID {user_id} not found.")
            movie = self.db.session.query(Movie).get(movie_id)
            if not movie:
                raise ValueError(f"Movie with ID {movie_id} not found.")
            if movie in user.movies:
                print(f"Movie with ID {movie_id} is already assigned to User with ID {user_id}.")
                return None
            user.movies.append(movie)
            self.db.session.commit()
            print(f"Movie {movie.title} successfully assigned to User {user.name}.")

        except ValueError as e:
            self.db.session.rollback()
            print(e)
        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"A database error occurred while assigning movie to user: {e}")

    def update_user(self, user_id, new_username):
        if self.input_not_string(new_username):
            raise TypeError("Username must be a string.")
        if self.username_already_used(new_username):
            raise ValueError("Username is already used.")

        try:
            user_to_update = self.db.session.query(User) \
                .filter(User.id == user_id) \
                .one()
            user_to_update.name = new_username
            self.db.session.commit()

        except NoResultFound:
            self.db.session.rollback()
            print(f"Movie with ID {user_id} not found.")
        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"A database error occurred while updating the user: {e}")


    def update_movie(self, movie_id, new_title, new_director, new_publication_year, new_rating):
        if self.input_not_string(new_title):
            raise TypeError("Title must be a string.")
        if self.input_not_string(new_director):
            raise TypeError("Director must be a string.")
        if self.input_not_int(new_publication_year):
            raise TypeError("Publication year must be an integer.")
        if self.input_not_float(new_rating):
            raise TypeError("Rating must be a float.")

        try:
            movie_to_update = self.db.session.query(Movie) \
                .filter(Movie.id == movie_id) \
                .one()
            if new_title:
                movie_to_update.title = new_title
            if new_director:
                movie_to_update.director = new_director
            if new_publication_year:
                movie_to_update.publication_year = new_publication_year
            if new_rating:
                movie_to_update.rating = new_rating
            self.db.session.commit()

        except NoResultFound:
            self.db.session.rollback()
            print(f"Movie with ID {movie_id} not found.")
        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"A database error occurred while updating the movie: {e}")


    def delete_user(self, user_id):
        try:
            self.db.session.query(User) \
                .filter(User.id == user_id) \
                .delete()
            self.db.session.commit()

        except NoResultFound:
            self.db.session.rollback()
            print(f"User with ID {user_id} not found.")
        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"A database error occurred while updating the movie: {e}")


    def delete_movie(self, movie_id):
        try:
            self.db.session.query(Movie) \
                .filter(Movie.id == movie_id) \
                .delete()
            self.db.session.commit()

        except NoResultFound:
            self.db.session.rollback()
            print(f"Movie with ID {movie_id} not found.")
        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"A database error occurred while updating the movie: {e}")



#Functions for input validation:
    def username_already_used(self, new_username):
        existing_user = self.db.session.query(User).filter(User.name == new_username).first()
        if existing_user:
            return True
        else:
            return False

    def input_not_string(self, new_input):
        if isinstance(new_input, str):
            return False
        else:
            return True

    def input_not_int(self, new_input):
        if isinstance(new_input, int):
            return False
        else:
            return True

    def input_not_float(self, new_input):
        if isinstance(new_input, float):
            return False
        else:
            return True







