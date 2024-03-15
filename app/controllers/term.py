from flask import render_template, Blueprint
from app.models.tables import Term
from app.models.term_forms import TermCreationForm

from flask_login import AnonymousUserMixin, current_user
from app.controllers.user import is_user_admin

term_blueprint = Blueprint('term', __name__)


@term_blueprint.route('/term/<term_content>')
def term_data(term_content):
    term = Term.get_term_by_content(term_content)

    return render_template('entry.html', term=term, enumerate=enumerate, format=format,
                           user_is_admin=is_user_admin(current_user))


@term_blueprint.route('/search/<search_query>')
def term_search(search_query):
    terms = Term.search_for_related_terms(search_query)

    return render_template('search_entry.html', search_query=search_query, terms=terms,
                           user_is_admin=is_user_admin(current_user))


@term_blueprint.route('/create_term')
def term_creation():
    form = TermCreationForm()

    return render_template('create-entry.html', form=form)
