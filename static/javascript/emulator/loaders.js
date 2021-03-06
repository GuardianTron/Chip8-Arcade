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
        emulator.rom = await downloadBinaryFile(romURL);
    }());
    Promise.all(promises).then(()=>{emulator.startRom()});
    
}