import ipywidgets as wi
from PIL import Image
from io import BytesIO
from base64 import b64encode, b64decode
from uuid import uuid4

class spylus:
    @staticmethod
    def ID_canvas(ID=None, width=300, height=100):
        if not ID:
            ID = str(uuid4())[:8]
        canvas = wi.HTML(f"<canvas id={ID} width={width} height={height} style=background:white;></canvas>")
        return ID, canvas

    @staticmethod
    def ID_multicanvas(N=3, ID=None, width=512, height=512):
        if not ID:
            ID = str(uuid4())[:8]
        canvas = wi.HTML('\n'.join(
        f'<canvas id={ID}{i} width={width} height={height} style="position:absolute;"></canvas>'
        for i in range(N)) +
        f'<canvas width={width} height={height} style="background:white;"></canvas>')
        return ID, canvas

    @staticmethod
    def encode(image):
        buffer = BytesIO()
        image.save(buffer, format="png")
        text = b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{text}"

    @staticmethod
    def decode(text):
        return Image.open(BytesIO(b64decode(text.split(",")[-1])))

spylus.js = """
class Canvas{
    X = null;
    Y = null;
    drawing = false;
    constructor({canvas}){
        this.canvas = canvas;
        this.ctx = canvas.getContext("2d", {desynchronized: true});
        canvas.style.touchAction = 'none';
        canvas.addEventListener("pointerup", (e)=>{this.up(e)});
        canvas.addEventListener("pointerleave", (e)=>{this.up(e)});
        canvas.addEventListener("pointerdown", (e)=>{this.down(e)});
        canvas.addEventListener("pointermove", (e)=>{this.move(e)});
    }
    move(e){
        if(this.drawing){
            this.ctx.beginPath();
            this.ctx.moveTo(this.X, this.Y);
            this.ctx.lineTo(e.offsetX, e.offsetY);
            this.ctx.lineCap = "round";
            this.ctx.lineWidth = this.lineWidth(e);
            this.ctx.strokeStyle = this.strokeStyle(e);
            this.ctx.stroke();
            this.X = e.offsetX;
            this.Y = e.offsetY;
        }
    }
    down(e){
        this.X = e.offsetX;
        this.Y = e.offsetY;
        this.drawing = true;
    }
    up(e){
        this.X = null;
        this.Y = null;
        this.drawing = false;
    }
    strokeStyle(e){
        return "black";
    }
    lineWidth(e){
        if(e.pointerType == "pen"){
            return 5*e.pressure;
        }else{
            return 5;
        }
    }
}

let Save = Canvas => class extends Canvas{
    constructor({save_input}){
        super(arguments[0]);
        this.save_input = save_input;
    }
    save(){
        this.save_input.value = this.canvas.toDataURL();
        let event = new Event('change', {bubbles: true});
        this.save_input.dispatchEvent(event);
    }
    up(e){
        super.up(e);
        this.save();
    }
}

let Load = Canvas => class extends Canvas{
    constructor({}){super(arguments[0]);}
    load(text){
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        let img = new Image();
        img.onload = () => {
            this.ctx.drawImage(img,0,0);
            if(this.save){ this.save(); }
        };
        img.src = text;
    }
}

let Paste = Canvas => class extends Canvas{
    constructor({paste_button}){
        super(arguments[0]);
        this.paste_button = paste_button;
        paste_button.addEventListener("click", (e)=>{this.paste(e)});
    }
    paste(e){
        this.read_clipboard(b=>{
            let img = new Image();
            img.onload = () => {
                this.ctx.drawImage(img,0,0);
                if(this.save){ this.save(); }
            };
            img.src = b;
        })
    }
    read_clipboard(f){
        navigator.clipboard.read()
        .then(clipboardItems => {
            const clipboardItem = clipboardItems[0];
            let type = clipboardItem.types[0]
            if (type == "image/png"){
                clipboardItem.getType(type)
                .then(blob => {
                    var reader = new FileReader();
                    reader.onload = function(event){
                        f(event.target.result)
                    };
                    var source = reader.readAsDataURL(blob);
                })
                .catch(err => {
                    console.error('blob error', err);
                });
            }
            else{
                console.error("unknown type");
            }
        })
        .catch(err => {
            console.error('permission denied', err);
        });
    }
}

let PasteCenter = Canvas => class extends Paste(Canvas){
    paste(e){
        this.read_clipboard(b=>{
            let img = new Image();
            img.onload = () => {
                let cw = this.ctx.canvas.clientWidth;
                let ch = this.ctx.canvas.clientHeight;
                let iw = img.width;
                let ih = img.height;
                let scale = Math.min(cw/iw, ch/ih);
                let dw = scale*iw;
                let dh = scale*ih;
                this.ctx.drawImage(img, (cw-dw)/2, (ch-dh)/2, dw, dh);
                if(this.save){ this.save(); }
            };
            img.src = b;
        })
    }
}

let _White = Canvas => class extends Canvas{
    constructor({}){ super(arguments[0]); }
    white(){
        let tmp = document.createElement("canvas");
        tmp.width = this.canvas.width;
        tmp.height = this.canvas.height;
        let tmpctx = tmp.getContext("2d");
        tmpctx.fillStyle = "white";
        tmpctx.fillRect(0,0,tmp.width,tmp.height);
        tmpctx.drawImage(this.canvas,0,0);
        return tmp.toDataURL();
    }
}

let White = Canvas => class extends _White(Canvas){
    constructor({}){ super(arguments[0]); }
    save(){
        this.save_input.value = this.white();
        let event = new Event('change', {bubbles: true});
        this.save_input.dispatchEvent(event);
    }
}

let Copy = Canvas => class extends _White(Canvas){
    constructor({copy_button}){
        super(arguments[0]);
        this.copy_button = copy_button;
        copy_button.addEventListener("click", (e)=>{this.copy(e)});
    }
    copy(e){
        dataURLtoBlob(this.white(), (blob)=>{
            navigator.clipboard.write([
                new ClipboardItem({[blob.type]: blob})
            ])
        });
    }
}

let Color = Canvas => class extends Canvas{
    constructor({color_input}){
        super(arguments[0]);
        this.color_input = color_input;
    }
    strokeStyle(e){
        return this.color_input.value;
    }
}

let Width = Canvas => class extends Canvas{
    constructor({width_select}){
        super(arguments[0]);
        this.width_select = width_select;
    }
    lineWidth(e){
        if(e.pointerType == "pen"){
            return this.width_select.value*e.pressure;
        }else{
            return this.width_select.value;
        }
    }
}

let Clear = Canvas => class extends Canvas{
    constructor({clear_button}){
        super(arguments[0]);
        this.clear_button = clear_button;
        clear_button.addEventListener("click", (e)=>{this.clear(e)});
    }
    clear(e){
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }
}

//TODO
let RedoUndo = Canvas => class extends Canvas{
    history = [];
    constructor({redo_button, undo_button}){
        super(arguments[0]);
        this.redo_button = redo_button;
        this.undo_button = undo_button;
        redo_button.addEventListener("click", (e)=>{this.redo(e)});
        undo_button.addEventListener("click", (e)=>{this.undo(e)});
    }
    save(){
        this.history.push(this.canvas.toDataURL());
        this.save_input.value = this.history[-1];
        let event = new Event('change', {bubbles: true});
        this.save_input.dispatchEvent(event);
    }
}

function dataURLtoBlob(dataUrl, callback){
    var req = new XMLHttpRequest;
    req.open( 'GET', dataUrl );
    req.responseType = 'blob';
    req.onload = function fileLoaded(e){
        callback(this.response);
    };
    req.send();
}

class Selector{
    constructor({apps, selector_select}){
        this.apps = apps;
        this.selector_select = selector_select;
        selector_select.addEventListener('change', (e)=>{this.select(e)});
        for(let i=0; i<this.apps.length; i++){
            this.apps[i].canvas.style.opacity = 0.9999999;
        }
        this.select();
    }
    select(e){
        for(let i=0; i<this.apps.length; i++){
            if(i == this.selector_select.value){
                this.apps[i].canvas.style.zIndex = 1;
            }else{
                this.apps[i].canvas.style.zIndex = 0;
            }
        }
    }
}

let find_element = function(xpath, i){
    let results = document.evaluate(
        xpath,
        document,
        null,
        XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,
        null
    ).snapshotItem(i);
    return results;
};

let elem = function(id, name, i){
    return find_element(`//*[@id="${id}"]/../../..//${name}`, i);
};

let mix = function(...mixins){
    return mixins.reduceRight((x,f)=>f(x), Canvas);
};
"""
