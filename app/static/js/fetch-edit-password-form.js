document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('#edit-password-form')
    form.addEventListener('submit', () => {
        const formData = getFormDataFromForm(form)
        sendFormData(formData, form.action)
    })
})

function getFormDataFromForm(form) {
    return new FormData(form)
}

async function sendFormData(formData, url) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            "Content-Type": "multipart/form-data",
        },
        body: formData
    })

    if (!response.ok) {
        console.error(response.statusText)
    }
}