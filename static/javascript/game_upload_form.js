window.addEventListener('load', event => {
    const keyComplete = new KeyCodeCompletion('key_code_entry', 'key_code');
    const enableCompletionCheckbox = document.getElementById('key_code_autocomplete');
    enableCompletionCheckbox.addEventListener('change',event =>{
        if (event.target.checked) keyComplete.enableCompletion();
        else keyComplete.disableCompletion();
    });
    //enable by default
    keyComplete.enableCompletion();


    //add clear buttons
    document.querySelectorAll('.key_code_entry').forEach(node => {
        const clearButton = document.createElement('button', { class: 'clear_button' });
        clearButton.appendChild(document.createTextNode('Clear'));
        clearButton.addEventListener('click', event => {
            event.preventDefault();
            const keyCodeInput = node.querySelector('[name$=key_code]');
            keyCodeInput.value = '';
        });
        node.appendChild(clearButton);
    });

    //add button to add more fields
    const adderButton = document.createElement('button');
    adderButton.appendChild(document.createTextNode('Add Entry'));
    document.getElementById('key_code_fields').appendChild(adderButton);
    adderButton.addEventListener('click', (event) => {
        //prevent form submttions
        event.preventDefault();
        add_input_field('.key_code_entry');
    });
});
function newNameString(name, separator, newNumber) {
    let parts = name.split(separator);
    //replace number in middle with new number
    parts[1] = newNumber;
    return parts.join(separator);
}

function add_input_field(query) {

    const inputContainer = document.querySelector(query);
    const newFields = inputContainer.cloneNode(true);
    //determine how many fields exist
    const newFieldNumber = inputContainer.parentNode.querySelectorAll(query).length;
    for (let i = 0; i < newFields.children.length; i++) {
        let element = newFields.children[i];
        if (element.hasAttribute('name')) {
            element.name = newNameString(element.name, '-', newFieldNumber);
            //remove any user added data
            element.value = '';
        }
        if (element.hasAttribute('id')) {
            element.id = newNameString(element.id, '-', newFieldNumber);
        }
        if (element.hasAttribute('for')) {
            console.log(element.attributes);
            element.setAttribute('for', newNameString(element.getAttribute('for'), '-', newFieldNumber));
        }
    }
    //add the new element to top
    inputContainer.parentNode.insertBefore(newFields, inputContainer);
    //return the new nodes for futher processing
    return newFields;
}





/**@TODO Consider adding checkbox to allow disabling of javascript keycode entry */

class KeyCodeCompletion {
    constructor(configLineClassName, inputFieldNameEndsWith) {

        const firstLine = document.getElementsByClassName(configLineClassName).item(0);
        if (!firstLine || !firstLine.parentNode) throw new Error(`Unable to locate code configuration elements with class ${configLineClassName}`);
        this.formContainer = firstLine.parentNode;
        this.inputFieldNameEndsWith = inputFieldNameEndsWith;
    }

    enableCompletion() {
        this.formContainer.addEventListener('keydown', this.handleKeyDown);
        this.formContainer.addEventListener('keyup', this.handleKeyUp);
    }

    disableCompletion() {
        this.formContainer.removeEventListener('keydown', this.handleKeyDown);
        this.formContainer.removeEventListener('keyup', this.handleKeyUp);
    }


    /**
     * Suppress regular output for keydown events
     */
    handleKeyDown = event => {
        if (event.target.name.substr(-this.inputFieldNameEndsWith.length) == this.inputFieldNameEndsWith) {
            event.preventDefault();
        }
    }

    /**
     * Fill input with javascript keycode based on key pressed
     * @param  event 
     */
    handleKeyUp = event => {
        if (event.target.name.substr(-this.inputFieldNameEndsWith.length) == this.inputFieldNameEndsWith) {
            event.target.value = event.which;
        }
    }







}
