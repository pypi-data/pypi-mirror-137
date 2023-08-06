from xmatters.xm_objects.common import Recipient, ReferenceById
from xmatters.xm_objects.people import PersonReference


class Provider(object):
    def __init__(self, data):
        self.id = data.get('id')

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.id)

    def __str__(self):
        return self.__repr__()


class Device(Recipient):
    _endpoints = {'timeframes': '?embed=timeframes'}

    def __init__(self, parent, data):
        super(Device, self).__init__(parent, data)
        self.default_device = data.get('defaultDevice')
        self.delay = data.get('delay')
        self.description = data.get('description')
        self.device_type = data.get('deviceType')
        self.name = data.get('name')
        owner = data.get('owner')
        self.owner = PersonReference(self, owner) if owner else None
        self.priority_threshold = data.get('priorityThreshold')
        provider = data.get('provider')
        self.provider = ReferenceById(provider) if provider else None
        self.sequence = data.get('sequence')
        self.test_status = data.get('testStatus')

    @property
    def timeframes(self):
        url = self.build_url(self._endpoints.get('timeframes'))
        data = self.con.get(url).get('timeframes', {}).get('data', [])
        return [DeviceTimeframe(timeframe) for timeframe in data]

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()


class EmailDevice(Device):
    def __init__(self, parent, data):
        super(EmailDevice, self).__init__(parent, data)
        self.email_address = data.get('emailAddress')

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()


class VoiceDevice(Device):
    def __init__(self, parent, data):
        super(VoiceDevice, self).__init__(parent, data)
        self.phone_number = data.get('phoneNumber')

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()


class SMSDevice(Device):
    def __init__(self, parent, data):
        super(SMSDevice, self).__init__(parent, data)
        self.phone_number = data.get('phoneNumber')

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()


class TextPagerDevice(Device):
    def __init__(self, parent, data):
        super(TextPagerDevice, self).__init__(parent, data)
        self.pin = data.get('pin')
        self.two_way_device = data.get('twoWayDevice')

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()


class ApplePushDevice(Device):
    def __init__(self, parent, data):
        super(ApplePushDevice, self).__init__(parent, data)
        self.account_id = data.get('accountId')
        self.apn_token = data.get('apnToken')
        self.alert_sound = data.get('alertSound')
        self.sound_status = data.get('soundStatus')
        self.sounds_threshold = data.get('soundThreshold')

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()


class AndroidPushDevice(Device):
    def __init__(self, parent, data):
        super(AndroidPushDevice, self).__init__(parent, data)
        self.account_id = data.get('accountId')
        self.registration_id = data.get('registrationId')

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()


class FaxDevice(Device):
    def __init__(self, parent, data):
        super(FaxDevice, self).__init__(parent, data)
        self.phone_number = data.get('phoneNumber')
        self.country = data.get('country')

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()


class PublicAddressDevice(Device):
    def __init__(self, parent, data):
        super(PublicAddressDevice, self).__init__(parent, data)
        self.phone_number = data.get('phoneNumber')

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()


class GenericDevice(Device):
    def __init__(self, parent, data):
        super(GenericDevice, self).__init__(parent, data)
        self.phone_number = data.get('pin')

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()


class DeviceTimeframe(object):
    def __init__(self, data):
        self.days = data.get('days')
        self.duration_in_minutes = data.get('durationInMinutes')
        self.exclude_holidays = data.get('excludeHolidays')
        self.name = data.get('name')
        self.start_time = data.get('startTime')
        self.timezone = data.get('timezone')

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()


