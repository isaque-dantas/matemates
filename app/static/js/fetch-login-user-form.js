document.addEventListener('DOMContentLoaded', () => {
    getNextPageURLFromURL()
    document.querySelector('#submit').addEventListener('click', () => {
        const formData = getFormData()

        if (formData.has('email') && formData.has('password')) {
            const jsonResponsePromise = sendFormData(formData, '/auth_user')
            jsonResponsePromise.then((response) => {
                updateFeedbackMessage(response)

                console.log(response)

                if (response['user_was_logged']) {
                    const nextPageURL = getNextPageURLFromURL()
                    if (nextPageURL !== undefined) {
                        updateNextPageButton(nextPageURL)
                    } else {
                        updateNextPageButton('/dashboard')
                    }
                }
            })
        } else {
            updateFeedbackMessage({'message': 'Insira o e-mail e a senha.', 'category': 'danger'})
        }
    })
})

async function sendFormData(formData, url) {
    const response = await fetch(url, {
        method: 'POST',
        body: formData
    })

    if (!response.ok) {
        console.error(response.statusText)
    }
    return await response.json()
}

function getFormData() {
    const formData = new FormData()
    document.querySelectorAll('.form-control').forEach((formInput) => {
        if (formInput.value !== '') {
            formData.append(formInput.name, formInput.value)
        }
    })

    return formData
}

function updateNextPageButton(nextPageURL) {
    const nextPageButton = document.querySelector('a#next-page-btn')
    nextPageButton.href = nextPageURL
    nextPageButton.classList.replace('d-none', 'd-inline-block')

    document.querySelector('#submit').classList.add('d-none')
}

function getNextPageURLFromURL() {
    const url = new URL(location.href)
    const urlParameters = new URLSearchParams(url.search)

    console.log(urlParameters)
    console.log(urlParameters.get('next'))

    if (urlParameters.has('next')) {
        return urlParameters.get('next')
    } else {
        return undefined
    }
}
