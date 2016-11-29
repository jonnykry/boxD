
$(document).ready( function() {
    $('#entryModal').modal({show: true});

    if (!('WebSocket' in window)) {
        alert('Your browser does not support web sockets');
    } else {
        var socket = setup();
        // TODO: Generate player based on `JOIN_GAME` response
        var player = Player.init("Jonny", "blue");
        var game = Game.init(player);
        var board = game.board;

        board.canvas.addEventListener('mousedown', function(e) {
            var mouseX = e.pageX;
            var mouseY = e.pageY;
            mouseX -= board.camera.x;
            mouseY -= board.camera.y;

            var points = board.getPointsByCursor(mouseX, mouseY);

            console.log(points.pointX, points.pointY, points.pointX2, points.pointY2);

            // TODO:  If the edge is valid, let's do it
            // Note:  Pass as (y, x) since backend uses (r, c)
            var request = {
               type:  'CLAIM_LINE',
               data: {
                   pt1_r: points.pointY,
                   pt1_c: points.pointX,
                   pt2_r: points.pointY2,
                   pt2_c: points.pointX2
               }
            };

            //if it passes update cooloff timer
            var d = new Date();
            var s = d.getSeconds();
            console.log(s);
            var carryover = 0;
            if (s>=55){
                carryover = s - 60;
            }

            board.move_timer=s+5 + carryover;
            board.cooloff_timer=s;
            board.next_move=s+15 + carryover;
            board.cooloff_end=s+5 + carryover;
            socket.send(JSON.stringify(request));

            board.claimEdge(points.pointX, points.pointY, points.pointX2, points.pointY2, player.color);
        });

        board.canvas.addEventListener('mousemove', function(e) {
            var mouseX = e.pageX;
            var mouseY = e.pageY;
            board.curX = mouseX;
            board.curY = mouseY;
            mouseX -= board.camera.x;
            mouseY -= board.camera.y;

            var points = board.getPointsByCursor(mouseX, mouseY);

            board.setCursor(points.pointX, points.pointY, points.pointX2, points.pointY2, player.color)
        });
    }

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

        var _socket = new WebSocket(host);
        //console.log("socket status: " + socket.readyState);

        var $nickname = $('#nickname');
        var $startGame = $('#startGame');

        $nickname.focus();

        // event handlers for UI
        $startGame.on('click', function () {
            var text = $nickname.val();

            if (text === null || text === 'undefined') text = '';

            var request = {
                type: 'JOIN_GAME',
                data: {
                    name: text
                }
            };

            _socket.send(JSON.stringify(request));
            $nickname.val('');
        });

        $nickname.keypress(function (evt) {
            if (evt.which == 13) { // ENTER
                $startGame.click();
            }
        });

        var $testText = $('#testText');
        var $submit = $('#submit');

        $submit.on('click', function () {
            var text = $testText.val();

            if (text === null || text === 'undefined') text = '';

            _socket.send(text);
            $testText.val('');
        });

        // event handlers for websocket
        if (_socket) {
            _socket.onopen = function () {
                // TODO: Let the client be idle and view ongoing game behind modal
            };

            _socket.onmessage = function (msg) {
                // TODO: Set listeners and call subsequent functions
                console.log(msg);
                if (msg === 'line_claimed') {
                    console.log('A line was successfully claimed on the server.');
                    console.log(msg.data);
                    // TODO: call board.claimEdge(data);
                } else {
                    showServerResponse(msg.data);
                }
            };

            _socket.onclose = function () {
                console.log("Closed");
                showServerResponse('The connection has been closed.');
            }
        } else {
            console.log('invalid socket');
        }

        function showServerResponse(txt) {
            var p = document.createElement('p');
            p.innerHTML = txt;
            document.getElementById('output').appendChild(p);
        }

        return _socket;
    }
});
