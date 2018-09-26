class TypeError(Exception):
    type = None

    def __init__(self, type):
        self.type = type

    def __str__(self):
        return 'unexcepted type: {type}.'.format(type = self.type)
