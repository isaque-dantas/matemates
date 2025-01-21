from os import getenv

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

from app.models import db
from app.models.tables import User, Entry, Definition, Term, Syllable, Image, Question, KnowledgeArea

app = Flask(__name__)

# load_dotenv("../.env")
# DB_USERNAME = getenv("DB_USERNAME")
# DB_PASSWORD = getenv("DB_PASSWORD")
# DB_HOST = getenv("DB_HOST")
# DB_DATABASE = getenv("DB_DATABASE")
# FLASK_SECRET_KEY = getenv("FLASK_SECRET_KEY")

app.config['SECRET_KEY'] = "bafjksjfdkasjdkf"
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///database.db'

db.init_app(app)
migrate = Migrate(app, db)

from app.controllers import entry, user, dashboard, errors

app.register_blueprint(errors.errors_blueprint)
app.register_blueprint(user.user_blueprint)
app.register_blueprint(entry.entry_blueprint)
app.register_blueprint(dashboard.dashboard_blueprint)

from app.models.tables import User

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.login'
login_manager.login_message = 'Por favor, faça login para acessar essa página.'


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))


if __name__ == '__main__':
    app.run(debug=True)
