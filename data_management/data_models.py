from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    """"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    movies = db.relationship('Movie', backref='user')


    def __str__(self):
        """Returns a string representation of the user."""
        return f"User(name = {self.name})"


class Movie(db.Model):
    """"""
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    director = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)                    # Datatype depends what you get change later maybe.
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)


    def __str__(self):
        """Returns a string representation of the movie."""
        return f"Movie(title = {self.title}, rating = {self.rating})"
