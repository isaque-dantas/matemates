from flask import render_template, Blueprint, abort, flash, request, url_for, redirect
from flask_login import current_user, login_required

from app.controllers.user import is_user_admin
from app.models.tables import Term
from app.models.term_forms import TermCreationForm

term_blueprint = Blueprint('term', __name__)


@term_blueprint.route('/term/<term_content>')
def term_data(term_content):
    term = Term.get_term_by_content(term_content)
    if term:
        return render_template('entry.html', term=term, enumerate=enumerate, format=format,
                               user_is_admin=is_user_admin(current_user))
    else:
        abort(404)

@term_blueprint.route('/validate/<term_content>')
def term_validate(term_content):
    term = Term.get_term_by_content(term_content)
    if term:
        return render_template('validate-entry.html', term=term, enumerate=enumerate, format=format,
                               user_is_admin=is_user_admin(current_user))
    else:
        abort(404)


@term_blueprint.route('/search/<search_query>')
def term_search(search_query):
    terms = Term.search_for_related_terms(search_query)

    return render_template('search_entry.html', search_query=search_query, terms=terms,
                           user_is_admin=is_user_admin(current_user))


@term_blueprint.route('/create_term', methods=['get', 'post'])
def term_creation():
    form = TermCreationForm()

    if form.validate_on_submit():
        try:
            Term.register(dict(request.form))
        except Exception as e:
            flash(str(e.args), category='danger')

    return render_template('create-entry.html', form=form)


@login_required
@term_blueprint.route('/delete_term/<term_content>')
def term_deletion(term_content):
    if is_user_admin(current_user):
        term = Term.get_term_by_content(term_content)
        term.delete_term()

        return redirect(url_for('dashboard.index'))
    else:
        abort(403)
