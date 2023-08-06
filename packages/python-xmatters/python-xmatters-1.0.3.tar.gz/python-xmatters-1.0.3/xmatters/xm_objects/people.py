import xmatters.factories
import xmatters.utils as utils
from xmatters.xm_objects.common import Recipient, SelfLink, Pagination
from xmatters.xm_objects.roles import Role
from xmatters.connection import ApiBridge
import xmatters.xm_objects.groups


class Person(Recipient):
    _endpoints = {'get_devices': '/devices',
                  'roles': '?embed=roles',
                  'get_supervisors': '/supervisors',
                  'supervisors': '?embed=supervisors',
                  'get_groups': '/group-memberships'}

    def __init__(self, parent, data):
        super(Person, self).__init__(parent, data)
        self.first_name = data.get('firstName')
        self.last_name = data.get('lastName')
        self.license_type = data.get('licenseType')
        self.language = data.get('language')
        self.timezone = data.get('timezone')
        self.web_login = data.get('webLogin')
        self.phone_login = data.get('phoneLogin')
        self.phone_pin = data.get('phonePin')
        self.properties = data.get('properties', {})
        last_login = data.get('lastLogin')
        self.last_login = utils.TimeAttribute(last_login) if last_login else None
        when_created = data.get('whenCreated')
        self.when_created = utils.TimeAttribute(when_created) if when_created else None
        when_updated = data.get('whenUpdated')
        self.when_updated = utils.TimeAttribute(when_updated) if when_updated else None
        links = data.get('links')
        self.links = SelfLink(self, data) if links else None

    @property
    def roles(self):
        url = self.build_url(self._endpoints.get('roles'))
        data = self.con.get(url)
        roles = data.get('roles', {})
        return Pagination(self, roles, Role) if roles.get('data') else []

    @property
    def devices(self):
        return self.get_devices()

    @property
    def supervisors(self):
        return self.get_supervisors()

    def get_supervisors(self, offset=None, limit=None):
        params = {'offset': offset,
                  'limit': limit}
        url = self.build_url(self._endpoints.get('get_supervisors'))
        s = self.con.get(url, params=params)
        return Pagination(self, s, Person) if s.get('data') else []

    def get_devices(self, offset=None, limit=None, phone_number_format=None, at=None):
        params = {'phoneNumberFormat': phone_number_format,
                  'at': self.process_time_param(at),
                  'offset': offset,
                  'limit': limit}
        url = self.build_url(self._endpoints.get('get_devices'))
        devices = self.con.get(url, params=params)
        return Pagination(self, devices, xmatters.factories.DeviceFactory) if devices.get('data') else []

    def get_groups(self, offset=None, limit=None):
        params = {'offset': offset,
                  'limit': limit}
        url = self.build_url(self._endpoints.get('get_groups'))
        groups = self.con.get(url, params=params)
        return Pagination(self, groups, xmatters.xm_objects.groups.GroupMembership) if groups.get('data') else []

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()


class PersonReference(ApiBridge):
    def __init__(self, parent, data):
        super(PersonReference, self).__init__(parent, data)
        self.id = data.get('id')
        self.target_name = data.get('targetName')
        self.first_name = data.get('firstName')
        self.last_name = data.get('lastName')
        self.recipient_type = data.get('recipientType')
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()
