document.addEventListener('DOMContentLoaded', () => {
    const userDataPromise = getUserData()

    const editButton = document.querySelector('button#edit-button')
    const resetUserDataButton = document.querySelector('button#reset-user-data-button')
    const enableOnEditFormFields = document.querySelectorAll('.enable-on-edit')
    const showWhenEditing = document.querySelector('.buttons#show-when-editing')
    const hideWhenEditing = document.querySelector('.buttons#hide-when-editing')

    updateDocumentData(userDataPromise)
    disableFormFields(enableOnEditFormFields)

    editButton.addEventListener('click', () => {
        enableFormFields(enableOnEditFormFields)

        showWhenEditing.classList.remove('d-none')
        hideWhenEditing.classList.add('d-none')
    })

    resetUserDataButton.addEventListener('click', () => {
        disableFormFields(enableOnEditFormFields)
        updateDocumentData(userDataPromise)

        showWhenEditing.classList.add('d-none')
        hideWhenEditing.classList.remove('d-none')
    })
})

async function getUserData() {
    const response = await fetch(`/user_data/`)

    if (!response.ok) {
        console.error(response.statusText)
    }

    return response.json()
}

async function updateDocumentData(userDataPromise) {
    const userData = await userDataPromise

    for (const formFieldID in userData) {
        const formField = document.querySelector(`#${formFieldID}`)
        if (formField !== null) {
            formField.value = userData[formFieldID]
        }
    }
}

function enableFormFields(formFields) {
    formFields.forEach((formField) => {
        formField.disabled = false
    })
}

function disableFormFields(formFields) {
    formFields.forEach((formField) => {
        formField.disabled = true
    })
}
