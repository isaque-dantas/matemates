from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

from app.models.tables import User, Entry, Definition, Term, Syllable, Image, Question, KnowledgeArea

from app.models import db

# from app.secret_keys import FLASK_SECRET_KEY, MYSQL_USER_PASSWORD, MYSQL_USER

app = Flask(__name__)

app.config['SECRET_KEY'] = "bafjksjfdkasjdkf"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

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
