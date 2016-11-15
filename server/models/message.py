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

