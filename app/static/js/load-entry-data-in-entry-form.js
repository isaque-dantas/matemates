document.addEventListener('DOMContentLoaded', () => {
    if (itsEditingPage()) {
        const entryDataPromise = getEntryData()
        updateDocumentFormData(entryDataPromise)
    }
})

function itsEditingPage() {
    return 'edit_entry' === location.href.split('/')[3]
}

async function getEntryData() {
    const response = await fetch(`/entry_data/${getEntryID()}`)
    return await response.json()
}

async function updateDocumentFormData(entryDataPromise) {
    const entryData = await entryDataPromise
    console.log(entryData)
    console.log()

    const fixedProperties = entryData['fixed_properties']
    updateDocumentFormFixedProperties(fixedProperties)

    const nProperties = entryData['n_properties']
    updateDocumentFormNProperties(nProperties)
}

function updateDocumentFormFixedProperties(fixedProperties) {
    for (const fixedProperty in fixedProperties) {
        const formField = document.querySelector(`[name="${fixedProperty}"]`)

        setPropertyToFormField(fixedProperties[fixedProperty], formField)
    }
}

function updateDocumentFormNProperties(nProperties) {
    for (const nProperty in nProperties) {
        let formField = document.querySelector(`[name="${nProperty}"]`)

        if (formField === null) {
            const fieldGroupsID = `${getEntityNameFromNProperty(nProperty)}-field-groups`
            const fieldGroups = document.querySelector(`#${fieldGroupsID}`)
            addFieldGroup(fieldGroups)
            formField = document.querySelector(`[name="${nProperty}"]`)
        }

        setPropertyToFormField(nProperties[nProperty], formField)
    }
}

function setPropertyToFormField(propertyValue, formField) {
    if (formField.tagName === 'SELECT') {
        const optionTarget = formField.querySelector(`option[value="${propertyValue}"]`)
        optionTarget.selected = true
    } else if (formField.tagName === 'INPUT') {
        formField.value = propertyValue
    }
}

function getEntityNameFromNProperty(nProperty) {
    return nProperty.split('_')[0]
}

function getEntryID() {
    return location.href.split('/')[4]
}

