import logger.logger
import logging
from flask import Flask, request, abort
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_ECHO, SQLALCHEMY_TRACK_MODIFICATIONS, BCRYPT_LOG_ROUNDS
from DB.database import connect_db_to_app
from DB.bootstrap import bootstrap


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_ECHO'] = SQLALCHEMY_ECHO
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['BCRYPT_LOG_ROUNDS'] = BCRYPT_LOG_ROUNDS



    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    
    connect_db_to_app(app)

    with app.app_context():
        import routes.message
        import routes.error
        import routes.user
        bootstrap()
        return app


app = create_app()
# init routes

# if __name__ == "__main__":
#     app.run()
