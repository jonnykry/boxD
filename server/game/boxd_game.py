class BoxdGame(object):

    def __init__(self):
        self.__players = []
        self.__board = Board(10, 10)

    def add_player(self, player_id):

        if player_id in self.__players:
            raise ValueError("Player already in game:  {}".format(player_id))

        self.__players.append(player_id)

    def remove_player(self, player_id):

        if player_id not in self.__players:
            raise ValueError("Player is not in game:  {}".format(player_id))

        # find all of the boxes owned by player_id
        to_void = []
        for (point, owner_id) in self.__board.get_boxes():
            if owner_id == player_id:
                to_void.append(point)

        # remove player_id from ownership
        if __name__ == '__main__':
            for box_corner in to_void:
                self.__board.remove_box_owner(box_corner)

        self.__players.remove(player_id)

        # for now, leave all lines owned by player_id.  Those can stay

    def get_players(self):
        return self.__players

    def claim_line(self, pt1, pt2, player_id):

        try:
            return self.__board.claim_edge(pt1, pt2, player_id)

        except ValueError:
            # line was somehow invalid
            return None



# TODO:  Figure out how to move back to models?

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
        self.__rows = rows
        self.__cols = cols
        self.__edges = {}  # maps edges to edge owner (board[p1][p2] = Owner)
        self.__boxes = {}  # maps top-left point of each box to box owner

        self.reset_board()

    '''
    '' Resets the board and box maps
    ''
    '' Adds unowned edges to each possible position on the board
    '''
    def reset_board(self):
        self.__boxes = {}
        for r in range(0, self.__rows):
            for c in range(0, self.__cols):

                if not (r, c) in self.__edges:
                    self.__edges[(r, c)] = {}

                # add an un-owned edge from the current node to the node below and to the right
                # do not add an edge that goes out of bounds (r + 1 exceeds rows, c + 1 exceeds cols)
                if not c == self.__cols - 1:
                    self.__edges[(r, c)][(r, c + 1)] = None

                if not r == self.__rows - 1:
                    self.__edges[(r, c)][(r + 1, c)] = None

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

        if not self.__is_valid_edge(p1, p2):
            raise ValueError("Edge is not valid:  {}, {}".format(str(p1), str(p2)))

        p1, p2 = self.__coerce_points(p1, p2)

        return self.__edges[p1][p2]

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
    ''  Returns:  the list of boxes created by claiming an edge
    ''
    ''  This implementation coerces the source node to always be above or to the left of the destination node
    ''    eg: if claim_edge((1, 1), (0, 1), PLAYER) is called, edges[(0, 1)][(1, 1)] is assigned to PLAYER
    ''
    ''  Raises an EdgeOwnedError if the edge is already owned
    ''  Raises a ValueError if the edge is invalid or owner is None
    '''
    def claim_edge(self, p1, p2, owner):

        if len(p1) != 2 or len(p2) != 2:
            raise ValueError("A point was not a tuple of len 2: {}, {}".format(p1, p2))

        if not owner:
            raise ValueError("Owner should not be None")

        if not self.__is_valid_edge(p1, p2):
            raise ValueError("Edge is not valid:  {}, {}".format(p1, p2))

        if self.edge_is_owned(p1, p2):
            raise EdgeOwnedError()

        p1, p2 = self.__coerce_points(p1, p2)

        created_boxes = self.__get_new_boxes(p1, p2)

        self.__edges[p1][p2] = owner

        for box in created_boxes:
            self.__boxes[box] = owner

        return created_boxes

    '''
    '  Sets the owner of the box specified at box_corner to None
    '
    '  Raises a ValueError if the box does not exist
    '''

    def remove_box_owner(self, box_corner):

        if box_corner not in self.__boxes:
            raise ValueError("Box does not exist:  {}".format(box_corner))

        self.__boxes[box_corner] = None

    '''
    '' Returns the list of boxes that would be made by adding a line
    ''
    ''  p1: a tuple describing source node (row, col)
    ''  p2: a tuple describing target node (row, col)
    ''
    ''  Throws an ValueError if the edge already exists on the board
    '''
    def __get_new_boxes(self, p1, p2):

        if not self.__is_valid_edge(p1, p2):
            raise ValueError("Edge is not valid:  {}, {}".format(str(p1), str(p2)))

        if self.edge_is_owned(p1, p2):
            raise ValueError("Edge is already owned:  {}, {}".format(str(p1), str(p2)))

        new_boxes = []

        # coerce p1, p2 so that p1 is either the top point or the left point in this line
        p1, p2 = self.__coerce_points(p1, p2)

        # if added edge is vertical
        if p2[0] - p1[0] == 1:

            # check if boxes exist to the left or right

            lbtp = self.__left_neighbor(p1)     # lbtp = left box top point
            lbbp = self.__left_neighbor(p2)     # lbbp = left box bottom point
            rbtp = self.__right_neighbor(p1)    # rbtp = right box top point
            rbbp = self.__right_neighbor(p2)    # rbbp = right box bottom point

            #  lbtp --- p1 --- rbtp
            #    |      | <--new |
            #  lbbp --- p2 --- rbbp
            #
            #  potential new boxes have top-left corners at [lbtp, p1]

            # check if the 3 lines necessary for a new box to exist are there

            if (self.__is_valid_edge(lbtp, p1) and self.edge_is_owned(lbtp, p1)) and \
                    (self.__is_valid_edge(lbbp, p2) and self.edge_is_owned(lbbp, p2))and \
                    (self.__is_valid_edge(lbtp, lbbp) and self.edge_is_owned(lbtp, lbbp)):

                new_boxes.append(lbtp)

            # check if the 3 lines necessary for a new box to exist are there
            if (self.__is_valid_edge(p1, rbtp) and self.edge_is_owned(p1, rbtp)) and \
                    (self.__is_valid_edge(p2, rbbp) and self.edge_is_owned(p2, rbbp))and \
                    (self.__is_valid_edge(rbtp, rbbp) and self.edge_is_owned(rbtp, rbbp)):

                new_boxes.append(p1)

            return new_boxes

        elif p2[1] - p1[1] == 1:

            # check if boxes exist above or below

            tblp = self.__top_neighbor(p1)      # tblp = top box left point
            tbrp = self.__top_neighbor(p2)      # tbrp = tob box right point
            bblp = self.__bottom_neighbor(p1)   # bblp = bottom box left point
            bbrp = self.__bottom_neighbor(p2)   # bbrp = bottom box right point

            #  tblp --- tbrp
            #    |       |
            #    p1 -n-  p2
            #    |       |
            #  bblp ---  bbrp
            #
            #  potential new boxes have top-left corners at [tblp, p1]

            # check if the 3 lines necessary for a new box to exist are there
            if (self.__is_valid_edge(tblp, p1) and self.edge_is_owned(tblp, p1)) and \
                    (self.__is_valid_edge(tbrp, p2) and self.edge_is_owned(tbrp, p2))and \
                    (self.__is_valid_edge(tblp, tbrp) and self.edge_is_owned(tblp, tbrp)):

                new_boxes.append(tblp)

            # check if the 3 lines necessary for a new box to exist are there
            if (self.__is_valid_edge(p1, bblp) and self.edge_is_owned(p1, bblp)) and \
                    (self.__is_valid_edge(p2, bbrp) and self.edge_is_owned(p2, bbrp))and \
                    (self.__is_valid_edge(bblp, bbrp) and self.edge_is_owned(bblp, bbrp)):

                new_boxes.append(p1)

            return new_boxes

    '''
    ''  Returns True if a valid edge could possibly exist between two points
    ''    That is to say, returns True if the two points provided are in bounds/immediately adjacent to each other
    '''
    def __is_valid_edge(self, p1, p2):

        # if the difference in two points' x is 1 or -1   XOR
        # the difference in two points' y is 1 or -1, then the points are either immediately above or beside each other
        try:
            p1, p2 = self.__coerce_points(p1, p2)
        except ValueError:
            return False

        if p1[0] < 0 or p1[1] < 0 or p1[0] > self.__rows or p1[1] > self.__cols:
            return False

        if p2[0] < 0 or p2[1] < 0 or p2[0] > self.__rows or p2[1] > self.__cols:
            return False

        return bool(abs(p1[0] - p2[0]) == 1) ^ bool(abs(p1[1] - p2[1]) == 1)

    '''
    '' Returns the proper ordering of p1 and p2.
    ''    If p1 is above p2 or p1 is to the left of p2, returns p1, p2.
    ''    Otherwise returns p2, p1
    '''
    @staticmethod
    def __coerce_points(p1, p2):

        if p1[0] == p2[0]:
            if p1[1] < p2[1]:
                return p1, p2
            return p2, p1

        if p1[1] == p2[1]:
            if p1[0] < p2[0]:
                return p1, p2

            return p2, p1

        raise ValueError("Either row or column must match: {}, {}".format(p1, p2))

    def get_rows(self):
        return self.__rows

    def get_cols(self):
        return self.__cols

    """
    ' For now, returns a list of tuples where the first item is the point indicating the top-left corner of the box
    ' and the second item is the owner of the box
    """
    def get_boxes(self):
        boxes = []
        for (point, owner) in self.__boxes.iteritems():
            boxes.append((point, owner))

        return boxes

    @staticmethod
    def __left_neighbor(point):
        left = (point[0], point[1] - 1)
        return left

    @staticmethod
    def __right_neighbor(point):
        right = (point[0], point[1] + 1)
        return right

    @staticmethod
    def __top_neighbor(point):
        top = (point[0] - 1, point[1])
        return top

    @staticmethod
    def __bottom_neighbor(point):
        bottom = (point[0] + 1, point[1])
        return bottom


class EdgeOwnedError(Exception):
    def __init__(self):
        pass