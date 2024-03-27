const nFieldGroupsContainers = document.querySelectorAll('.has-n-field-groups')

nFieldGroupsContainers.forEach(
    (nFieldGroupsContainer) => {
        let fieldGroups = nFieldGroupsContainer.querySelector('.field-groups')

        const btnRemoveFirstFieldGroup = getFirstFieldGroup(fieldGroups).querySelector('button.btn-remove-field-group')
        btnRemoveFirstFieldGroup.disabled = true
        btnRemoveFirstFieldGroup.addEventListener(
            'click',
            () => {
                removeFieldGroup(getFirstFieldGroup(fieldGroups), fieldGroups)
            }
        )

        const btnAddFieldGroup = nFieldGroupsContainer.querySelector('.btn-add-field-group')
        btnAddFieldGroup.addEventListener(
            'click',
            () => {
                addFieldGroup(fieldGroups)
            }
        )
    }
)

function addFieldGroup(fieldGroups) {
    const newFieldGroup = getFirstFieldGroup(fieldGroups).cloneNode(true)

    newFieldGroup.querySelectorAll('input').forEach(
        (input) => {
            input.value = ""
        }
    )

    const btnRemoveDefinitionField = newFieldGroup.querySelector(`button.btn-remove-field-group`)
    btnRemoveDefinitionField.disabled = false
    getFirstFieldGroup(fieldGroups).querySelector('button.btn-remove-field-group').disabled = false

    btnRemoveDefinitionField.addEventListener(
        'click',
        () => {
            removeFieldGroup(newFieldGroup, fieldGroups)
        }
    )

    fieldGroups.append(newFieldGroup)
    sortFieldGroupsIndexes()
}

function removeFieldGroup(fieldGroup, fieldGroups) {
    fieldGroups.removeChild(fieldGroup)
    sortFieldGroupsIndexes()

    if (fieldGroups.querySelectorAll('& > *').length === 1) {
        getFirstFieldGroup(fieldGroups).querySelector('button.btn-remove-field-group').disabled = true
    }
}

function getFirstFieldGroup(fieldGroups) {
    return fieldGroups.querySelectorAll('.field-group').item(0)
}

function sortFieldGroupsIndexes() {
    nFieldGroupsContainers.forEach(
        (nFieldGroupsContainer) => {
            const fieldsGroups = nFieldGroupsContainer.querySelectorAll('.field-group')
            let index = 1

            fieldsGroups.forEach(
                (fieldGroup) => {
                    updateFieldGroupIndex(fieldGroup, index)
                    index += 1
                }
            )
        }
    )
}

function updateFieldGroupIndex(fieldGroup, newIndex) {
    updateIDIndex(fieldGroup, newIndex)

    const fieldsQueries = ['input', 'select']
    fieldsQueries.forEach(
        (fieldQuery) => {
            const field = fieldGroup.querySelector(fieldQuery)

            if (field === null) {
                return;
            }

            updateIDIndex(field, newIndex)
            updateNameIndex(field, newIndex)
        }
    )
}

function updateIDIndex(element, newIndex) {
    element.id = getDescriptionFromProperty(element.id) + newIndex.toString()
}

function updateNameIndex(element, newIndex) {
    element.name = getDescriptionFromProperty(element.name) + newIndex.toString()
}

function getDescriptionFromProperty(property) {
    const propertyMatch = property.match(/^[a-zA-z\-_]+/)

    if (propertyMatch) {
        return propertyMatch[0]
    }
}
