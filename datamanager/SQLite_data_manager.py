from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from datamanager.data_manager_interface import DataManagerInterface
from datamanager.data_models import User, Movie, db, user_movie_association
from API_Movies import api_request_data


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db):
        self.db = db


    def get_all_users(self):
        """"""
        try:
            list_of_all_users = self.db.session.query(User).all()
            return list_of_all_users

        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"A database error occurred at getting all users: {e}")


    def get_all_movies(self):
        try:
            list_of_all_movies = self.db.session.query(Movie).all()
            return list_of_all_movies

        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"A database error occurred at getting all movies: {e}")


    def get_user_movies(self, user_id):
        """Returns the movie object."""
        try:
            user = self.db.session.query(User).get(user_id)
            if not user:
                raise ValueError(f"User with ID {user_id} not found.")
            movies = user.movies
            return movies

        except ValueError as e:
            self.db.session.rollback()
            print(e)
        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"A database error occurred getting the assigned movies from a user: {e}")


    def add_user(self, input_username):
        """"""
        if self._input_not_string(input_username):
            raise TypeError("Username must be a string.")
        if self._username_already_used(input_username):
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


    def add_movie_to_user(self, user_id, movie_name):
        """"""
        try:
            user = self.db.session.query(User).get(user_id)
            if not user:
                raise ValueError(f"User with ID {user_id} not found.")
            movie_name = movie_name.strip()
            api_data = api_request_data(movie_name)
            if api_data:
                title, publication_year, string_rating, poster_url, director = api_data
            else:
                return f"Title {(movie_name)} was not found in online database"

            existing_movie = self.db.session.query(Movie).filter(Movie.title == title).first()
            if existing_movie:
                if existing_movie not in user.movies:
                    user.movies.append(existing_movie)
                    self.db.session.commit()
                    return f"Movie {title} successfully assigned to your list."
                else:
                    return f"Movie {title} is already in your list."
            if string_rating is not None:
                rating = float(string_rating.split("/")[0])
            else:
                rating = None
            new_movie = Movie(
                title = title,
                director = director,
                publication_year = publication_year,
                rating = rating,
                poster_url = poster_url
            )
            user.movies.append(new_movie)
            self.db.session.commit()
            return f"Movie {title} successfully assigned to your list."

        except ValueError as e:
            self.db.session.rollback()
            print(e)
        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"A database error occurred while assigning movie to user: {e}")





    def update_movie(self, user_id, movie_id, new_title, new_director, new_publication_year, new_rating):
        """"""
        try:
            movie = self.get_movie(movie_id)
            user = self.db.session.query(User).get(user_id)
            poster_url = movie.poster_url
            new_rating = float(new_rating)
            new_publication_year = int(new_publication_year)
            if self._input_not_string(new_title):
                raise TypeError("Title must be a string.")
            if self._input_not_string(new_director):
                raise TypeError("Director must be a string.")
            if self._input_not_int(new_publication_year):
                raise TypeError("Publication year must be an integer.")
            if self._input_not_float_or_None(new_rating):
                raise TypeError("Rating must be a float.")

            self.remove_movie_from_favourites(movie_id, user_id)
            new_movie = Movie(
                title=new_title,
                director=new_director,
                publication_year=new_publication_year,
                rating=new_rating,
                poster_url=poster_url
            )
            user.movies.append(new_movie)
            self.db.session.commit()
            return f"Movie {movie.title} successfully updated in your list."

        except TypeError as e:
            print(f"Type error: {e}")
        except NoResultFound:
            self.db.session.rollback()
            print(f"Movie with ID {movie_id} not found.")
        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"A database error occurred while updating the movie: {e}")


    def remove_movie_from_favourites(self, movie_id, user_id):
        """"""
        try:
            movie = self.db.session.query(Movie).get(movie_id)
            if not movie:
                raise ValueError(f"Movie with ID {movie_id} not found.")
            user = self.db.session.query(User).get(user_id)
            if not user:
                raise ValueError(f"User with ID {user_id} not found.")

            if movie in user.movies:
                user.movies.remove(movie)
                self.db.session.commit()
            if len(movie.users) == 0:
                db.session.delete(movie)
                db.session.commit()
            return f"The movie '{movie.title}' has been removed from your list."

        except ValueError as e:
            self.db.session.rollback()
            print(e)
        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"A database error occurred while updating the movie: {e}")


    def get_user(self, user_id):
        """"""
        try:
            user = self.db.session.query(User) \
            .filter(User.id == user_id).first()
            if not user:
                return "Unknown"
            return user

        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"A database error occurred at getting all users: {e}")


    def get_movie(self, movie_id):
        """"""
        try:
            movie = self.db.session.query(Movie) \
            .filter(Movie.id == movie_id).first()
            if not movie:
                return "Unknown"
            return movie

        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"A database error occurred at getting all movies: {e}")




#Functions for input validation:
    def _username_already_used(self, new_username):
        existing_user = self.db.session.query(User).filter(User.name == new_username).first()
        if existing_user:
            return True
        else:
            return False

    def _input_not_string(self, new_input):
        if isinstance(new_input, str):
            return False
        else:
            return True

    def _input_not_int(self, new_input):
        if isinstance(new_input, int):
            return False
        else:
            return True

    def _input_not_float_or_None(self, new_input):
        if isinstance(new_input, float) or None:
            return False
        else:
            return True








