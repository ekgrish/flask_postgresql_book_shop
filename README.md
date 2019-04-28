# flask_postgresq_book_shop

initial settings: <br />
You need to create new db(postgreSQL) with following name or password:
postgresql://postgres:123@localhost/book_shop  <br />
name: book_shop  <br />
pass: 123  <br />
or just change app.config['SQLALCHEMY_DATABASE_URI'] in app.py to yours ones  <br />

to fill db: <br />
from app import app <br />
from app import db <br />
db.create_all() <br />
from initial_data_to_db import fill_db_with_data <br />
fill_db_with_data()  <br />

to start app: <br />
app.run()

