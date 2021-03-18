window.addEventListener('load', event => {
    //set up key code detection and clear buttons
    const keyComplete = new KeyCodeCompletion('key_code_entry', 'key_code');
    const clearButtons = new ClearButtonManager('key_code_entry','[name$=key_code]');
    const enableCompletionCheckbox = document.getElementById('key_code_autocomplete');
    enableCompletionCheckbox.addEventListener('change',event =>{
        if (event.target.checked){
             keyComplete.enableCompletion();
             clearButtons.addClearButtons();
        }
        else{
            clearButtons.removeClearButtons();
            keyComplete.disableCompletion();
        }
    });

    //enable by default
    keyComplete.enableCompletion();
    clearButtons.addClearButtons();

    //set up clear buttons for 

    //add clear buttons
    /*
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
    */

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





/**
 * Class to handle autocomplete feature for keycodes.
 * Had event handlers for keycode completion as well
 * as methods to enable and disable keycode completion.
 */

class KeyCodeCompletion {
    /**
     * 
     * @param {String} configLineClassName -- Class name of elements containing fields for single key code configuration
     * @param {String} inputFieldNameEndsWith -- The end portion of the individual key code field name.  Used in conjunction with Flask-WTF FieldList 
     */
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

class ClearButtonManager{
    /**
     * 
     * @param {String} parentNodeClass Class name of the field's container
     * @param {String} inputFieldQuery CSS Query for the input field to be cleared
     * @param {Object} Options buttonElementType - Type of element to be created, buttonClass - CSS class for button, label - the label string
     */
    constructor(parentNodeClass,inputFieldQuery,{buttonElementType='button',buttonClass = 'clear_button',label='clear'} = {}){
        this.parentNodeClass = parentNodeClass;
        this.inputFieldQuery = inputFieldQuery;
        this.buttonElementType = buttonElementType;
        this.buttonClass = buttonClass;
        this.label = label;
    }

    addClearButtons(){
        const parentNodes = this._getParentNodes();
        parentNodes.forEach( node =>{
            const clearButton = document.createElement(this.buttonElementType);
            clearButton.className = this.buttonClass;
            clearButton.appendChild(document.createTextNode(this.label));
            clearButton.addEventListener('click',this.handleClear);
            node.appendChild(clearButton);
        });
    }

    removeClearButtons(){
        const parentNodes = this._getParentNodes();
        parentNodes.forEach( node =>{
            /*
             * Buttons are removed from the container nodes instead of 
             * simply using document.getElementsByClassName to prevent other 
             * buttons from being removed from unrelated containers should they 
             * share the other class name.
             */
            const clearButton = node.getElementsByClassName(this.buttonClass)[0];
            if(clearButton){
                node.removeChild(clearButton);
            }
        

        
        });
    }

    handleClear = event =>{
        event.preventDefault()
        try{
            document.querySelector(this.inputFieldQuery).value = ''
        }
        catch(error){
            throw new Error(`Field matching query ${this.inputFieldQuery} not found by clear function.`);
        }
    }

    _getParentNodes(){
        return document.querySelectorAll(`.${this.parentNodeClass}`);
    }
}