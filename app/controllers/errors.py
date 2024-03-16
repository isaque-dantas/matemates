from flask import render_template, Blueprint, abort

errors_blueprint = Blueprint('errors', __name__)


@errors_blueprint.app_errorhandler(403)
def forbidden(error):
    return render_template('http_error.html', error_code=error.code,
                           error_description='Você não tem permissão de acessar essa página.')


@errors_blueprint.app_errorhandler(404)
def page_not_found(error):
    return render_template('http_error.html', error_code=error.code,
                           error_description='Página não encontrada.')
