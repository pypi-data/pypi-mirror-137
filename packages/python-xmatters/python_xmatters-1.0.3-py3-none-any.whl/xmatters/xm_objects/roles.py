class Role(object):
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()


