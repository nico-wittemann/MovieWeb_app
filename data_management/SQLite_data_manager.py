from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from data_management.data_manager_interface import DataManagerInterface
from data_management.data_models import User, Movie, db



class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db):
        self.db = db

    def get_all_users(self):
        pass

    def get_all_movies(self):
        pass

    def get_user_movies(self, user_id):
        pass

    def get_user_favourites(self, user_id):
        pass

    def add_user(self, input_name): # No input validation yet!!! No errors yet!
        user = User(
            name = input_name,
        )
        self.db.session.add(user)
        self.db.session.commit()

    def add_movie(self,input_title, input_director, input_publication_year, input_rating):  # No input validation yet!!! No errors yet!
        movie = Movie(
            title = input_title,
            director = input_director,
            publication_year = input_publication_year,
            rating = input_rating
        )
        self.db.session.add(movie)
        self.db.session.commit()

    def add_movie_to_user_favourites(self, user_id):
        pass

    def update_user(self, user_id, new_name):  # No input validation yet!!! No errors yet!
        user_to_update = self.db.session.query(User) \
            .filter(User.id == user_id) \
            .one()
        user_to_update.name = new_name
        self.db.session.commit()

    def update_movie(self, movie_id, new_title, new_director, new_publication_year, new_rating): # No input validation yet!!!
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
        pass

    def delete_movie(self, movie_id):
        pass


