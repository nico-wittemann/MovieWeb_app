from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from datamanager.data_manager_interface import DataManagerInterface
from datamanager.data_models import User, Movie, db
from API_Movies import api_request_data


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db):
        self.db = db


    def get_all_users(self):
        """

        :return:
        """
        try:
            list_of_all_users = self.db.session.query(User).all()
            return list_of_all_users

        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"A database error occurred at getting all users: {e}")

    def get_username_by_id(self, user_id):
        """
        """
        try:
            user = self.db.session.query(User) \
            .filter(User.id == user_id).first()
            if not user:
                return "Unknown"
            return user.name

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
        """"""
        try:
            user = self.db.session.query(User).get(user_id)
            if not user:
                raise ValueError(f"User with ID {user_id} not found.")
            movies = user.movies
            return movies # Careful it returns the object now (for loop and movie.title or .director) to get specifics

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


    def add_movie_to_user(self, user_id, movie_name): # Change later to title maybe, or make sure to display id in flask!
        """
        Prompt the user to enter a movie name, fetch its details from an API,
        and ensure it is not already in the movie collection.

        Args:
            movies (dict): A dictionary with existing movies,
                                where the keys are the movie titles.

        Returns:
            tuple: A tuple containing the movie details fetched from the API:
                        (title (str), year (str), rating (str), poster_url (str)).
                        These details are only returned if the movie is valid and
                        not already in the collection.
        """
        try:
            user = self.db.session.query(User).get(user_id)
            if not user:
                raise ValueError(f"User with ID {user_id} not found.")
            movie_name = movie_name.strip()
            api_data = api_request_data(movie_name)
            if api_data:
                title, publication_year, string_rating, poster_url, director = api_data
            else:
                return f"Title {(movie_name)} was not found in Database"
            movies = self.get_user_movies(user_id)
            titles = [movie.title for movie in movies]
            if title in titles:
                return f"Movie {title} already exist!"
            else:
                rating = float(string_rating.split("/")[0])
                new_movie = Movie(
                    title = title,
                    director = director,
                    publication_year = publication_year,
                    rating = rating,
                    poster_url = poster_url
                )
                user.movies.append(new_movie)
                self.db.session.commit()
                return f"Movie {title} successfully assigned to User {user.name}."

        except ValueError as e:
            self.db.session.rollback()
            print(e)
        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"A database error occurred while assigning movie to user: {e}")





    def update_movie(self, movie_id, new_title, new_director, new_publication_year, new_rating):
        """"""
        if self._input_not_string(new_title):
            raise TypeError("Title must be a string.")
        if self._input_not_string(new_director):
            raise TypeError("Director must be a string.")
        if self._input_not_int(new_publication_year):
            raise TypeError("Publication year must be an integer.")
        if self._input_not_float(new_rating):
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


    def delete_movie_from_favourites(self, movie_id): #DELETE FROM USERS LIST!
        """"""
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

    def _input_not_float(self, new_input):
        if isinstance(new_input, float):
            return False
        else:
            return True



# Not used but could be used for extension:
    def update_user(self, user_id, new_username):
        if self._input_not_string(new_username):
            raise TypeError("Username must be a string.")
        if self._username_already_used(new_username):
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






