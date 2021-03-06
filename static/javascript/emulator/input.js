import { Chip8 } from "./chip8.js";
export class KeyboardInput{
    
    constructor(chip8){
        this.chip8 = chip8;
        this.physicalToChip8 = new Map();
        this.chip8toPhysical = new Map();
    }

    mapKey(keycode, chip8Key){
        //remove old key code
        if(this.chip8toPhysical.has(chip8Key)){
            let oldKeycode = this.chip8toPhysical.get(chip8Key);
            this.physicalToChip8.delete(oldKeycode);
        }

        this.chip8toPhysical.set(chip8Key, keycode);
        this.physicalToChip8.set(keycode,chip8Key);
    }

    onkeydown = (event) => {
        if(this.physicalToChip8.has(event.keyCode)){
            let chip8Key = this.physicalToChip8.get(event.keyCode);
            this.chip8.setKey(chip8Key);
        }
 
        
    }

    onkeyup = (event) => {
        if(this.physicalToChip8.has(event.keyCode)){
            let chip8Key = this.physicalToChip8.get(event.keyCode);
            this.chip8.unsetKey(chip8Key);
        }
        
    }


}