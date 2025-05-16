from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

user_movie_association  = db.Table(
    'user_movie',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True)
)

class User(db.Model):
    """User Table"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    movies = db.relationship('Movie', secondary=user_movie_association, back_populates='users')

    def __str__(self):
        """Returns a string representation of the user."""
        return f"User(name = {self.name})"


class Movie(db.Model):
    """Movie Table"""
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    director = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=True)
    poster_url = db.Column(db.String, nullable=True)
    users = db.relationship('User', secondary=user_movie_association, back_populates='movies')

    def __str__(self):
        """Returns a string representation of the movie."""
        return f"Movie(title = {self.title}, rating = {self.rating})"
