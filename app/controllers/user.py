from flask import render_template, Blueprint, redirect, url_for, flash, request, abort
from flask_login import AnonymousUserMixin, login_required, login_user, logout_user, current_user

from app.controllers import get_form_data_from_request

from app.models.tables import User
from app.models.user_forms import LoginForm, RegisterForm

user_blueprint = Blueprint('user', __name__)


def is_user_admin(user):
    if isinstance(user, AnonymousUserMixin):
        user_is_admin = False
    else:
        user_is_admin = user.is_admin()
    return user_is_admin


def is_current_user_logged_in() -> bool:
    return not isinstance(current_user, AnonymousUserMixin)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if is_current_user_logged_in():
        return redirect(url_for('dashboard.index'))

    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)

        if user is not None and user.is_password_valid(form.password.data):
            login_user(user)
            return redirect(url_for('dashboard.index'))
        else:
            flash('Email e/ou senha inválidos',
                  category='danger')

    return render_template('login.html', form=form)


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        try:
            print(f'request.files: {dict(request.files)}')
            print(f'request.form: {dict(request.form)}')
            form_data = get_form_data_from_request(request)

            User.register(form_data)
        except Exception as e:
            flash(str(e), category='danger')
        else:
            flash('Usuário criado com sucesso.', category='success')
            return redirect(url_for('user.login'))

    elif request.method == 'POST':
        flash('Verifique se todos os dados foram inseridos corretamente.', category='warning')

    return render_template('register.html', form=form)


@user_blueprint.route('/perfil/<username>', methods=['GET', 'POST'])
def perfil(username):
    if current_user.username == username:
        print(current_user.get_parsed_name())
        return render_template('perfil.html', user=current_user)
    else:
        abort(403)


@user_blueprint.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('user.login'))


@login_required
@user_blueprint.route('/user_data/<username>')
def user_data(username):
    if current_user.username == username:
        return current_user.get_dict_of_properties()
    else:
        abort(403)
