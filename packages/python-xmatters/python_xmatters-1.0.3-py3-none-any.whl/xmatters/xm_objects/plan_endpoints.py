import xmatters.xm_objects.common
import xmatters.xm_objects.plans
from xmatters.connection import ApiBridge
import xmatters.factories


class ServiceAuthentication(object):
    def __init__(self, data):
        self.username = data.get('username')
        self.connection_status = data.get('connectionStatus')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class BasicAuthentication(object):
    def __init__(self, data):
        self.username = data.get('username')
        self.password = data.get('password')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class OAuth2Authentication(object):
    def __init__(self, data):
        self.username = data.get('username')
        self.oauth_token_url = data.get('oauthTokenUrl')
        self.oauth_client_id = data.get('oauthClientId')
        self.client_secret = data.get('client_secret')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Endpoint(ApiBridge):
    def __init__(self, parent, data):
        super(Endpoint, self).__init__(parent, data)
        self.id = data.get('id')
        plan = data.get('plan')
        self.plan = xmatters.xm_objects.plans.PlanReference(plan) if plan else None
        self.url = data.get('url')
        self.endpoint_type = data.get('endpointType')
        self.authentication_type = data.get('authenticationType')
        auth = data.get('authentication')
        self.authentication = xmatters.factories.AuthFactory.compose(self, data) if auth else None
        links = data.get('links')
        self.links = xmatters.xm_objects.common.SelfLink(self, data) if links else None
        self.trust_self_signed = data.get('trustSelfSigned')
        self.preemptive = data.get('preemptive')
        self.data = data.get('data')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
