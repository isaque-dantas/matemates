document.addEventListener('DOMContentLoaded', () => {
    if (itsEditingPage()) {
        const entryDataPromise = getEntryData()

    }
})

function itsEditingPage() {
    return 'edit_entry' === location.href.split('/')[3]
}

async function getEntryData() {
    const response = await fetch(`/entry_data/${getEntryContent()}`)
    const json = await response.json()
    console.log(json)
    return json
}

async function updateDocumentFormData(entryDataPromise) {
    const entryData = await entryDataPromise

}

function getEntryContent() {
    return location.href.split('/')[4]
}

