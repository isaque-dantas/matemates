from flask import render_template, Blueprint, abort, flash, request, url_for, redirect
from flask_login import current_user, login_required

from app.controllers.user import is_user_admin
from app.models.tables import Entry
from app.models.entry_forms import EntryCreationForm

entry_blueprint = Blueprint('entry', __name__)


@entry_blueprint.route('/entry/<entry_content>')
def view_entry(entry_content):
    entry = Entry.get_entry_by_content(entry_content.replace('_', ' '))
    if entry:
        if is_user_admin(current_user):
            return render_template('entry.html', entry=entry, enumerate=enumerate, format=format,
                                   user_is_admin=is_user_admin(current_user))
        else:
            if entry.is_validated:
                return render_template('entry.html', entry=entry, enumerate=enumerate, format=format,
                                       user_is_admin=is_user_admin(current_user))
            else:
                abort(403)
    else:
        abort(404)


@entry_blueprint.route('/search/<search_query>')
def entry_search(search_query):
    entries = Entry.search_for_related_entries(search_query)
    print(f'entries: {entries}')

    return render_template('search_entry.html', search_query=search_query, entries=entries,
                           user_is_admin=is_user_admin(current_user))


@login_required
@entry_blueprint.route('/create_entry', methods=['GET', 'POST'])
def entry_creation():
    if is_user_admin(current_user):
        form = EntryCreationForm()

        if form.validate_on_submit():
            try:
                print(f'request.files: {dict(request.files)}')
                print(f'request.form: {dict(request.form)}')
                form_data = dict(request.form)
                form_files = dict(request.files)
                form_data.update(form_files)
                new_entry = Entry.register(form_data)
            except Exception as e:
                flash(str(e), category='danger')
            else:
                flash('Verbete criado com sucesso.', category='success')
                return redirect(url_for('entry.view_entry', entry_content=new_entry.content))
        elif request.method == 'POST':
            flash('Verifique se todos os dados foram inseridos corretamente.', category='warning')

        return render_template('create-entry.html', form=form, user_is_admin=is_user_admin(current_user))
    else:
        abort(403)


@login_required
@entry_blueprint.route('/validate_entry/<entry_content>')
def validate_entry(entry_content):
    if is_user_admin(current_user):
        entry = Entry.get_entry_by_content(entry_content)
        entry.turn_valid()
        return redirect(url_for('entry.view_entry', entry_content=entry_content))
    else:
        abort(403)


@login_required
@entry_blueprint.route('/delete_entry/<entry_content>')
def delete_entry(entry_content):
    if is_user_admin(current_user):
        entry = Entry.get_entry_by_content(entry_content)
        entry.delete_entry()

        return redirect(url_for('dashboard.index'))
    else:
        abort(403)
