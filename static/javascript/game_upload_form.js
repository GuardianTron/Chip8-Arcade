window.addEventListener('load', event => {
    //set keycode from button press directly
    const keyCodeInputList = document.querySelector(".key_code_entry").parentNode;
    const keyCodeEndsWith = "key_code";
    //prevent characters from displaying on the field during typing
    keyCodeInputList.addEventListener('keydown', event => {
        //name ends with key_code
        if (event.target.name.substr(-keyCodeEndsWith.length) == keyCodeEndsWith) {
            event.preventDefault();
        }
    });

    keyCodeInputList.addEventListener('keyup', event => {
        //name ends with key_code
        if (event.target.name.substr(-keyCodeEndsWith.length) == keyCodeEndsWith) {
            event.target.value = event.which;
        }

    });

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


