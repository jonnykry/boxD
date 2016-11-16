
$(document).ready( function() {
    $('#entryModal').modal({show: true});

    if (!('WebSocket' in window)) {
        alert('Your browser does not support web sockets');
    } else {
        playerResult = setup();

        var player = Player.init(playerResult.name, playerResult.color);
        var game = Game.init(player);
        var board = game.board;

        function getParameterByName(name, url) {
            if (!url) {
                url = window.location.href;
            }

            name = name.replace(/[\[\]]/g, '\\$&');
            var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
                    results = regex.exec(url);
            if (!results) return null;
            if (!results[2]) return '';
            return decodeURIComponent(results[2].replace(/\+/g, ' '));
        }

        function setup() {
            var host;
            if (getParameterByName('local') == 'true') {
                host = 'ws://localhost:5000/ws';
            } else {
                host = 'wss://boxd.herokuapp.com/ws';
            }

            var socket = new WebSocket(host);
            //console.log("socket status: " + socket.readyState);

            var $nickname = $('#nickname');
            var $startGame = $('#startGame');

            $nickname.focus();

            // event handlers for UI
            $startGame.on('click',function(){
                var text = $nickname.val();

                if (text === null || text === 'undefined') text = '';

                var request = {
                   type:  'JOIN_GAME',
                   data: {
                        name:  text
                   }
                };

                socket.send(JSON.stringify(request));
                $nickname.val('');
            });

            $nickname.keypress(function(evt) {
                if (evt.which == 13) { // ENTER
                    $startGame.click();
                }
            });

            var $testText = $('#testText');
            var $submit = $('#submit');

            $submit.on('click',function(){
                var text = $testText.val();

                if (text === null || text === 'undefined') text = '';

                socket.send(text);
                $testText.val('');
            });

            // event handlers for websocket
            if (socket) {
                socket.onopen = function(){};

                socket.onmessage = function(msg){
                    showServerResponse(msg.data);
                };

                socket.onclose = function(){
                    showServerResponse('The connection has been closed.');
                }
            } else {
                console.log('invalid socket');
            }

            function showServerResponse(txt){
                var p = document.createElement('p');
                p.innerHTML = txt;
                document.getElementById('output').appendChild(p);
            }

            return {
                name: 'TempName',
                color: 'white'
            }
        }

        board.canvas.addEventListener('mousedown', function(e) {
            var mousex = e.pageX;
            var mousey = e.pageY;
            //get closest point
            mousex -= board.camera.x;
            mousey -= board.camera.y;
            var pointx = Math.round(mousex/100);
            var pointy = Math.round(mousey/100);
            var pointx2 = pointx;
            var pointy2 = pointy;

            //get second point
            if ((mousex%100)>=(mousey%100) && mousex %100 <50 && mousey%100 <50) {
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

            board.claimEdge(pointx, pointy, pointx2, pointy2, player.color);
        });

        board.canvas.addEventListener('mousemove', function(e) {
            var mousex = e.pageX;
            var mousey = e.pageY;
            board.curx = mousex;
            board.cury = mousey;

            mousex-= board.camera.x;
            mousey-= board.camera.y;
            var pointx = Math.round(mousex/100);
            var pointy = Math.round(mousey/100);
            var pointx2 = pointx;
            var pointy2 = pointy;

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

            board.setCursor(pointx, pointy, pointx2, pointy2, player.color)
        });
    }

});
