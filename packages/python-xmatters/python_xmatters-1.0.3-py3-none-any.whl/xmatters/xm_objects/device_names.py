class TargetDeviceNameSelector(object):
    def __init__(self, data):
        self.name = data.get('name')
        self.selected = data.get('selected')
        self.visible = data.get('visible')

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()


class DeviceName(object):
    def __init__(self, data):
        self.id = data.get('id')
        self.device_type = data.get('deviceType')
        self.name = data.get('name')
        self.description = data.get('description')
        self.privileged = data.get('privileged')

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()


class DeviceNameEmail(DeviceName):
    def __init__(self, data):
        super(DeviceNameEmail, self).__init__(data)
        self.domains = data.get('domains', [])

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()

