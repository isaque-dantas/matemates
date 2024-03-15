const btnAddDefinitionField = document.querySelector('button#btn-add-definition-fields')
let firstDefinitionField = document.querySelectorAll('.definition').item(0)
firstDefinitionField.querySelector('button').disabled = true

const removeDefinitionFieldButtons = document.querySelectorAll('button.btn-remove-definition-field')
removeDefinitionFieldButtons.forEach(
    (removeDefinitionFieldButton) => {
        removeDefinitionFieldButton.addEventListener('click', () => {
            removeDefinitionField(removeDefinitionFieldButton.parentNode)
        })
    }
)

btnAddDefinitionField.addEventListener(
    'click',
    () => {
        const newDefinitionField = firstDefinitionField.cloneNode(true)
        const input = newDefinitionField.querySelector('input')
        input.value = ""

        const btnRemoveDefinitionField = newDefinitionField.querySelector(`button.btn-remove-definition-field`)
        btnRemoveDefinitionField.disabled = false
        firstDefinitionField.querySelector('button').disabled = false

        btnRemoveDefinitionField.addEventListener(
            'click',
            () => {
                removeDefinitionField(newDefinitionField)
            }
        )

        firstDefinitionField.parentNode.append(newDefinitionField)
        sortDefinitionsIndexes()
    }
)

function removeDefinitionField(parentElement) {
    firstDefinitionField.parentNode.removeChild(parentElement)
    sortDefinitionsIndexes()

    firstDefinitionField = document.querySelectorAll('.definition').item(0)

    if (firstDefinitionField.parentNode.children.length === 1) {
        firstDefinitionField.querySelector('button').disabled = true
    }
}

function sortDefinitionsIndexes() {
    const definitions = document.querySelectorAll('.definition')
    let index = 1

    definitions.forEach(
        (definition) => {
            updateDefinitionIndex(definition, index)
            index += 1
        }
    )
}

function updateDefinitionIndex(definition, newIndex) {
    updateIDIndex(definition, newIndex)

    const childElementsQueries = ['input', 'select']
    childElementsQueries.forEach(
        (childElementQuery) => {
            const childElement = definition.querySelector(childElementQuery)
            updateIDIndex(childElement, newIndex)
            updateNameIndex(childElement, newIndex)
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
