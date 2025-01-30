from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from datamanager.data_manager_interface import DataManagerInterface
from datamanager.data_models import User, Movie, db
from omdbapi.API_Movies import api_request_data


class SQLiteDataManager(DataManagerInterface):
    """A data manager class that interacts with a SQLite database to manage users and their movie collections."""

    def __init__(self, db):
        """Initializes the SQLiteDataManager with the provided SQLAlchemy database session.
        Args:
            db: Initialize database connection with db."""
        self.db = db


    def get_all_users(self):
        """
        Retrieves all users from the database.

        Returns:
            list: List of users as objects.
        """
        try:
            list_of_all_users = self.db.session.query(User).all()
            return list_of_all_users

        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"A database error occurred at getting all users: {e}")


    def get_all_movies(self):
        """
        Retrieves all movies from the database.

        Returns:
            list: List of movies as objects.
        """
        try:
            list_of_all_movies = self.db.session.query(Movie).all()
            return list_of_all_movies

        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"A database error occurred at getting all movies: {e}")


    def get_user_movies(self, user_id):
        """
        Retrieves the movies associated with a user by their user ID.

        Args:
            user_id (int): The ID of the user from whom to retrieve movies.

        Returns:
            list: A list of Movie objects associated with the user.

        Raises:
            ValueError: If the user with the given ID does not exist.
        """
        try:
            user = self.db.session.query(User).get(user_id)
            if not user:
                raise ValueError(f"User with ID {user_id} not found.")
            movies = user.movies
            return movies

        except ValueError as e:
            self.db.session.rollback()
            print(e)
            return "error"
        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"A database error occurred getting the assigned movies from a user: {e}")


    def add_user(self, input_username):
        """
        Adds a new user to the database.

        Args:
            input_username (str): The username to be added.

        Raises:
            TypeError: If the input username is not a string.
            ValueError: If the username is already taken.
        """
        if self._input_not_string(input_username):
            raise TypeError("Username must be a string.")
        if self._username_already_used(input_username):
            return "Username is already used."

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
        """
        Adds a movie to the user's collection.

        Args:
            user_id (int): The ID of the user to whom the movie should be added.
            movie_name (str): The name of the movie to add.

        Returns:
            str: A success or failure message which will be displayed on user_favourites.html .
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
        """
        Updates the details of a movie in the user's collection, does not affect the same movie of other users,
        because a new movie with the new data will be created

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie to update.
            new_title (str): The new title of the movie.
            new_director (str): The new director of the movie.
            new_publication_year (string): The new publication year of the movie. Later changed to (int).
            new_rating (string): The new rating of the movie. Later changed to (float).

        Returns:
            str: A success or failure message.

        Raises:
            TypeError: If the input data is not of the expected type.
        """
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
        """
        Removes a movie from the user's collection and deletes it if no users are left with the movie.

        Args:
            movie_id (int): The ID of the movie to remove.
            user_id (int): The ID of the user from whose collection the movie should be removed.

        Returns:
            str: A success or failure message.
        """
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
        """
        Retrieves a user by their ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            User: The User object if found, otherwise "Unknown".
        """
        try:
            user = self.db.session.query(User) \
            .filter(User.id == user_id).first()
            if not user:
                return "error"
            return user

        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"A database error occurred at getting all users: {e}")


    def get_movie(self, movie_id):
        """
        Retrieves a movie by its ID.

        Args:
            movie_id (int): The ID of the movie to retrieve.

        Returns:
            Movie: The Movie object if found, otherwise "Unknown".
        """
        try:
            movie = self.db.session.query(Movie) \
            .filter(Movie.id == movie_id).first()
            if not movie:
                return "error"
            return movie

        except SQLAlchemyError as e:
            self.db.session.rollback()
            print(f"A database error occurred at getting all movies: {e}")


    def _username_already_used(self, new_username):
        """Checks if the username is already taken."""
        existing_user = self.db.session.query(User).filter(User.name == new_username).first()
        if existing_user:
            return True
        else:
            return False

    def _input_not_string(self, new_input):
        """Validates if the input is not a string."""
        if isinstance(new_input, str):
            return False
        else:
            return True

    def _input_not_int(self, new_input):
        """Validates if the input is not an integer."""
        if isinstance(new_input, int):
            return False
        else:
            return True

    def _input_not_float_or_None(self, new_input):
        """Validates if the input is neither a float nor None."""
        if isinstance(new_input, float) or None:
            return False
        else:
            return True








