def get_form_data_from_request(request):
    form_data = dict(request.form)
    form_files = dict(request.files)
    if form_files:
        form_data.update(form_files)

    return form_data
