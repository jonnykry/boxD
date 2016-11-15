
var Board = {
    edges: [],
    canvas : document.createElement("canvas"),
    maxRows: 100,
    maxCols: 100,
    curx : 200,
    cury : 200,
    cursor: new edge(0,0,0,0,'yellow'),
    init : function() {
        this.canvas.width =  window.innerWidth;
        this.canvas.height =  window.innerHeight;
        this.context = this.canvas.getContext("2d");
        document.body.insertBefore(this.canvas, document.body.childNodes[0]);
        this.frameNo = 0;
        this.interval = setInterval(updateBoard, 20);
        },
    stop : function(){
        clearInterval(this.interval);
        },
    clear : function() {
        this.context.clearRect(-camera.x, -camera.y, this.canvas.width, this.canvas.height);
        this.context.fillStyle = '#525252';
        this.context.fillRect(-camera.x, -camera.y, this.canvas.width, this.canvas.height);

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
    // edge = {src: {x: int, y: int}, dst: {x: int, y: int}, owner: String}
    claimEdge: function(p1, p2, owner) {
        // TODO: Proper edge claiming
        // If valid, render and edge and notify server via websockets
        //this.edges.push({src: p1, dst: p2, owner: owner});
    },

    removeEdge: function(src, dst) {
       // this.edges = this.edges.filter(function (edge) {
           // return !(edge.src.x == src.x && edge.src.y == src.y && edge.dst.x == dst.x && edge.dst.y == dst.y);
        }

};

function edge(x,y,x2,y2,color) {
    this.x = x;
    this.y = y;
    this.x2 = x2;
    this.y2 = y2;
    this.color = color
    this.update = function(){
        ctx = Board.context;
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.fillStyle = this.color;
        ctx.fillRect(this.x*100 -4, this.y*100-4,(this.x2-this.x)*100+4,(this.y2-this.y)*100+4);
        ctx.restore();
        }
}

var camera = {
    x: 0,
    y: 0,
    width: 1000,
    height: 600
};
function moveContext(){
    Board.context.setTransform(1, 0, 0, 1, 0, 0); // Reset context
    Board.context.translate((camera.x),(camera.y));
}

function updateBoard(){
    Board.clear();
	Board.cursor.update();
	for(var i=0; i< Board.edges.length;i++){
		Board.edges[i].update();
		}
    if (Board.curx>(Board.canvas.width-100) && camera.x>-3000) {
        camera.x-=10
        moveContext();
        }
    else if (Board.curx<(100)&& camera.x<0) {
        camera.x+=10
        moveContext();
        }
    if (Board.cury>(Board.canvas.height-100) && camera.y>-3000){
        camera.y-=10
        moveContext();
        }
    else if (Board.cury<(100) && camera.y<0) {
        camera.y+=10
        moveContext();
        }
}

Board.canvas.addEventListener('mousedown',function(e) {
    mousex= e.pageX;
    mousey= e.pageY;
    //get closest point
    mousex-=camera.x;
    mousey-=camera.y;
    pointx = Math.round(mousex/100);
    pointy = Math.round(mousey/100);
    pointx2 = pointx;
    pointy2 = pointy;

    //get second point
    if ((mousex%100)>=(mousey%100) && mousex%100 <50 && mousey%100 <50) {
        pointx2 = parseInt(pointx)+1;
        }
    else if ((mousex%100)<(mousey%100) && mousex%100 <50 && mousey%100 <50){
        pointy2 = parseInt(pointy)+1;
        }

    if ((mousex%100)>=(mousey%100) && mousex%100 >=50 && mousey%100 <50){
        pointx2 = parseInt(pointx)-1;
        }
    else if ((mousex%100)<(mousey%100) && mousex%100 >=50 && mousey%100 <50){
        pointy2 = parseInt(pointy)+1;
        }

    if ((mousex%100)>=(mousey%100) && mousex%100 <50 && mousey%100 >=50){
        pointx2 = parseInt(pointx)-1;
        }
    else if ((mousex%100)<(mousey%100) && mousex%100 <50 && mousey%100 >=50) {
        pointy2 = parseInt(pointy)-1;
        }

    if ((mousex%100)<(mousey%100) && mousex%100 >=50 && mousey%100 >=50){
        pointx2 = parseInt(pointx)-1;
        }
    else if ((mousex%100)>=(mousey%100) && mousex%100 >=50 && mousey%100 >=50) {
        pointy2 = parseInt(pointy)-1;
        }
    Board.edges.push(new edge(pointx,pointy,pointx2,pointy2,'blue'));

});

Board.canvas.addEventListener('mousemove',function(e) {
    mousex= e.pageX;
    mousey= e.pageY;
    Board.curx =mousex;
    Board.cury = mousey;

    mousex-=camera.x;
    mousey-=camera.y;
    pointx = Math.round(mousex/100)
    pointy = Math.round(mousey/100)
    pointx2 = pointx;
    pointy2 = pointy;

    //get second point
    if ((mousex%100)>=(mousey%100) && mousex%100 <50 && mousey%100 <50) {
        pointx2 = parseInt(pointx)+1;
        }
    else if ((mousex%100)<(mousey%100) && mousex%100 <50 && mousey%100 <50){
        pointy2 = parseInt(pointy)+1;
        }

    if ((mousex%100)>=(mousey%100) && mousex%100 >=50 && mousey%100 <50){
        pointx2 = parseInt(pointx)-1;
        }
    else if ((mousex%100)<(mousey%100) && mousex%100 >=50 && mousey%100 <50){
        pointy2 = parseInt(pointy)+1;
        }

    if ((mousex%100)>=(mousey%100) && mousex%100 <50 && mousey%100 >=50){
        pointx2 = parseInt(pointx)-1;
        }
    else if ((mousex%100)<(mousey%100) && mousex%100 <50 && mousey%100 >=50) {
        pointy2 = parseInt(pointy)-1;
        }

    if ((mousex%100)<(mousey%100) && mousex%100 >=50 && mousey%100 >=50){
        pointx2 = parseInt(pointx)-1;
        }
    else if ((mousex%100)>=(mousey%100) && mousex%100 >=50 && mousey%100 >=50) {
        pointy2 = parseInt(pointy)-1;
        }
    Board.cursor = new edge(pointx,pointy,pointx2,pointy2,'yellow');
})