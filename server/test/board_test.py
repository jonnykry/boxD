import unittest,os,sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

from models.board import Board


def main():

    b = Board(5, 4)

    assert b.get_rows() == 5
    assert b.get_cols() == 4

    b.claim_edge((0, 0), (0, 1), 'sam')
    b.claim_edge((1, 0), (0, 0), 'sam')

    assert b.get_edge_owner((0, 0), (1, 0)) == 'sam'  # previous addition should have coerced via rows

    b.claim_edge((1, 0), (1, 1), 'sam')
    b.claim_edge((1, 2), (1, 1), 'sam')

    assert b.get_edge_owner((1, 1), (1, 2)) == 'sam'  # previous addition should have coerced via cols

    b.claim_edge((0, 1), (0, 2), 'sam')
    b.claim_edge((0, 2), (1, 2), 'sam')

    assert b.claim_edge((0, 1), (1, 1), 'sam') == [(0, 0), (0, 1)]  # should create two boxes

    assert len(b.get_boxes()) == 2
    assert ((0, 0), 'sam') in b.get_boxes()
    assert ((0, 1), 'sam') in b.get_boxes()

    # todo:
    #  test adding an invalid line, ensuring board throws an error
    #  test creating a box where the final edge was added on the board boundary (make sure get_new_boxes handles that)
    #  should prolly actually unit test this whole bad boy...

    return 0

if __name__ == '__main__':
    main()
