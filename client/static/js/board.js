
var Board = {
    edges: [],
    canvas : document.createElement("canvas"),
    maxRows: 100,
    maxCols: 100,
    curx : 200,
    cury : 200,
    cursor: new Edge(0,0,0,0,'yellow'),
    camera: {
        x: 0,
        y: 0,
        width: 1000,
        height: 600
    },

    init: function() {
        this.canvas.width =  window.innerWidth;
        this.canvas.height =  window.innerHeight;
        this.context = this.canvas.getContext("2d");
        document.body.insertBefore(this.canvas, document.body.childNodes[0]);
        this.frameNo = 0;
        this.interval = setInterval(updateBoard, 20);

        return this;
    },

    stop: function() {
        clearInterval(this.interval);
    },

    clear: function() {
        this.context.clearRect(-this.camera.x, -this.camera.y, this.canvas.width, this.canvas.height);
        this.context.fillStyle = '#525252';
        this.context.fillRect(-this.camera.x, -this.camera.y, this.canvas.width, this.canvas.height);

        for(var i=0; i<this.maxRows; i++){
            this.context.strokeStyle= '#b2b2b2';
            this.context.moveTo(i*100+100,0);
            this.context.lineTo(i*100+100,this.maxRows *100);
            this.context.stroke();
            this.context.moveTo(0,i*100+100);
            this.context.lineTo(this.maxRows *100,i*100+100);
            this.context.stroke();
        }

        for(var c=0; c<this.maxCols;c++){
            for(var r=0; r<this.maxRows;r++){
                this.context.strokeStyle= 'black';
                this.context.beginPath();
                this.context.arc(r*100+100,c*100+100,10,0,2*Math.PI);
                this.context.stroke();
            }
        }
     },

    setCursor: function(x1, y1, x2, y2, color) {
        this.cursor = new Edge(x1, y1, x2, y2, color);
    },

    moveContext: function (){
        this.context.setTransform(1, 0, 0, 1, 0, 0); // Reset context
        this.context.translate((this.camera.x),(this.camera.y));
    },

    // edge = {src: {x: int, y: int}, dst: {x: int, y: int}, owner: String}
    claimEdge: function(x1, y1, x2, y2, color) {
        // TODO: Proper edge claiming
        // If valid, render and edge and notify server via websockets
        this.edges.push(new Edge(x1, y1, x2, y2, color));
    }
};

function updateBoard() {
    Board.clear();
    Board.cursor.update();

    for(var i=0; i< Board.edges.length;i++){
        Board.edges[i].update();
    }

    if (Board.curx>(Board.canvas.width-100) && Board.camera.x>-3000) {
        Board.camera.x-=10;
        Board.moveContext();
    } else if (Board.curx<(100) && Board.camera.x<0) {
        Board.camera.x+=10;
        Board.moveContext();
    }

    if (Board.cury>(Board.canvas.height-100) && Board.camera.y>-3000){
        Board.camera.y-=10;
        Board.moveContext();
    } else if (this.cury<(100) && this.camera.y<0) {
        this.camera.y+=10;
        Board.moveContext();
    }
}

function Edge(x, y, x2, y2, color) {
    this.x = x;
    this.y = y;
    this.x2 = x2;
    this.y2 = y2;
    this.color = color;
    this.update = function() {
        var ctx = Board.context;
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.fillStyle = this.color;
        ctx.fillRect(this.x*100 -4, this.y*100-4, (this.x2-this.x)*100+4, (this.y2-this.y)*100+4);
        ctx.restore();
    }
}
