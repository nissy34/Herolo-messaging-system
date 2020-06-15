from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db_to_app(app):
    db.init_app(app)
    return app


