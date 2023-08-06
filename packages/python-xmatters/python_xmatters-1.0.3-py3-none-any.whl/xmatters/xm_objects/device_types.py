class DeviceTypes(object):
    def __init__(self, data):
        self.count = data.get('count')
        self.total = data.get('total')
        self.data = data.get('data', [])

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


