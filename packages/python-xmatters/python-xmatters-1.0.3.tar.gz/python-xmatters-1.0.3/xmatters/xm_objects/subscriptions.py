import xmatters.connection
import xmatters.utils
import xmatters.factories
import xmatters.xm_objects.forms
from xmatters.xm_objects.common import Pagination, SelfLink
from xmatters.xm_objects.people import Person

class SubscriptionCriteriaReference(object):
    def __init__(self, data):
        self.name = data.get('name')
        self.operator = data.get('operator')
        self.value = data.get('value')
        self.values = data.get('values', [])

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Subscription(xmatters.connection.ApiBridge):
    _endpoints = {'get_subscribers': '/subscribers'}

    def __init__(self, parent, data):
        super(Subscription, self).__init__(parent, data)
        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')
        form = data.get('form')
        self.form = xmatters.xm_objects.forms.FormReference(form) if form else None
        owner = data.get('owner')

        self.owner = xmatters.xm_objects.people.PersonReference(self, owner)
        created = data.get('created')
        self.created = xmatters.utils.TimeAttribute(created) if created else None
        self.notification_delay = data.get('notificationDelay')
        criteria = data.get('criteria', {})
        self.criteria = Pagination(self, criteria, SubscriptionCriteriaReference) if criteria.get(
            'data') else []
        r = data.get('recipients', {})
        self.recipients = Pagination(self, r, xmatters.factories.RecipientFactory) if r.get('data') else []
        tdns = data.get('targetDeviceNames', {})
        self.target_device_names = Pagination(self, tdns, xmatters.factories.DeviceNameFactory) if tdns.get('data') else []
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None

    def get_subscribers(self, offset=None, limit=None):
        params = {'offset': offset,
                  'limit': limit}
        url = self.build_url(self._endpoints.get('get_subscribers'))
        subscribers = self.con.get(url, params=params)
        return Pagination(self, subscribers, xmatters.xm_objects.people.Person, limit=limit) if subscribers.get('data') else []

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
