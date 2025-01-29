from datamanager.data_models import User, Movie, db
from abc import ABC, abstractmethod



class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_all_movies(self):
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        pass

    @abstractmethod
    def add_user(self, input_name):
        pass

    @abstractmethod
    def add_movie_to_user(self, user_id, movie_id):
        pass

    @abstractmethod
    def update_movie(self, user_id, movie_id, new_title, new_director, new_publication_year, new_rating):
        pass

    @abstractmethod
    def remove_movie_from_favourites(self, movie_id, user_id):
        pass

    @abstractmethod
    def get_user(self, user_id):
        pass

    @abstractmethod
    def get_movie(self, movie_id):
        pass
















