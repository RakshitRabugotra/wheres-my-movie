from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager

# To export to the app
from app.models import db

# Passwords and cryptography
bcrypt = Bcrypt()
# For database management
migrate = Migrate()
# For user state management
login_manager = LoginManager()
