from flask import Flask
from app.controllers import default
from app.secret_keys import FLASK_SECRET_KEY, MYSQL_USER_PASSWORD

app = Flask(__name__)

app.config['SECRET_KEY'] = FLASK_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f'mysql+pymysql://dba_matemates:{MYSQL_USER_PASSWORD}@localhost/matemates_db'

app.register_blueprint(default.blueprint)
