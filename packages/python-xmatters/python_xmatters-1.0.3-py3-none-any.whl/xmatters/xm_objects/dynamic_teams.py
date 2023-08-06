from xmatters.xm_objects.common import Recipient, Pagination, SelfLink
from xmatters.xm_objects.people import Person
from xmatters.xm_objects.roles import Role
from xmatters.xm_objects.subscriptions import SubscriptionCriteriaReference


class DynamicTeam(Recipient):
    _endpoints = {'supervisors': '?embed=supervisors',
                  'observers': '?embed=observers',
                  'get_members': '/members'}

    def __init__(self, parent, data):
        super(DynamicTeam, self).__init__(parent, data)
        self.response_count = data.get('responseCount')
        self.response_count_threshold = data.get('responseCountThreshold')
        self.use_emergency_device = data.get('useEmergencyDevice')
        self.description = data.get('description')
        criteria = data.get('criteria')
        self.criteria = SubscriptionCriteriaReference(criteria) if criteria else None
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None

    @property
    def observers(self):
        url = self.build_url(self._endpoints.get('observers'))
        observers = self.con.get(url).get('observers', {}).get('data')
        return [Role(role) for role in observers] if observers else []

    @property
    def supervisors(self):
        url = self.build_url(self._endpoints.get('supervisors'))
        supervisors = self.con.get(url).get('supervisors', {})
        return Pagination(self, supervisors, Person) if supervisors.get('data') else []

    def get_members(self):
        url = self.build_url(self._endpoints.get('get_members'))
        data = self.con.get(url)
        return Pagination(self, data, Person) if data.get('data') else None

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()


