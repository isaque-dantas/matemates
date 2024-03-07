from flask import render_template, Blueprint

blueprint = Blueprint('default', __name__)


@blueprint.route('/')
@blueprint.route('/index')
def index():
    return render_template('usuario.html')


