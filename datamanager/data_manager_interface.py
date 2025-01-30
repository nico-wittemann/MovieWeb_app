from datamanager.data_models import User, Movie, db
from abc import ABC, abstractmethod



class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        """Abstract method to get all users from the database."""
        pass


    @abstractmethod
    def get_all_movies(self):
        """Abstract method to get all movies from the database."""
        pass


    @abstractmethod
    def get_user_movies(self, user_id):
        """Abstract method to get all movies assigned to a specific user by their ID."""
        pass


    @abstractmethod
    def add_user(self, input_name):
        """Abstract method to add a new user to the system. Takes username as input."""
        pass


    @abstractmethod
    def add_movie_to_user(self, user_id, movie_id):
        """Abstract method to associate a movie with a user by their respective IDs"""
        pass


    @abstractmethod
    def update_movie(self, user_id, movie_id, new_title, new_director, new_publication_year, new_rating):
        """Abstract method to update a movie's details for a given user, if another user is using the movie it wont
        change his movie details.
        It allows modification of the movie's title, director, publication year, and rating.
        """
        pass


    @abstractmethod
    def remove_movie_from_favourites(self, movie_id, user_id):
        """Abstract method to remove a movie from the user's list of favourites."""
        pass


    @abstractmethod
    def get_user(self, user_id):
        """Abstract method to get a user by their ID."""
        pass


    @abstractmethod
    def get_movie(self, movie_id):
        """Abstract method to get a movie by its ID."""
        pass
















