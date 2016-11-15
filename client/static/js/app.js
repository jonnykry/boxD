
$(document).ready( function() {
    var board = Board.init();

    // Temporarily testing board/game here, though we should move this to another file ran serparately
   // board.claimEdge({x: 3, y: 2}, {x: 3, y: 3}, 'Blake');
    //board.claimEdge({x: 3, y: 2}, {x: 2, y: 3}, 'Jonny');
    //console.log(board.edges.length);
    //board.removeEdge({x: 3, y: 2}, {x: 3, y: 3});
    //board.removeEdge({x: 3, y: 2}, {x: 3, y: 3});
    //console.log(board.edges.length);

    $('#entryModal').modal({show: true});

    if (!("WebSocket" in window)) {
        alert("Your browser does not support web sockets");
    } else {
        setup();
    }

    function getParameterByName(name, url) {
        if (!url) {
            url = window.location.href;
        }

        name = name.replace(/[\[\]]/g, "\\$&");
        var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
                results = regex.exec(url);
        if (!results) return null;
        if (!results[2]) return '';
        return decodeURIComponent(results[2].replace(/\+/g, " "));
    }

    function setup(){
        // Note: You have to change the host var
        // if your client runs on a different machine than the websocket server

        var host;
        if (getParameterByName('local') == 'true') {
            host = "ws://localhost:5000/ws"
        } else {
            host = "wss://boxd.herokuapp.com/ws";
        }

        var socket = new WebSocket(host);
        //console.log("socket status: " + socket.readyState);

        var $txt = $("#data");
        var $btnSend = $("#sendtext");

        $txt.focus();

        // event handlers for UI
        $btnSend.on('click',function(){
            var text = $txt.val();
            if(text == ""){
                return;
            }

            socket.send(text);
            $txt.val("");
        });

        $txt.keypress(function(evt){
            if(evt.which == 13){
                $btnSend.click();
            }
        });

        // event handlers for websocket
        if(socket){
            socket.onopen = function(){
                //alert("connection opened....");
            };

            socket.onmessage = function(msg){
                showServerResponse(msg.data);
            };

            socket.onclose = function(){
                //alert("connection closed....");
                showServerResponse("The connection has been closed.");
            }

        } else {
            console.log("invalid socket");
        }

        function showServerResponse(txt){
            var p = document.createElement('p');
            p.innerHTML = txt;
            document.getElementById('output').appendChild(p);
        }
    }
});
