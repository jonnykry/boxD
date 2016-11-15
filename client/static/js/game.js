
// TODO:  Generate a color map for N users, or create a static map
var Game = {
    board: null,
    users: null,
    maxUsers: 8,

    init: function(maxUsers) {
        maxUsers = maxUsers || 8;
        this.board = Board.init();
        users = [];

        return this;
    },

    addUser: function(name) {
        users.push({name: name, color: 0, score: 0, });
    }
};
