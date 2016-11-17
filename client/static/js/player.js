
var Player = {
    nickname: null,
    color: null,
    score: null,

    init: function(nickname, color) {
        this.nickname = nickname;
        this.color = color;
        this.score = 0;

        return this;
    }
};
