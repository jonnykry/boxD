$( document ).ready( function() {
  game = Game.init();
  board = game.board;
  console.log(board.maxRows, board.maxCols, board.edges);

  // Temporarily testing board/game here, though we should move this to another file ran serparately
  console.log(board.edges.length);
  board.addEdge({src: {x: 1, y: 2}, dst: {x: 2, y: 2}, owner: 'Jonny'});
  board.addEdge({src: {x: 3, y: 2}, dst: {x: 3, y: 3}, owner: 'Blake'});
  board.removeEdge({x: 3, y: 2}, {x: 3, y: 3});
  console.log(board.edges.length);

  $('#entryModal').modal({show: true});

  if (!("WebSocket" in window)) {
      alert("Your browser does not support web sockets");
  } else {
      setup();
  }

  function setup(){

    // Note: You have to change the host var
    // if your client runs on a different machine than the websocket server

    var host = "ws://localhost:9090/ws";
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
      }

      socket.onmessage = function(msg){
        showServerResponse(msg.data);
      }

      socket.onclose = function(){
        //alert("connection closed....");
        showServerResponse("The connection has been closed.");
      }

    }else{
      console.log("invalid socket");
    }

    function showServerResponse(txt){
      var p = document.createElement('p');
      p.innerHTML = txt;
      document.getElementById('output').appendChild(p);
    }


  }

});
