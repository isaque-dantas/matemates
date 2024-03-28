document.addEventListener('DOMContentLoaded', () => {
    const userDataPromise = getUserData()

    const editButton = document.querySelector('button#edit-button')
    const resetUserDataButton = document.querySelector('button#reset-user-data-button')
    const enableOnEditFormFields = document.querySelectorAll('.enable-on-edit')
    const showWhenEditing = document.querySelector('.buttons#show-when-editing')
    const hideWhenEditing = document.querySelector('.buttons#hide-when-editing')

    editButton.addEventListener('click', () => {
        enableOnEditFormFields.forEach((enableOnEditFormField) => {
            enableOnEditFormField.disabled = false

            showWhenEditing.classList.remove('d-none')
            hideWhenEditing.classList.add('d-none')
        })
    })

    resetUserDataButton.addEventListener('click', () => {
        enableOnEditFormFields.forEach((enableOnEditFormField) => {
            enableOnEditFormField.disabled = true
        })

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

    console.log(userData)

    for (const formFieldID in userData) {
        const formField = document.querySelector(`#${formFieldID}`)
        formField.value = userData[formFieldID]
    }
}
