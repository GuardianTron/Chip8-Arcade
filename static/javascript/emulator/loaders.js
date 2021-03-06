export {loadGame};

async function downloadBinaryFile(fileURL){
    const response = await fetch(fileURL);

    if(response.ok){
        const fileBuffer = await response.arrayBuffer();
        return new Uint8Array(fileBuffer);
    }
    else{
        throw new Error(`Unable to load file ${fileURL}.`);
    }
}
/**
 * Takes the emulator instance and appropriate urls to 
 * load fonts and the game rom.
 * Starts game once all assets are loaded.
 *  
 * @param {Chip8Emulator} emulator 
 * @param {String} chip8FontURL 
 * @param {String} superChipFontURL 
 * @param {String} romURL 
 */

export default function loadGame(emulator,chip8FontURL,superChipFontURL,romURL){
    let promises = [];
    if(!emulator.chip8Font){
        promises.push(async function(){
           emulator.chip8Font = await downloadBinaryFile(chip8FontURL);
        }());
    }
    if(!emulator.superFont){
        promises.push(async function(){
            emulator.superChipFont = await downloadBinaryFile(superChipFontURL);
        }());
    }
    promises.push(async function(){
        let response = await fetch(romURL);
        let romHexString = await response.text();
        emulator.rom = hexStringToBinary(romHexString);

    }());
    Promise.all(promises).then(()=>{emulator.startRom()});
    
}

function hexStringToBinary(hexString){
    //hex strings are double the file size of original binary representation
    let binary = new Uint8Array(Math.ceil(hexString.length/2));
    for(let i = 0; i < binary.length; i++){
        let stringStart = i*2;
        let stringEnd = stringStart+2;
        binary[i] = parseInt(hexString.slice(stringStart,stringEnd),16);
    }
    return binary
}