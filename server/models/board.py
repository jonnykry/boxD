"""
'  Class modeling a box game board
'
'  rows:  number of rows in the grid
'  cols:  number of columns in the grid
'
'  edges are maintained in a map of maps with the following structure:
'    { sourcePoint1: {neighboringPoint1: owner, neighboringPoint2: owner}, sourcePoint2: ... }
'
'    where each point is a row-majored tuple of 2 integers describing the row and column of the point.
'
'  completed boxes are maintained in a map mapping the top-left corner of the box to the owner of the box
"""


class Board(object):

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self._edges = {}  # maps edges to edge owner (board[p1][p2] = Owner)
        self._boxes = {}  # maps top-left point of each box to box owner

        self._reset_board()

    '''
    '' Resets the board and box maps
    ''
    '' Adds unowned edges to each possible position on the board
    '''
    def _reset_board(self):
        self._boxes = {}
        for r in range(0, self.rows):
            for c in range(0, self.cols):

                if not (r, c) in self._edges:
                    self._edges[(r, c)] = {}

                # add an un-owned edge from the current node to the node below and to the right
                # do not add an edge that goes out of bounds (r + 1 exceeds rows, c + 1 exceeds cols)
                if not c == self.cols - 1:
                    self._edges[(r, c)][(r, c + 1)] = None

                if not r == self.rows - 1:
                    self._edges[(r, c)][(r + 1, c)] = None

    '''
    '' Returns the owner of the edge (p1, p2)
    ''  p1:     A tuple describing source node (row, col)
    ''  p2:     A tuple describing target node (row, col)
    ''
    ''  Returns the owner of the edge, or None if the edge is unowned
    '''
    def get_edge_owner(self, p1, p2):

        if len(p1) != 2 or len(p2) != 2:
            raise ValueError("A point was not a tuple of len 2: {}, {}".format(p1, p2))

        if not self._is_valid_edge(p1, p2):
            raise ValueError("Edge is not valid:  {}, {}".format(str(p1), str(p2)))

        p1, p2 = self._coerce_points(p1, p2)

        return self._edges[p1][p2]

    '''
    '' Returns True if the edge (p1, p2) is owned
    ''  p1:     A tuple describing source node (row, col)
    ''  p2:     A tuple describing target node (row, col)
    ''
    ''  Returns the owner of the edge, or None if the edge is unowned
    '''
    def edge_is_owned(self, p1, p2):
        return self.get_edge_owner(p1, p2) is not None

    '''
    '' Claims an unowned edge from p1 to p2
    ''
    ''  p1:     A tuple describing source node (row, col)
    ''  p2:     A tuple describing target node (row, col)
    ''  player: the owner of the new edge
    ''
    ''  This implementation coerces the source node to always be above or to the left of the destination node
    ''    eg: if claim_edge((1, 1), (0, 1), PLAYER) is called, board[(0, 1)][(1, 1)] is assigned to PLAYER
    ''
    ''  Raises an ValueError if the edge is already owned
    ''  Raises a ValueError if the edge isn't between two adjacent nodes
    '''
    def claim_edge(self, p1, p2, owner):

        if len(p1) != 2 or len(p2) != 2:
            raise ValueError("A point was not a tuple of len 2: {}, {}".format(p1, p2))

        if not owner:
            raise ValueError("Owner should not be None")

        if not self._is_valid_edge(p1, p2):
            raise ValueError("Edge is not valid:  {}, {}".format(str(p1), str(p2)))

        p1, p2 = self._coerce_points(p1, p2)
        if p1 not in self._edges:
            self._edges[p1] = {}

        if self._edges[p1][p2]:
            raise

        created_boxes = self._get_new_boxes(p1, p2)

        self._edges[p1][p2] = owner

        # TODO:  implement _get_new_boxes
        # for box in created_boxes:
        #     self.boxes[box] = owner

    '''
    '' Returns the list of boxes that would be made by adding a line
    ''
    ''  p1: a tuple describing source node (row, col)
    ''  p2: a tuple describing target node (row, col)
    ''
    ''  Throws an ValueError if the edge already exists on the board
    '''
    def _get_new_boxes(self, p1, p2):
        pass

    '''
    ''  Returns True if a valid edge could possibly exist between two points
    ''    That is to say, returns True if the two points provided are immediately adjacent to each other
    '''
    @staticmethod
    def _is_valid_edge(p1, p2):

        # if the difference in two points' x is 1 or -1   XOR
        # the difference in two points' y is 1 or -1, then the points are either immediately above or beside each other
        return bool(abs(p1[0] - p2[0]) == 1) ^ bool(abs(p1[1] - p2[1]) == 1)

    '''
    '' Returns the proper ordering of p1 and p2.
    ''    If p1 is above p2 or p1 is to the left of p2, returns p1, p2.
    ''    Otherwise returns p2, p1
    '''
    @staticmethod
    def _coerce_points(p1, p2):

        if p1[0] == p2[0]:
            if p1[1] < p2[1]:
                return p1, p2
            return p2, p1

        if p1[1] == p2[1]:
            if p1[0] < p2[0]:
                return p1, p2

            return p2, p1

        raise ValueError("Either row or column must match: {}, {}".format(p1, p2))