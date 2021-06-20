def find_opposite(direction):
    if direction == 'South':
        return 'North'
    if direction == 'North':
        return 'South'
    if direction == 'East':
        return 'West'
    if direction == 'West':
        return 'East'
    if direction == 'Up':
        return 'Down'
    if direction == 'Down':
        return 'Up'
    if direction == 'Up1':
        return "Down1"
    if direction == 'Down1':
        return 'Up1'


class Warp:

    def __init__(self, coordinate: (int, int)):
        self.coordinate = coordinate
