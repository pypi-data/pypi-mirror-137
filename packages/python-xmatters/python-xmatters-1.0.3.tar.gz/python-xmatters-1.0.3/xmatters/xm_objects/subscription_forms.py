import xmatters.factories
import xmatters.xm_objects.forms
import xmatters.utils
import xmatters.connection
import xmatters.xm_objects.plans
import xmatters.xm_objects.roles
from xmatters.xm_objects.common import Pagination, SelfLink

class SubscriptionForm(xmatters.connection.ApiBridge):
    _endpoints = {'target_device_names': '?embed=deviceNames',
                  'visible_target_device_names': '?embed=deviceNames',
                  'property_definitions': '?embed=propertyDefinitions',
                  'roles': '?embed=roles'}

    def __init__(self, parent, data):
        super(SubscriptionForm, self).__init__(parent, data)
        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')
        plan = data.get('plan')
        self.plan = xmatters.xm_objects.plans.PlanReference(data) if plan else None
        self.scope = data.get('scope')
        form = data.get('form')
        self.form = xmatters.xm_objects.forms.FormReference(form) if form else None
        created = data.get('created')
        self.created = xmatters.utils.TimeAttribute(created) if created else None
        self.one_way = data.get('oneWay')
        self.subscribe_others = data.get('subscribeOthers')
        self.notification_delay = data.get('notificationDelay')
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None

    @property
    def target_device_names(self):
        url = self.build_url(self._endpoints.get('target_device_names'))
        data = self.con.get(url)
        tdns = data.get('targetDeviceNames', {})
        return Pagination(self, tdns, xmatters.factories.DeviceNameFactory) if tdns.get('data') else []

    @property
    def visible_target_device_names(self):
        url = self.build_url(self._endpoints.get('visible_target_device_names'))
        data = self.con.get(url)
        vtdns = data.get('visibleTargetDeviceNames', {})
        return Pagination(self, vtdns, xmatters.factories.DeviceNameFactory) if vtdns.get('data') else []

    @property
    def property_definitions(self):
        url = self.build_url(self._endpoints.get('property_definitions'))
        data = self.con.get(url)
        ps = data.get('propertyDefinitions', {})
        return Pagination(self, ps, xmatters.factories.PropertiesFactory) if ps.get('data') else []

    @property
    def roles(self):
        url = self.build_url(self._endpoints.get('roles'))
        data = self.con.get(url).get('roles')
        roles = data.get('roles')
        return Pagination(self, roles, xmatters.xm_objects.roles.Role) if roles else []

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()


class SubscriptionFormReference(object):
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        plan = data.get('plan')
        self.plan = xmatters.xm_objects.plans.PlanReference(plan) if plan else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
