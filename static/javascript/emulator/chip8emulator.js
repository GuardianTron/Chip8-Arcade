import { Chip8 } from "./chip8.js"
import { CanvasDisplay } from "./display.js"
import {KeyboardInput} from "./input.js"
import {Beep} from "./sound.js";

export {Chip8Emulator as default}

export class Chip8Emulator{

    constructor(canvas){

        this.rom = null;
        this.cpu = new Chip8();
        this.keyboardMapper = new KeyboardInput(this.cpu);
        this.display = new CanvasDisplay(canvas,this.cpu.vram);
        this.beep = new Beep();

        //resume sound when user presses a button for audio compliance

       
        window.addEventListener("keyup",this.beep.resume);
        window.addEventListener("keydown",this.beep.resume);

        //set up key mapper
        window.addEventListener("keydown",this.keyboardMapper.onkeydown);
        
        window.addEventListener("keyup",this.keyboardMapper.onkeyup);
        
        this.cpu.clockSpeed = 1000;
        
        this.cpu.sound = this.beep;

        //start the screen
        window.requestAnimationFrame(this.display.drawFrame);



    }

    get clockSpeed(){
        return this.cpu.clockSpeed;
    }

    set clockSpeed(speed){
        this.cpu.clockSpeed = speed;
    }

    get chip8Font(){
        return this.cpu.chip8Font;
    }

    set chip8Font(fontBuffer){
        this.cpu.loadChip8Font(fontBuffer);
    }

    get superChipFont(){
        return this.cpu.superChipFont;
    }

    set superChipFont(fontBuffer){
        this.cpu.loadSuperFont(fontBuffer);
    }



    

    /**
     * Load the keymap from a parsed json object
     * Format
     * Chip 8 keys can be hexidecimal strings.
     * Modern Key Codes are integers refering to modern keyboard mappings.
     * 
     * @param {Object} keyMap A javascript object mapping chip 8 hex keys to key codes 
     */
    loadKeyMap(keyMap){
        Object.keys(keyMap).forEach((chip8Key)=>{
            const keyCode = keyMap[chip8Key];
            const chip8Parsed = parseInt(chip8Key,16);
            this.keyboardMapper.mapKey(keyCode,chip8Parsed);
        });
    }

    startRom(){
        this.cpu.loadRom(this.rom);
        this.cpu.execute();


    }

    addCallback(func){
        this.cpu.addCallback(func);
    }

    removeCallback(func){
        this.cpu.removeCallback(func);
    }
    
}
