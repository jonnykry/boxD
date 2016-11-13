
var Board = {
  edges: null,
  maxRows: 1000,
  maxCols: 1000,

  init: function(maxRows, maxCols) {
    this.edges = [];
    maxRows = maxRows || 1000;
    maxCols = maxCols || 1000;

    return this;
  },

  // edge = {src: {x: int, y: int}, dst: {x: int, y: int}, owner: String}
  addEdge: function(edge) {
    this.edges.push(edge);
  },

  // src: {x: int, y: int}
  // dst: {x: int, y: int}
  removeEdge: function(src, dst) {
    this.edges = this.edges.filter(function (edge) {
      return (edge.src.x == src.x && edge.src.y == src.y && edge.dst.x == dst.x && edge.dst.y == dst.y);
    });
  }
};
