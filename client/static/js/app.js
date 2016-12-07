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
            if (board.cooloff_timer > board.cooloff_end - 1){
                if(mouseX > scale && mouseY > scale && mouseX < board.maxCols * scale && mouseY < board.maxCols * scale ){

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
                }
            //if it passes update cooloff timer
            Board.cooloff_timer = 0 ;
            Board.move_timer =  0;
            Board.next_move = 10;
            Board.cooloff_end= 5;
            socket.send(JSON.stringify(request));
            }

        });

        board.canvas.addEventListener('mousemove', function(e) {
            var mouseX = e.pageX;
            var mouseY = e.pageY;
            board.curX = mouseX;
            board.curY = mouseY;
            mouseX -= board.camera.x;
            mouseY -= board.camera.y;

            if(mouseX > 100 && mouseY > 100 && mouseX < board.maxCols * scale && mouseY < board.maxCols * scale){
                var points = board.getPointsByCursor(mouseX, mouseY);

                board.setCursor(points.pointX, points.pointY, points.pointX2, points.pointY2, game.player.color);

            }
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
        console.log("socket status: " + _socket.readyState);

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
                var data = {};

                try {
                    data = JSON.parse(msg.data);
                } catch(err) {
                    data = msg.data;
                }

                if (data.type === 'line_claimed') {
                    console.log('A line was successfully claimed on the server.');
                    console.log(data);
                    // TODO: grab color from data
                    // x1, y1, x2, y2, color
                    //game.player.color = data.data.owner;
                    board.claimEdge(data.data.point1.col, data.data.point1.row, data.data.point2.col, data.data.point2.row, data.data.owner);
                } else if (data.type === 'box_created') {
                    board.claimSquare(data.data.corner.col, data.data.corner.row,data.data.owner);
                    if(data.data.owner == game.player.color){
                        Board.cooloff_timer = 5 ;
                        Board.move_timer =  0;
                        Board.next_move = 10;
                        Board.cooloff_end= 5;
                    }
                    console.log('A box was successfully created on the server.');

                } else if (data.type === 'board_state') {
                    console.log('Drawing Board');
                    console.log(data);
                    game.player.color = data.data.your_color;
                    data.data.edges.forEach(function(edge) {
                        board.claimEdge(edge.point1.col, edge.point1.row, edge.point2.col, edge.point2.row, edge.color);
                    });

                    data.data.boxes.forEach(function(box) {
                        board.claimSquare(box.corner.col, box.corner.row, box.color);
                    });
                    data.data.scores.forEach(function(score) {
                        Board.update_scores(score);
                    });
                } else if (data.type === 'score_update') {
                    console.log('Updating Score');
                    console.log(data);
                    Board.update_scores(data.data);

                } else {
                    showServerResponse(data);
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
