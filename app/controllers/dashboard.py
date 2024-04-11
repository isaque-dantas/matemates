from flask import render_template, Blueprint
from flask_login import login_required, current_user

from app.models.tables import KnowledgeArea

from app.controllers.user import is_user_logged_in

dashboard_blueprint = Blueprint('dashboard', __name__)


@dashboard_blueprint.route('/dashboard')
def index():
    return render_template("dashboard-index.html", knowledge_areas=KnowledgeArea.get_all(), list=list,
                           user=current_user, is_current_user_logged_in=is_user_logged_in(current_user))
