from flask import render_template, Blueprint, redirect, url_for, flash
from flask_login import AnonymousUserMixin, login_required, login_user, logout_user, current_user

dashboard_blueprint = Blueprint('dashboard', __name__)


@login_required
@dashboard_blueprint.route('/dashboard')
def index():
    return render_template("dashboard-index.html")
