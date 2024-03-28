from flask import render_template, Blueprint, redirect, url_for, flash
from flask_login import AnonymousUserMixin, login_required, login_user, logout_user, current_user

from app.models.tables import KnowledgeArea

dashboard_blueprint = Blueprint('dashboard', __name__)


@dashboard_blueprint.route('/dashboard')
@login_required
def index():
    return render_template("dashboard-index.html", knowledge_areas=KnowledgeArea.get_all(), list=list)
