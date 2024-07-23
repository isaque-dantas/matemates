from flask import render_template, Blueprint, redirect, url_for, flash, request, abort
from flask_login import AnonymousUserMixin, login_required, login_user, logout_user, current_user

from app.controllers import get_form_data_from_request

from app.models.tables import UserRepository
from app.models.user_forms import LoginForm, RegisterForm

from googleapiclient.errors import HttpError

user_blueprint = Blueprint('user', __name__)


def is_user_admin(user):
    if isinstance(user, AnonymousUserMixin):
        user_is_admin = False
    else:
        user_is_admin = user.is_admin()
    return user_is_admin


def is_user_logged_in(user) -> bool:
    return not isinstance(user, AnonymousUserMixin)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if is_user_logged_in(current_user):
        return redirect(url_for('dashboard.index'))

    form = LoginForm()
    return render_template('login.html', form=form)


@user_blueprint.route('/auth_user', methods=['POST'])
def auth_user():
    form_data = get_form_data_from_request(request)

    if 'email' not in form_data or 'password' not in form_data:
        return {
            'message': 'Insira o email e a senha, sem deixar nenhum deles vazios.',
            'category': 'warning',
            'user_was_logged': False
        }
    else:
        user = UserRepository.get_by_email(form_data['email'])

        print(form_data)

        if user is not None and user.is_password_valid(form_data['password']):
            login_user(user)
            return {
                'message': 'Login realizado com sucesso.',
                'category': 'success',
                'user_was_logged': True
            }
        else:
            return {
                'message': 'Email e/ou senha inválidos.',
                'category': 'danger',
                'user_was_logged': False
            }


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        try:
            print(f'request.files: {dict(request.files)}')
            print(f'request.form: {dict(request.form)}')
            form_data = get_form_data_from_request(request)

            UserRepository.register(form_data)
        except Exception as e:
            flash(str(e), category='danger')
        else:
            flash('Usuário criado com sucesso.', category='success')
            return redirect(url_for('user.login'))

    elif request.method == 'POST':
        flash('Verifique se todos os dados foram inseridos corretamente.', category='warning')

    return render_template('user-form.html', form=form, is_registering=True, endpoint='user.register',
                           is_current_user_logged_in=is_user_logged_in(current_user), user=current_user)


@user_blueprint.route('/perfil/', methods=['GET', 'POST'])
@login_required
def perfil():
    form = RegisterForm()

    form_data = get_form_data_from_request(request)
    if form_data:
        try:
            print(f'request.files: {dict(request.files)}')
            print(f'request.form: {dict(request.form)}')

            UserRepository.update_user(current_user, form_data)
            print('ended update')
        except Exception as e:
            flash(str(e), category='danger')
        else:
            flash('Perfil editado com sucesso.', category='success')
    elif request.method == 'POST':
        flash('Verifique se todos os dados foram inseridos corretamente.', category='warning')

    return render_template('user-form.html', user=current_user, form=form, is_registering=False, endpoint='user.perfil',
                           is_current_user_logged_in=is_user_logged_in(current_user))


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('user.login'))


@user_blueprint.route('/user_data/')
@login_required
def user_data():
    return current_user.get_dict_of_properties()


@user_blueprint.route('/delete_current_user/')
@login_required
def delete_current_user():
    user = UserRepository.get_by_id(current_user.id)
    logout_user()
    user.delete_user()
    return redirect(url_for('user.login'))


@user_blueprint.route('/invite_to_be_admin/<email>')
@login_required
def invite_to_be_admin(email):
    if is_user_admin(current_user):
        try:
            current_user.invite(email)
        except Exception as e:
            return {
                'message': str(e),
                'category': 'danger' if isinstance(e, HttpError) else 'info'
            }
        else:
            return {
                'message': 'Convite enviado com sucesso.',
                'category': 'success'
            }
    else:
        abort(403)


@user_blueprint.route('/accept_invite/<email>')
def accept_invite(email):
    user = UserRepository.get_by_email(email)
    if user is None:
        flash('Cadastre-se para continuar.', category='info')
        return redirect(url_for('user.register'))
    else:
        if is_user_logged_in(current_user):
            if current_user.email == email:
                user.accept_invite_to_be_admin()
                return redirect(url_for('dashboard.index'))
            else:
                abort(403)
        else:
            return redirect(url_for('user.login'))


@user_blueprint.route('/edit_password/<username>', methods=['POST'])
@login_required
def edit_password(username):
    if current_user.username == username:
        user = UserRepository.get_by_username(username)
        if request.form:
            form_data = get_form_data_from_request(request)
            try:
                user.edit_password(form_data)
            except Exception as e:
                return {
                    'message': str(e),
                    'category': 'danger'
                }
            else:
                return {
                    'message': 'Senha alterada com sucesso.',
                    'category': 'success'
                }
        else:
            return {
                'message': 'Algo deu errado. Tente novamente.',
                'category': 'warning'
            }
    else:
        abort(403)
