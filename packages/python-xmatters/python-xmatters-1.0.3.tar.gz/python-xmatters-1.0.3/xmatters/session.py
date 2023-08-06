import urllib.parse

import xmatters.auth
import xmatters.connection
import xmatters.endpoints


class XMSession(object):
    """ Primary class used to interact with xMatters API """

    def __init__(self, base_url, **kwargs):
        """
        :param base_url: xMatters instance url or xMatters instance base url
        :type base_url: str
        """
        p_url = urllib.parse.urlparse(base_url)
        instance_url = 'https://{}'.format(p_url.netloc) if p_url.netloc else 'https://{}'.format(p_url.path)
        self._base_url = '{}/api/xm/1'.format(instance_url)
        self.con = None
        self._kwargs = kwargs

    def set_authentication(self, username=None, password=None, client_id=None, token=None, token_storage=None):
        """
        Set authentication method to use.
            If client_id is provided, it is assumed OAuth2 authentication is desired;
            otherwise basic authentication is used.
        :param username: xMatters username
        :type username: str, optional
        :param password: xMatters password
        :type password: str, optional
        :param client_id: xMatters instance client id
        :type client_id: str, optional
        :param token: xMatters token object or refresh token
        :type token: dict or str, optional
        :param token_storage: Class instance used to store token returned during a refresh.
            Any class instance will be accepted as long as it has "read_token" and "write_token" methods.
        :type token_storage: :class:`xmatters.utils.TokenFileStorage`, optional
        :return: self
        :rtype: :class:`xmatters.session.XMSession`
        """
        timeout = self._kwargs.get('timeout')
        max_retries = self._kwargs.get('max_retries')
        if client_id:
            self.con = xmatters.auth.OAuth2Auth(self._base_url, client_id, token, username, password, token_storage,
                                                timeout=timeout,
                                                max_retries=max_retries)
        elif None not in (username, password):
            self.con = xmatters.auth.BasicAuth(self._base_url, username, password, timeout=timeout,
                                               max_retries=max_retries)
        else:
            raise ValueError('unable to determine authentication method')

        return self

    def audits(self):
        return xmatters.endpoints.AuditsEndpoint(self)

    def conference_bridges(self):
        return xmatters.endpoints.ConferenceBridgesEndpoint(self)

    def device_names(self):
        return xmatters.endpoints.DeviceNamesEndpoint(self)

    def device_types(self):
        return xmatters.endpoints.DeviceTypesEndpoint(self)

    def devices(self):
        return xmatters.endpoints.DevicesEndpoint(self)

    def dynamic_teams(self):
        return xmatters.endpoints.DynamicTeamsEndpoint(self)

    def events(self):
        return xmatters.endpoints.EventsEndpoint(self)

    def event_suppressions(self):
        return xmatters.endpoints.EventSuppressionsEndpoint(self)

    def forms(self):
        return xmatters.endpoints.FormsEndpoint(self)

    def import_jobs(self):
        return xmatters.endpoints.ImportJobsEndpoint(self)

    def groups(self):
        return xmatters.endpoints.GroupsEndpoint(self)

    def incidents(self):
        return xmatters.endpoints.IncidentsEndpoint(self)

    def oncall(self):
        return xmatters.endpoints.OnCallEndpoint(self)

    def oncall_summary(self):
        return xmatters.endpoints.OnCallSummaryEndpoint(self)

    def people(self):
        return xmatters.endpoints.PeopleEndpoint(self)

    def plans(self):
        return xmatters.endpoints.PlansEndpoint(self)

    def roles(self):
        return xmatters.endpoints.RolesEndpoint(self)

    def scenarios(self):
        return xmatters.endpoints.ScenariosEndpoint(self)

    def services(self):
        return xmatters.endpoints.ServicesEndpoint(self)

    def sites(self):
        return xmatters.endpoints.SitesEndpoint(self)

    def subscriptions(self):
        return xmatters.endpoints.SubscriptionsEndpoint(self)

    def subscription_forms(self):
        return xmatters.endpoints.SubscriptionFormsEndpoint(self)

    def temporary_absences(self):
        return xmatters.endpoints.TemporaryAbsencesEndpoint(self)

    # TODO
    # def upload_users(self):
    #     return xmatters.endpoints.UploadUsersEndpoint(self)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
