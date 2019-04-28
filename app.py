from flask import Flask, logging
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from logging.config import dictConfig
from internal_logger.logging_config import logging_config
from itsdangerous import URLSafeSerializer

dictConfig(logging_config)
app = Flask(__name__)

#TODO: move to config file
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/book_shop'
app.config['SECRET_KEY'] = 'very_secret_key'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
serializer = URLSafeSerializer(app.secret_key)

logger = logging.getLogger()


if __name__ == "__main__":
    app.run(debug=True)

# Can it be done another way? Think about
from handlers import *


