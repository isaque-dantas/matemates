from flask import render_template, Blueprint, abort, flash, request, url_for, redirect
from flask_login import current_user, login_required

from app.controllers.user import is_user_admin
from app.models.tables import Entry
from app.models.entry_forms import EntryCreationForm

entry_blueprint = Blueprint('entry', __name__)


@entry_blueprint.route('/entry/<entry_content>')
def entry_data(entry_content):
    entry = Entry.get_entry_by_content(entry_content)
    if entry:
        return render_template('entry.html', entry=entry, enumerate=enumerate, format=format,
                               user_is_admin=is_user_admin(current_user))
    else:
        abort(404)


@entry_blueprint.route('/search/<search_query>')
def entry_search(search_query):
    entries = Entry.search_for_related_entries(search_query)

    return render_template('search_entry.html', search_query=search_query, entries=entries,
                           user_is_admin=is_user_admin(current_user))


@entry_blueprint.route('/create_entry', methods=['get', 'post'])
def entry_creation():
    form = EntryCreationForm()

    try:
        if form.validate_on_submit():
            print(f'request.files: {dict(request.files)}')
            print(f'request.form: {dict(request.form)}')
            form_data = dict(request.form)
            form_files = dict(request.files)
            form_data.update(form_files)
            Entry.register(form_data)
    except Exception as e:
        flash(str(e), category='danger')

    return render_template('create-entry.html', form=form, user_is_admin=is_user_admin(current_user))


@login_required
@entry_blueprint.route('/delete_entry/<entry_content>')
def entry_deletion(entry_content):
    if is_user_admin(current_user):
        entry = Entry.get_entry_by_content(entry_content)
        entry.delete_entry()

        return redirect(url_for('dashboard.index', user_is_admin=is_user_admin(current_user)))
    else:
        abort(403)
