var scale = 100;
var Board = {
    edges: [],
    squares: [],
    canvas : document.createElement("canvas"),
    maxRows:40,
    maxCols:40,
    curX : 200,
    curY : 200,
    lastFrameTimeMs : 0,
    maxFPS : 60,
    move_timer: 0,
    next_move: 10,
    cooloff_timer: 0,
    last_second:0,
    cooloff_end: 5,
    minimap_x : 0,
    minimap_y : 0,
    cursor: new Edge(0, 0, 0, 0, 'yellow'),

    camera: {
        x: 0,
        y: 0,
        width:1000,
        height: 600
    },

    init: function() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
        this.context = this.canvas.getContext("2d");
        document.body.insertBefore(this.canvas, document.body.childNodes[0]);
        this.frameNo = 0;
        this.interval = requestAnimationFrame(updateBoard);
        this.camera.y = - (Math.random()*10000)%3000;
        this.camera.x = -(Math.random()*10000)%3000;
        this.moveContext();
        return this;
    },

    stop: function() {
        clearInterval(this.interval);
    },

    clear: function() {
        this.context.clearRect(-this.camera.x, -this.camera.y, this.canvas.width, this.canvas.height);
        this.context.fillStyle = '#525252';
        this.context.fillRect(-this.camera.x, -this.camera.y, this.canvas.width, this.canvas.height);

        for (var i = 0; i < this.maxRows; i++) {
            this.context.strokeStyle= '#b2b2b2';
            this.context.moveTo(i * scale + scale, scale);
            this.context.lineTo(i * scale + scale, this.maxRows * scale);
            this.context.stroke();
            this.context.moveTo(scale, i * scale + scale);
            this.context.lineTo(this.maxRows * scale, i * scale + scale);
            this.context.stroke();
        }

    },

    setCursor: function(x1, y1, x2, y2, color) {
        this.cursor = new Edge(x1, y1, x2, y2, color);
    },

    moveContext: function () {
        this.context.setTransform(1, 0, 0, 1, 0, 0); // Reset context
        this.context.translate((this.camera.x),(this.camera.y));
    },

    claimEdge: function(x1, y1, x2, y2, color) {
        // TODO: Proper edge claiming
        // If valid, render and edge and notify server via websockets
        this.edges.push(new Edge(x1, y1, x2, y2, color));
    },
    claimSquare: function(x1, y1, color) {
            this.squares.push(new Square(x1, y1,color));
        },
    next_move_timer: function(current) {
        ctx = this.context;
        ctx.beginPath();
        ctx.save();

        if (current < 0.75) {
            ctx.strokeStyle = '#99CC33';
        }
        else {
            ctx.strokeStyle = '#ff0000';
        }

        ctx.lineCap = 'square';
        ctx.lineWidth = 10.0;
        ctx.arc(120 -this.camera.x, 120-this.camera.y, 70, -(Math.PI / 2), (( Math.PI * 2)) , false);
        ctx.stroke();
        ctx.restore();

        if (current != 0){
            ctx.beginPath();
            ctx.save();
            ctx.strokeStyle = '#ffffff';
            ctx.lineCap = 'square';
            ctx.lineWidth = 10.0;
            ctx.arc(120 -this.camera.x, 120-this.camera.y, 70, -(Math.PI / 2), (( Math.PI * 2) * current) - Math.PI / 2, false);
            ctx.stroke();
            ctx.restore();
        }

    },
    cool_off_timer: function(current) {
        ctx = this.context;
        ctx.beginPath();
        ctx.save();
        ctx.strokeStyle = '#ff0000';
        ctx.lineWidth = 75.0;
        ctx.arc(120 -this.camera.x, 120-this.camera.y, 35, -(Math.PI / 2), (( Math.PI * 2)) - Math.PI / 2, false);
        ctx.stroke();
        ctx.restore();

        ctx.beginPath();
        ctx.save();
        ctx.strokeStyle = '#0066ff';
        ctx.lineWidth = 75.0;
        ctx.arc(120 -this.camera.x, 120-this.camera.y, 35, -(Math.PI / 2), (( Math.PI * 2) * current) - Math.PI / 2, false);
        ctx.stroke();
        ctx.restore();
    },
    mini_map_update: function() {
        this.minimap_x = -this.camera.x+this.canvas.width - 200;
        this.minimap_y = -this.camera.y+this.canvas.height - 200;
        this.context.fillStyle = 'black';
        this.context.fillRect(this.minimap_x - 5,this.minimap_y -5 , 210 , 210);
        this.context.fillStyle = '#525252';
        this.context.fillRect(this.minimap_x,this.minimap_y , 200 , 200);
        this.context.beginPath();
        this.context.save();
        this.context.strokeStyle = 'black';
        this.context.rect(this.minimap_x + ( -this.camera.x /20),this.minimap_y +( -this.camera.y /20) , this.canvas.width / 20, this.canvas.height /20);
        this.context.stroke();
        this.context.restore();
    },
    getPointsByCursor: function(mouseX, mouseY) {
            var result = {};

            // Get closest point
            var pointX = Math.round(mouseX /scale);
            var pointY = Math.round(mouseY /scale);

            result.pointX = pointX;
            result.pointY = pointY;
            result.pointX2 = pointX;
            result.pointY2 = pointY;

            //get second point
            if ((mouseX %scale) >= (mouseY %scale) && mouseX %scale < 50 && mouseY %scale < 50) {
                result.pointX2 = parseInt(pointX) + 1;
            }
            else if ((mouseX %scale) < (mouseY %scale) && mouseX %scale < 50 && mouseY %scale < 50) {
                result.pointY2 = parseInt(pointY) + 1;
            }

            if ((mouseX %scale) >= (mouseY %scale) && mouseX %scale >= 50 && mouseY %scale < 50) {
                result.pointX2 = parseInt(pointX) - 1;
            }
            else if ((mouseX %scale) < (mouseY %scale) && mouseX %scale >= 50 && mouseY %scale <50) {
                result.pointY2 = parseInt(pointY) + 1;
            }

            if ((mouseX %scale) >= (mouseY %scale) && mouseX %scale < 50 && mouseY %scale >= 50) {
                result.pointX2 = parseInt(pointX) - 1;
            }
            else if ((mouseX %scale) < (mouseY %scale) && mouseX %scale <50 && mouseY %scale >= 50) {
                result.pointY2 = parseInt(pointY) - 1;
            }

            if ((mouseX %scale) < (mouseY %scale) && mouseX %scale >= 50 && mouseY %scale >= 50) {
                result.pointX2 = parseInt(pointX) - 1;
            }
            else if ((mouseX %scale) >= (mouseY %scale) && mouseX %scale >= 50 && mouseY %scale >= 50) {
                result.pointY2 = parseInt(pointY) - 1;
            }

            return result;
        }

};

function updateBoard(timestamp) {
    if (timestamp < Board.lastFrameTimeMs + (1000 / Board.maxFPS)) {
            requestAnimationFrame(updateBoard);
            return;
    }

    Board.lastFrameTimeMs = timestamp;
    Board.clear();
    Board.mini_map_update();
    for (var i = 0; i < Board.edges.length; i++) {
        Board.edges[i].update();
        Board.edges[i].mini_map_update();
    }
    for (var i = 0; i < Board.squares.length; i++) {
        Board.squares[i].update();
        Board.squares[i].mini_map_update();
    }
    Board.cursor.update();
    if (Board.curX > (Board.canvas.width -100) && Board.camera.x > -3000) {
        Board.camera.x -= 10;
        Board.moveContext();
    } else if (Board.curX < 100 && Board.camera.x < 0) {
        Board.camera.x += 10;
        Board.moveContext();
    }

    if (Board.curY>(Board.canvas.height -100) && Board.camera.y > -3500){
        Board.camera.y -= 10;
        Board.moveContext();
    } else if (Board.curY < 100 && Board.camera.y < 0) {
        Board.camera.y += 10;
        Board.moveContext();
    }
    var d = new Date();
    var s = d.getSeconds();
    Board.cool_off_timer((Board.cooloff_timer )/5);
    Board.next_move_timer((Board.move_timer )/10);
    if(Board.last_second != s){
        Board.cooloff_timer+= 1;

        if( Board.cooloff_timer >= Board.cooloff_end){
            Board.move_timer+=1;

            if (Board.move_timer >=Board.next_move){
                Board.cooloff_timer = 0 ;
                Board.move_timer =  0;
                Board.next_move = 10;
                Board.cooloff_end= 5;
            }
         }
        Board.last_second=s;
        if (Board.last_second ==60){
            Board.last_second =0;
        }
    }





    requestAnimationFrame(updateBoard);
}

function Edge(x, y, x2, y2, color) {
    this.x = x;
    this.y = y;
    this.x2 = x2;
    this.y2 = y2;
    this.color = color;
    if (this.x > this.x2){
        var temp = this.x;
        this.x = this.x2;
        this.x2 = temp;
    }
    if (this.y > this.y2){
        var temp = this.y;
        this.y = this.y2;
        this.y2 = temp;
    }
    this.update = function() {
        var ctx = Board.context;
        ctx.save();
        ctx.fillStyle = this.color;
        ctx.fillRect((this.x *scale) - 2, (this.y *scale) - 2, ((this.x2 - this.x) *scale) + 4, ((this.y2 - this.y) *scale) + 4);
        ctx.restore();
    }
    this.mini_map_update = function(){
        var hor = true;
        if(this.x == this.x2){
            hor = false;
        }
        var ctx = Board.context;
        if (hor) {
            ctx.save();
            ctx.translate(Board.minimap_x +this.x, Board.minimap_y +this.y);
            ctx.fillStyle = this.color;
            ctx.fillRect( 5 * this.x ,  5 *this.y , 5 , 1);
            ctx.restore();
        }
        else {
            ctx.save();
            ctx.translate(Board.minimap_x +this.x, Board.minimap_y +this.y);
            ctx.fillStyle = this.color;
            ctx.fillRect( 5 * this.x ,  5 *this.y , 1, 5);
            ctx.restore();

        }

    }

}

function Square(x , y , color) {
    this.x = x;
    this.y = y;
    this.color = color;
    this.update = function() {
        var ctx = Board.context;
        ctx.save();
        ctx.fillStyle = this.color;
        ctx.fillRect((this.x *scale) , (this.y *scale) , scale, scale);
        ctx.restore();
    }
    this.mini_map_update = function(){
        ctx.save();
        ctx.translate(Board.minimap_x , Board.minimap_y );
        ctx.fillStyle = this.color;
        ctx.fillRect( 5 * this.x ,  5 *this.y , 6 , 6);
        ctx.restore();
    }
}