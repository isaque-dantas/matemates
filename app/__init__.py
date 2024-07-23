from flask import Flask
from flask_login import LoginManager

from app.secret_keys import FLASK_SECRET_KEY, MYSQL_USER_PASSWORD, MYSQL_USER

app = Flask(__name__)

app.config['SECRET_KEY'] = FLASK_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f'mysql+pymysql://{MYSQL_USER}:{MYSQL_USER_PASSWORD}@localhost/matemates_db'

from app.controllers import entry, user, dashboard, errors

app.register_blueprint(errors.errors_blueprint)
app.register_blueprint(user.user_blueprint)
app.register_blueprint(entry.entry_blueprint)
app.register_blueprint(dashboard.dashboard_blueprint)

from app.models.tables import UserRepository

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.login'
login_manager.login_message = 'Por favor, faça login para acessar essa página.'

@login_manager.user_loader
def load_user(user_id):
    return UserRepository.get_by_id(int(user_id))


if __name__ == '__main__':
    app.run(debug=True)
