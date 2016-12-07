
var Game = {
    board: null,
    player: null,

    init: function(player) {
        this.board = Board.init();
        this.player = player;
        return this;
    }
};
