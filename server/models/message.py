class Message(object):

    def __init__(self, msg):
        self.__message = msg

    def get_message(self):
        return self.__message


class LineClaimedMessage(Message):

    def __init__(self, point1, point2, owner):
        if not (isinstance(point1, tuple) and isinstance(point2, tuple)):
            raise ValueError("Point was not a tuple:  {}, {}".format(point1, point2))
        # TODO:  change to what Jonny and Blake will be expecting
        msg = {
            'type': 'line_claimed',
            'data': {
                'point1': {
                    'row': point1[0],
                    'col': point1[1],
                },
                'point2': {
                    'row': point2[0],
                    'col': point2[1],
                },
                'owner': owner
            }
        }

        super(LineClaimedMessage, self).__init__(msg)


class BoxCreatedMessage(Message):

    def __init__(self, corner_point, owner):
        if not isinstance(corner_point, tuple):
            raise ValueError("Point was not a tuple:  {}".format(corner_point))
        # TODO:  change to what Jonny and Blake will be expecting
        msg = {
            'type': 'box_created',
            'data': {
                'corner': {
                    'row': corner_point[0],
                    'col': corner_point[1],
                },
                'owner': owner
            }
        }

        super(BoxCreatedMessage, self).__init__(msg)


class NameChangedMessage(Message):
    def __init__(self, player_id, new_name):
        # TODO:  change to what Jonny and Blake will be expecting
        msg = {
            'type': 'name_changed',
            'data': {
                'player': player_id,
                'name': new_name}
        }
        super(NameChangedMessage, self).__init__(msg)


class BoardStateMessage(Message):
    def __init__(self, edges, boxes, client_color):

        edge_data = []
        box_data = []

        for edge_tuple in edges:
            point1 = edge_tuple[0]
            point2 = edge_tuple[1]
            color = edge_tuple[2]
            data_map = {
                'point1': {
                    'row': point1[0],
                    'col': point1[1],
                },
                'point2': {
                    'row': point2[0],
                    'col': point2[1],
                },
                'color': color
            }
            edge_data.append(data_map)

        for box_tuple in boxes:
            box_corner = box_tuple[0]
            print(str(box_corner))
            box_color = box_tuple[1]
            data_map = {
                'corner': {
                    'row': box_corner[0],
                    'col': box_corner[1]
                },
                'color': box_color
            }
            box_data.append(data_map)

        msg = {
            'type': 'board_state',
            'data': {
                'your_color': client_color,
                'edges': edge_data,
                'boxes': box_data
            }
        }
        super(BoardStateMessage, self).__init__(msg)
