from flask import Flask
from app.secret_keys import FLASK_SECRET_KEY, MYSQL_USER_PASSWORD

app = Flask(__name__)


app.config['SECRET_KEY'] = FLASK_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f'mysql+pymysql://dba_matemates:{MYSQL_USER_PASSWORD}@localhost/matemates_db'

from app.controllers import term

app.register_blueprint(term.blueprint)

if __name__ == '__main__':
    app.run(debug=True)
