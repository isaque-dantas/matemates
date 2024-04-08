async function updateFeedbackMessage(response) {
    const feedbackMessage = document.querySelector('#feedback-message')
    feedbackMessage.textContent = response.message

    const feedbackMessageClasses = feedbackMessage.classList
    feedbackMessageClasses.forEach((feedbackMessageClass) => {
        if (feedbackMessageClass.includes('text')) {
            feedbackMessage.classList.remove(feedbackMessageClass)
            feedbackMessage.classList.add(`text-${response.category}`)
        }
    })
    feedbackMessage.style.opacity = 1
    setTimeout(() => {feedbackMessage.style.opacity = 0}, 7500)
}