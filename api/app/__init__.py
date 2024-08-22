"""
Initialize Flask application and register blueprints for each set of routes:
"""

from flask import Flask
import pandas as pd

# Custom modules
from config import ApplicationConfig
from app.lib.movie_recommender import MovieRecommender

# Import the extensions
from .extensions import bcrypt, db, migrate, login_manager

# Create the app instance
app = Flask(__name__)

# Set the configurations from external object
app.config.from_object(ApplicationConfig)

# Create instance of recommender
movie_recommender = None

# Initialize extensions
bcrypt.init_app(app)
# Initialize the Database
db.init_app(app)

with app.app_context():
    db.create_all()
    engine = db.get_engine()
    # Read the 'movies' table into a pandas DataFrame
    movies = pd.read_sql_table("movies", con=engine)
    # Initialize the movie_recommender
    movie_recommender = MovieRecommender(movies)

# Initialize the migrator
migrate.init_app(app, db)

# For auth state management
login_manager.init_app(app)

# Import and register blueprints
from .routes.movies import movies_bp
from .routes.admin import admin_bp
from .routes.auth import auth_bp

# Register blueprints
app.register_blueprint(admin_bp, url_prefix="/_/admin")

# The APIS for db access
app.register_blueprint(movies_bp, url_prefix="/api/movies")
app.register_blueprint(auth_bp, url_prefix="/api/auth")
