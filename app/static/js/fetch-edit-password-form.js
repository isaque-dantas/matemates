document.addEventListener('DOMContentLoaded', () => {
    const submitButton = document.querySelector('#edit-password-form-submit')
    const urlPromise = getEditPasswordURLPromise()

    submitButton.addEventListener('click', () => {
        const formData = getFormData()
        sendFormData(formData, urlPromise)
    })
})

function getFormData() {
    const formData = new FormData()
    const inputs = document.querySelectorAll('input.edit-password-form-input')
    inputs.forEach((input) => {
        formData.append(input.name, input.value)
    })

    return formData
}

async function sendFormData(formData, urlPromise) {
    const url = await urlPromise
    const response = await fetch(url, {
        method: 'POST',
        body: formData
    })

    if (!response.ok) {
        console.error(response.statusText)
    }

    updateFeedbackMessage(await response.json())
}

async function getEditPasswordURLPromise() {
    const username = await getCurrentUserUsernamePromise()
    return `/edit_password/${username}`
}

async function getCurrentUserUsernamePromise() {
    const response = await fetch('/user_data/')

    if (!response.ok) {
        console.error(response.statusText)
    }

    const jsonResponse = await response.json()
    return jsonResponse['username']
}
