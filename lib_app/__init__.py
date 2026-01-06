from flask import Flask
from .config import Config
from .extensions import db, login_manager, migrate

# blueprints
from .auth.routes import auth_bp
from .books.routes import books_bp
from .main.routes import main_bp

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_class)

    # initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(main_bp)

    return app