# Custom utilities
from . import db


# Model for Movies
class Movies(db.Model):
    __tablename__ = "movies"
    movieId = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.Text, nullable=False)
    genres = db.Column(db.Text)
    tags = db.Column(db.Text)
    rating = db.Column(db.Float)
    imdbId = db.Column(db.Integer, nullable=False)
    tmdbId = db.Column(db.Integer)

    @staticmethod
    def get_fields() -> list:
        """
        Returns all of the fields used in here
        """
        return [
            "movieId",
            "title",
            "genres",
            "tags",
            "rating",
            "imdbId",
            "tmdbId",
        ]

    # Serializes the object
    @staticmethod
    def serialize(movie) -> dict:
        return {
            "movieId": movie.movieId,
            "title": movie.title,
            "genres": movie.genres,
            "tags": movie.tags,
            "rating": movie.rating,
            "imdbId": movie.imdbId,
            "tmdbId": movie.tmdbId,
        }
