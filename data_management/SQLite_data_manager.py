from flask_sqlalchemy import SQLAlchemy
from data_management.data_manager_interface import DataManagerInterface
from data_management.data_models import User, Movie, db

class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name):
        self.db = SQLAlchemy(db_file_name)

    def get_all_users(self):
        pass

    def get_user_movies(self, user_id):
        pass

    def get_user_favourites(self, user_id):
        pass

    def add_user(self, input_name):
        user = User(
            name = input_name,
        )
        db.add(user)
        db.commit()

    def add_movie(self,input_title, input_director, input_publication_year, input_rating):
        movie = Movie(
            title = input_title,
            director = input_director,
            publication_year = input_publication_year,
            rating = input_rating
        )
        db.add(movie)
        db.commit()

    def add_movie_to_user_favourites(self, user_id):
        pass

    def update_user(self, user_id):
        pass

    def update_movie(self, movie_id):
        pass

    def delete_user(self, user_id):
        pass

    def delete_movie(self, movie_id):
        pass


