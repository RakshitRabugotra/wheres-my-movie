from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
import datetime

# Create the database instance
db = SQLAlchemy()


def get_uuid():
    """
    Generates a new unique id
    """
    return uuid4().hex


def now():
    """
    Returns the current timestamp
    """
    return datetime.datetime.now()


from .admin import Admin
from .user import User
