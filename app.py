from flask import Flask, logging
import logging
from flask_sqlalchemy import SQLAlchemy
from logging.config import dictConfig
from internal_logger.logging_config import logging_config

dictConfig(logging_config)
app = Flask(__name__)

#TODO: move to config file
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/book_shop'

db = SQLAlchemy(app)
logger = logging.getLogger()


if __name__ == "__main__":
    app.run(debug=True)

# Can it be done another way? Think about
from handlers import *


