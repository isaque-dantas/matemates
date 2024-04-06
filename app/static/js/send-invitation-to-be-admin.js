

document.addEventListener('DOMContentLoaded', () => {
    const emailInput = document.querySelector('input#input-email-to-invite')
    const sendInvitationButton = document.querySelector('button#send-invitation-btn')

    sendInvitationButton.addEventListener('click', () => {
        const email = getEmailFromInput(emailInput)
        if (email) {
            sendInvitationRequest(email)
        }
    })
})

function getEmailFromInput(input) {
    const inputValue = input.value
    if (emailIsValid(inputValue)) {
        return inputValue
    } else {
        updateInvitationFeedback( {'message': 'O e-mail informado não é válido.', 'category': 'danger'} )
        return undefined
    }
}

function emailIsValid(email) {
    const emailRegexPattern = new RegExp('^([\\w\-.]+)@([\\w\-]+[.])+([\\w\-]{2,})$', 'm')
    return emailRegexPattern.test(email)
}

async function sendInvitationRequest(email) {
    const response = await fetch(`/invite_to_be_admin/${email}`)

    if (!response.ok) {
        console.error(response.statusText)
    }
    const jsonResponse = await response.json()
    updateInvitationFeedback(jsonResponse)
}

async function updateInvitationFeedback(response) {
    console.log(response)

    const invitationFeedback = document.querySelector('#invitation-feedback')
    invitationFeedback.textContent = response.message

    const invitationFeedbackClasses = invitationFeedback.classList
    invitationFeedbackClasses.forEach((invitationFeedbackClass) => {
        if (invitationFeedbackClass.includes('text')) {
            invitationFeedback.classList.remove(invitationFeedbackClass)
            invitationFeedback.classList.add(`text-${response.category}`)
        }
    })

    if (invitationFeedbackClasses.contains('d-none')) {
        invitationFeedback.classList.remove('d-none')
    }
}
