import {Chip8Emulator} from "./emulator/chip8emulator.js";
import {loadGame} from "./emulator/loaders.js";

const canvas = document.getElementById('emulator_screen');
const emulator = new Chip8Emulator(canvas);
//get the api url from the calling script tag
const gameUrl = document.querySelector("script[data-gameurl]").dataset.gameurl;
fetch(gameUrl).then(
    async function(response){
    if(response.ok){
        const config = await response.json();
        if(config.hasOwnProperty('error')){
            throw new Error('Game could not be found on the server.');
        }
        const keys = config['key_config'];
        emulator.loadKeyMap(keys);
        return loadGame(emulator,config['chip8_font'],config['super_chip_font'],config['rom']);
    }
    else{
        throw new Error(`Unable to download configuration. Response Code: ${response.status}`)
    }
}).catch(error => alert(error));