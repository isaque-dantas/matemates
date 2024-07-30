from flask import render_template, Blueprint
from flask_login import login_required, current_user

from app.models.tables import KnowledgeAreaRepository

from app.controllers.user import is_user_logged_in, is_user_admin

dashboard_blueprint = Blueprint('dashboard', __name__)


@dashboard_blueprint.route('/dashboard')
def index():
    return render_template("dashboard-index.html", knowledge_areas=KnowledgeAreaRepository.get_all(),
                           user=current_user, is_current_user_logged_in=is_user_logged_in(current_user),
                           is_user_admin=is_user_admin(current_user))
