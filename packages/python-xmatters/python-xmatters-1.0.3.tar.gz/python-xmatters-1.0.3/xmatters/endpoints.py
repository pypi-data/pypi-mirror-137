import xmatters.factories as factory
import xmatters.xm_objects.forms
from xmatters.connection import ApiBridge
from xmatters.xm_objects.common import Pagination
from xmatters.xm_objects.conference_bridges import ConferenceBridge
from xmatters.xm_objects.device_types import DeviceTypes
from xmatters.xm_objects.dynamic_teams import DynamicTeam
from xmatters.xm_objects.event_supressions import EventSuppression
from xmatters.xm_objects.events import Event
from xmatters.xm_objects.groups import Group
from xmatters.xm_objects.import_jobs import Import
from xmatters.xm_objects.incidents import Incident
from xmatters.xm_objects.oncall import OnCall
from xmatters.xm_objects.oncall_summary import OnCallSummary
from xmatters.xm_objects.people import Person
from xmatters.xm_objects.plans import Plan
from xmatters.xm_objects.roles import Role
from xmatters.xm_objects.scenarios import Scenario
from xmatters.xm_objects.services import Service
from xmatters.xm_objects.sites import Site
from xmatters.xm_objects.subscription_forms import SubscriptionForm
from xmatters.xm_objects.subscriptions import Subscription
from xmatters.xm_objects.temporary_absences import TemporaryAbsence


class AuditsEndpoint(ApiBridge):
    """ Used to interact with '/audit' endpoint """

    def __init__(self, parent):
        """
        :param parent: XMSession instance
        :type parent: :class:`xmatters.session.XMSession`
        """
        super(AuditsEndpoint, self).__init__(parent)

        self._endpoints = {'get_audit': '/audits'}

    # TODO: update docstring
    def get_audit(self, event_id=None, audit_type=None, sort_order=None, at_time=None, from_time=None, to_time=None,
                  after_time=None, before_time=None, offset=None, limit=None):
        """
        Perform an audit on a specified event id.

        See `xMatters REST API Reference <https://help.xmatters.com/xmapi/>`_ for valid parameters.

        :param event_id: xMatters event id
        :type event_id: str
        :param audit_type: Comma-separated list of audit types
        :type audit_type: str or list, optional
        :param sort_order: Sort order of the results
        :type sort_order: str, optional
        :return: list of audit objects
        :rtype: list
        """
        params = {'eventId': event_id,
                  'auditType': audit_type,
                  'sortOrder': sort_order,
                  'at': self.process_time_param(at_time),
                  'from': self.process_time_param(from_time),
                  'to': self.process_time_param(to_time),
                  'after': self.process_time_param(after_time),
                  'before': self.process_time_param(before_time),
                  'offset': offset,
                  'limit': limit}
        url = self.build_url(self._endpoints.get('get_audit'))
        data = self.con.get(url=url, params=params)
        return Pagination(self, data, xmatters.factories.AuditFactory, limit=limit) if data.get('data') else []

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class DevicesEndpoint(ApiBridge):
    """ Used to interact with '/devices' endpoint """
    _endpoints = {'get_devices': '/devices',
                  'get_device_by_id': '/devices/{device_id}'}

    def __init__(self, parent):
        """
        :param parent: XMSession instance
        :type parent: :class:`xmatters.session.XMSession`
        """
        super(DevicesEndpoint, self).__init__(parent)

    def get_devices(self, device_status=None, device_type=None, device_names=None, phone_number_format=None,
                    offset=None, limit=None):
        params = {'deviceStatus': device_status,
                  'deviceType': device_type,
                  'phoneNumberFormat': phone_number_format,
                  'deviceNames': device_names,
                  'offset': offset,
                  'limit': limit}
        url = self.build_url(self._endpoints.get('get_devices'))
        data = self.con.get(url=url, params=params)
        return Pagination(self, data, xmatters.factories.DeviceFactory, limit=limit) if data.get('data') else []

    def get_device_by_id(self, device_id, at_time=None):
        params = {'at': self.process_time_param(at_time)}
        url = self.build_url(self._endpoints.get('get_device_by_id').format(device_id=device_id))
        data = self.con.get(url=url, params=params)
        return xmatters.factories.DeviceFactory.compose(self, data) if data else None

    def create_device(self, data):
        url = self.build_url(self._endpoints.get('get_devices'))
        data = self.con.post(url, data=data)
        return xmatters.factories.DeviceFactory.compose(self, data) if data else None

    def update_device(self, data):
        url = self.build_url(self._endpoints.get('get_devices'))
        data = self.con.post(url=url, data=data)
        return xmatters.factories.DeviceFactory.compose(self, data) if data else None

    def delete_device(self, device_id):
        url = self.build_url(self._endpoints.get('get_device_by_id').format(device_id=device_id))
        data = self.con.delete(url=url)
        return xmatters.factories.DeviceFactory.compose(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class DeviceNamesEndpoint(ApiBridge):
    _endpoints = {'get_device_names': '/device-names',
                  'delete_device_name': '/device-names/{device_name_id}'}

    def __init__(self, parent):
        super(DeviceNamesEndpoint, self).__init__(parent)

    # TODO: Test params
    def get_device_names(self, device_types=None, search=None, sort_by=None, sort_order=None,
                         at_time=None, offset=None, limit=None):
        params = {'search': ' '.join(search) if search else None,
                  'sortBy': sort_by,
                  'sortOrder': sort_order,
                  'deviceTypes': device_types,
                  'at': self.process_time_param(at_time),
                  'offset': offset,
                  'limit': limit}
        url = self.build_url(self._endpoints.get('get_device_names'))
        data = self.con.get(url=url, params=params)
        return Pagination(self, data, factory.DeviceNameFactory, limit=limit) if data.get('data') else []

    def create_device_name(self, data):
        url = self.build_url(self._endpoints.get('get_device_names'))
        data = self.con.post(url, data=data)
        return xmatters.factories.DeviceNameFactory.compose(self, data) if data else None

    def update_device_name(self, data):
        url = self.build_url(self._endpoints.get('get_device_names'))
        data = self.con.post(url, data=data)
        return xmatters.factories.DeviceNameFactory.compose(self, data) if data else None

    def delete_device_name(self, device_name_id):
        url = self.build_url(self._endpoints.get('delete_device_name').format(device_name_id=device_name_id))
        data = self.con.delete(url)
        return xmatters.factories.DeviceNameFactory.compose(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class DeviceTypesEndpoint(ApiBridge):
    _endpoints = {'get_device_types': '/device-types'}

    def __init__(self, parent):
        super(DeviceTypesEndpoint, self).__init__(parent)

    def get_device_types(self):
        url = self.build_url(self._endpoints.get('get_device_types'))
        data = self.con.get(url)
        return DeviceTypes(data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class DynamicTeamsEndpoint(ApiBridge):
    _endpoints = {'get_dynamic_teams': '/dynamic-teams',
                  'get_dynamic_team_by_id': '/dynamic-teams/{dynamic_team_id}'}

    # TODO: Test params
    def get_dynamic_teams(self, search=None, operand=None, fields=None, supervisors=None, sort_by=None,
                          sort_order=None, offset=None, limit=None):
        params = {'search': ' '.join(search) if search else None,
                  'operand': operand,
                  'fields': fields,
                  'supervisors': supervisors,
                  'sortBy': sort_by,
                  'sortOrder': sort_order,
                  'offset': offset,
                  'limit': limit}
        url = self.build_url(self._endpoints.get('get_dynamic_teams'))
        data = self.con.get(url, params)
        return Pagination(self, data, DynamicTeam, limit=limit) if data.get('data') else []

    def get_dynamic_team_by_id(self, dynamic_team_id):
        url = self.build_url(self._endpoints.get('get_dynamic_team_by_id').format(dynamic_team_id=dynamic_team_id))
        data = self.con.get(url)
        return DynamicTeam(self, data) if data else None

    # TODO: Test
    def create_dynamic_team(self, data):
        url = self.build_url(self._endpoints.get('get_dynamic_teams'))
        data = self.con.post(url, data=data)
        return DynamicTeam(self, data) if data else None

    # TODO: Test
    def update_dynamic_team(self, data):
        url = self.build_url(self._endpoints.get('get_dynamic_teams'))
        data = self.con.post(url, data=data)
        return DynamicTeam(self, data) if data else None

    # TODO: Test
    def delete_dynamic_team(self, dynamic_team_id):
        url = self.build_url(self._endpoints.get('get_dynamic_team_by_id').format(dynamic_team_id=dynamic_team_id))
        data = self.con.delete(url=url)
        return DynamicTeam(self, data) if data else None

    def __init__(self, parent):
        super(DynamicTeamsEndpoint, self).__init__(parent)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class EventsEndpoint(ApiBridge):
    _endpoints = {'get_events': '/events',
                  'get_event_by_id': '/events/{event_id}',
                  'trigger_event': '{instance_url}/api/integration/1/functions/{func_id}/triggers'}

    def __init__(self, parent):
        super(EventsEndpoint, self).__init__(parent)

    # TODO: Test params
    def get_events(self, property_name=None, property_value=None, property_value_operator=None, status=None,
                   priority=None, plan=None, form=None, request_id=None, event_type=None, sort_by=None, sort_order=None,
                   submitter_id=None, search=None, targeted_recipients=None, resolved_users=None, from_time=None,
                   to_time=None, at_time=None, after_time=None, before_time=None, offset=None, limit=None):
        params = {'propertyName': property_name,
                  'propertyValue': property_value,
                  'propertyValueOperator': property_value_operator,
                  'status': status,
                  'priority': priority,
                  'plan': plan,
                  'form': form,
                  'requestId': request_id,
                  'eventType': event_type,
                  'sortBy': sort_by,
                  'sortOrder': sort_order,
                  'submitterid': submitter_id,
                  'search': ' '.join(search) if search else None,
                  'targetedRecipients': targeted_recipients,
                  'resolvedUsers': resolved_users,
                  'from': self.process_time_param(from_time),
                  'to': self.process_time_param(to_time),
                  'at': self.process_time_param(at_time),
                  'after': self.process_time_param(after_time),
                  'before': self.process_time_param(before_time),
                  'offset': offset,
                  'limit': limit}
        url = self.build_url(self._endpoints.get('get_events'))
        data = self.con.get(url, params)
        return Pagination(self, data, Event, limit=limit) if data.get('data') else []

    # TODO: Test params
    def get_event_by_id(self, event_id, at=None):
        params = {'at': self.process_time_param(at)}
        url = self.build_url(self._endpoints.get('get_event_by_id').format(event_id=event_id))
        data = self.con.get(url, params)
        return Event(self, data) if data else None

    # TODO
    # def trigger_event(self, function_id, data, params=None):
    #     url = self._endpoints.get('trigger_event').format(instance_url=self.con.instance_url, func_id=function_id)
    #     data = self.con.post(url, data=data, params=params)
    #     return RequestReference(data) if data else None

    # TODO: Test
    def change_event_status(self, data):
        url = self.build_url(self._endpoints.get('get_events'))
        data = self.con.post(url, data=data)
        return Event(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class EventSuppressionsEndpoint(ApiBridge):
    _endpoints = {'get_event_suppressions_by_event_id': '/event-suppressions?event={event_id}'}

    def __init__(self, parent):
        super(EventSuppressionsEndpoint, self).__init__(parent)

    def get_suppressions_by_event_id(self, event_id, sort_by, sort_order, offset=None, limit=None):
        params = {'sortBy': sort_by,
                  'sortOrder': sort_order,
                  'offset': offset,
                  'limit': limit}
        url = self.build_url(self._endpoints.get('get_event_suppressions_by_event_id').format(event_id))
        data = self.con.get(url, params)
        return Pagination(self, data, EventSuppression, limit=limit) if data.get('data') else []

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ConferenceBridgesEndpoint(ApiBridge):
    _endpoints = {'get_conference_bridges': '/conference-bridges',
                  'get_conference_bridge_by_id': '/conference-bridges/{bridge_id}'}

    def __init__(self, parent):
        super(ConferenceBridgesEndpoint, self).__init__(parent)

    # TODO: Test params
    def get_conference_bridges(self, name=None, description=None, toll_number=None, toll_free_number=None,
                               preferred_connection_type=None, pause_before_bridge_prompt=None,
                               static_bridge_number=False, bridge_number=None, dial_after_bridge=None, offset=None,
                               limit=None):
        params = {'name': name,
                  'description': description,
                  'tollNumber': toll_number,
                  'tollFreeNumber': toll_free_number,
                  'preferredConnectionType': preferred_connection_type,
                  'pauseBeforeBridgePrompt': pause_before_bridge_prompt,
                  'staticBridgeNumber': static_bridge_number,
                  'bridgeNumber': bridge_number,
                  'dialAfterBridge': dial_after_bridge,
                  'offset': offset,
                  'limit': limit}
        url = self.build_url(self._endpoints.get('get_conference_bridges'))
        data = self.con.get(url, params)
        return Pagination(self, data, ConferenceBridge, limit=limit) if data.get('data') else []

    def get_conference_bridge_by_id(self, bridge_id):
        url = self.build_url(self._endpoints.get('get_conference_bridge_by_id').format(bridge_id=bridge_id))
        data = self.con.get(url)
        return ConferenceBridge(self, data) if data else None

    def create_conference_bridge(self, data):
        url = self.build_url(self._endpoints.get('get_conference_bridges'))
        data = self.con.post(url, data=data)
        return ConferenceBridge(self, data) if data else None

    def update_conference_bridge(self, data):
        url = self.build_url(self._endpoints.get('get_conference_bridges'))
        data = self.con.post(url, data=data)
        return ConferenceBridge(self, data) if data else None

    def delete_conference_bridge(self, bridge_id):
        url = self.build_url(self._endpoints.get('get_conference_bridge_by_id').format(bridge_id=bridge_id))
        data = self.con.delete(url=url)
        return ConferenceBridge(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class FormsEndpoint(ApiBridge):
    _endpoints = {'get_forms': '/forms',
                  'get_form_by_id': '/forms/{form_id}'}

    def __init__(self, parent):
        super(FormsEndpoint, self).__init__(parent)

    # TODO: Test params
    def get_forms(self, search=None, operand=None, fields=None, enabled_for=None, plan_type=None, sort_by=None,
                  sort_order=None, trigger_type=None, offset=None, limit=None):
        params = {'search': ' '.join(search) if search else None,
                  'operand': operand,
                  'fields': fields,
                  'enabledFor': enabled_for,
                  'plans.planType': plan_type,
                  'sortBy': sort_by,
                  'sortOrder': sort_order,
                  'triggerType': trigger_type,
                  'offset': offset,
                  'limit': limit}

        url = self.build_url(self._endpoints.get('get_forms'))
        data = self.con.get(url, params=params)
        return Pagination(self, data, xmatters.xm_objects.forms.Form, limit=limit) if data.get('data') else []

    # TODO: Test
    def get_form_by_id(self, form_id):
        url = self.build_url(self._endpoints.get('get_form_by_id').format(form_id=form_id))
        data = self.con.get(url)
        return xmatters.xm_objects.forms.Form(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class GroupsEndpoint(ApiBridge):
    _endpoints = {'get_groups': '/groups',
                  'get_group_by_id': '/groups/{group_id}'}

    def __init__(self, parent):
        super(GroupsEndpoint, self).__init__(parent)

    # TODO: Test params
    def get_groups(self, search=None, operand=None, fields=None, sites=None, members=None, members_exists=None,
                   sort_by=None, sort_order=None, status=None, supervisors=None, offset=None, limit=None):
        params = {'search': ' '.join(search) if search else None,
                  'operand': operand,
                  'fields': fields,
                  'sites': sites,
                  'members': members,
                  'members.exists': members_exists,
                  'sortBy': sort_by,
                  'sortOrder': sort_order,
                  'status': status,
                  'supervisors': supervisors,
                  'offset': offset,
                  'limit': limit}

        url = self.build_url(self._endpoints.get('get_groups'))
        data = self.con.get(url, params=params)
        return Pagination(self, data, Group) if data.get('data') else []

    def get_group_by_id(self, group_id, at=None):
        params = {'at': self.process_time_param(at)}
        url = self.build_url(self._endpoints.get('get_group_by_id').format(group_id=group_id))
        data = self.con.get(url, params=params)
        return Group(self, data) if data else None

    # TODO: Test
    def create_group(self, data):
        url = self.build_url(self._endpoints.get('get_groups'))
        data = self.con.post(url, data=data)
        return Group(self, data) if data else None

    # TODO: Test
    def update_group(self, data):
        url = self.build_url(self._endpoints.get('get_groups'))
        data = self.con.post(url, data=data)
        return Group(self, data) if data else None

    # TODO: Test
    def delete_group(self, group_id):
        url = self.build_url(self._endpoints.get('get_group_by_id').format(group_id=group_id))
        data = self.con.delete(url)
        return Group(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ImportJobsEndpoint(ApiBridge):
    _endpoints = {'get_import_jobs': '/imports',
                  'get_import_job_by_id': '/imports/{import_id}'}

    def __init__(self, parent):
        super(ImportJobsEndpoint, self).__init__(parent)

    # TODO: Test params
    def get_import_jobs(self, transform_type=None, sort_by=None, sort_order=None):
        params = {'transformType': transform_type,
                  'sortBy': sort_by,
                  'sortOrder': sort_order}

        url = self.build_url(self._endpoints.get('get_import_jobs'))
        data = self.con.get(url, params=params).get('data', {})
        return [Import(self, job) for job in data] if data else []

    # TODO: Test
    def get_import_job_by_id(self, import_id):
        url = self.build_url(self._endpoints.get('get_import_job_by_id').format(import_id=import_id))
        data = self.con.get(url)
        return Import(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class IncidentsEndpoint(ApiBridge):
    _endpoints = {'get_incidents': '/incidents',
                  'get_incident_by_id': '/incidents/{incident_id}'}

    def __init__(self, parent):
        super(IncidentsEndpoint, self).__init__(parent)

    def get_incidents(self, request_id=None, search=None, operand=None, fields=None, sites=None, status=None,
                      severity=None, offset=None, limit=None):
        params = {'requestId': request_id,
                  'search': ' '.join(search) if search else None,
                  'operand': operand,
                  'fields': fields,
                  'sites': sites,
                  'status': status,
                  'severity': severity,
                  'offset': offset,
                  'limit': limit}

        url = self.build_url(self._endpoints.get('get_incidents'))
        data = self.con.get(url, params=params)
        return Pagination(self, data, Incident, limit=limit) if data.get('data') else []

    # TODO: Test
    def get_incident_by_id(self, incident_id):
        url = self.build_url(self._endpoints.get('get_incident_by_id').format(incident_id=incident_id))
        data = self.con.get(url)
        return Incident(self, data) if data else None

    # TODO
    # def trigger_incident(self, data, params=None):
    #     url = self._endpoints.get('trigger_incident').format(instance_url=self.con.instance_url)
    #     data = self.con.post(url, data=data, params=params)
    #     return RequestReference(data) if data else None

    # TODO: Test
    def update_incident(self, incident_id, data):
        url = self.build_url(self._endpoints.get('get_incident_by_id').format(incident_id=incident_id))
        data = self.con.post(url, data=data)
        return Incident(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class OnCallEndpoint(ApiBridge):
    _endpoints = {'get_oncall': '/on-call'}

    def __init__(self, parent):
        super(OnCallEndpoint, self).__init__(parent)

    # TODO: Test params
    def get_oncall(self, groups, members_per_shift=None, at_time=None, from_time=None, to_time=None, offset=None,
                   limit=None):
        params = {'groups': groups,
                  'membersPerShift': members_per_shift,
                  'at': self.process_time_param(at_time),
                  'from': self.process_time_param(from_time),
                  'to': self.process_time_param(to_time),
                  'offset': offset,
                  'limit': limit}
        url = self.build_url(self._endpoints.get('get_oncall'))
        data = self.con.get(url, params=params)
        return Pagination(self, data, OnCall, limit=limit) if data.get('data') else []

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class OnCallSummaryEndpoint(ApiBridge):
    _endpoints = {'get_oncall_summary': '/on-call-summary'}

    def __init__(self, parent):
        super(OnCallSummaryEndpoint, self).__init__(parent)

    # TODO: Test params
    def get_oncall_summary(self, groups, escalation_order=None, recipients_per_shift=None, at=None):
        params = {'groups': groups,
                  'escalationOrder': escalation_order,
                  'recipientsPerShift': recipients_per_shift,
                  'at': self.process_time_param(at)}

        url = self.build_url(self._endpoints.get('get_oncall_summary'))
        data = self.con.get(url, params=params)
        return [OnCallSummary(self, summary) for summary in data] if data else []

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class PeopleEndpoint(ApiBridge):
    _endpoints = {'get_people': '/people',
                  'get_person_by_id': '/people/{person_id}'}

    def __init__(self, parent):
        super(PeopleEndpoint, self).__init__(parent)

    # TODO: Test params
    def get_people(self, search=None, operand=None, fields=None, property_names=None, property_values=None,
                   devices_exist=None, devices_test_status=None, site=None, status=None, supervisors_exists=None,
                   groups=None, groups_exist=None, roles=None, supervisors=None, created_from_time=None,
                   created_to_time=None, created_before_time=None, created_after_time=None, sort_by=None,
                   sort_order=None, at_time=None, limit=None):
        params = {'search': ' '.join(search) if search else None,
                  'operand': operand,
                  'fields': fields,
                  'propertyNames': property_names,
                  'propertyValues': property_values,
                  'devices.exists': devices_exist,
                  'devices.testStatus': devices_test_status,
                  'site': site,
                  'status': status,
                  'supervisors.exists': supervisors_exists,
                  'groups': groups,
                  'groups.exists': groups_exist,
                  'roles': roles,
                  'supervisors': supervisors,
                  'createdFrom': self.process_time_param(created_from_time),
                  'createdTo': self.process_time_param(created_to_time),
                  'createdBefore': self.process_time_param(created_before_time),
                  'createdAfter': self.process_time_param(created_after_time),
                  'sortBy': sort_by,
                  'sortOrder': sort_order,
                  'at': self.process_time_param(at_time),
                  'limit': limit}
        url = self.build_url(self._endpoints.get('get_people'))
        data = self.con.get(url, params=params)
        return Pagination(self, data, Person, limit=limit) if data.get('data') else []

    def get_person_by_id(self, person_id, params=None):
        url = self.build_url(self._endpoints.get('get_person_by_id').format(person_id=person_id))
        data = self.con.get(url, params)
        return Person(self, data) if data else None

    def get_people_by_query(self, first_name=None, last_name=None, target_name=None, web_login=None, phone_number=None,
                            email_address=None, offset=None, limit=None):
        if all(p is None for p in (first_name, last_name, target_name, web_login, phone_number, email_address)):
            raise ValueError('must assign a parameter to query by')
        params = {'firstName': first_name,
                  'lastName': last_name,
                  'targetName': target_name,
                  'webLogin': web_login,
                  'phoneNumber': phone_number,
                  'emailAddress': email_address,
                  'offset': offset,
                  'limit': limit}
        url = self.build_url(self._endpoints.get('get_people'))
        data = self.con.get(url, params=params)
        return Pagination(self, data, Person, limit=limit) if data.get('data') else []

    def create_person(self, data):
        url = self.build_url(self._endpoints.get('get_people'))
        data = self.con.post(url, data=data)
        return Person(self, data) if data else None

    def update_person(self, data):
        url = self.build_url(self._endpoints.get('get_people'))
        data = self.con.post(url, data=data)
        return Person(self, data) if data else None

    def delete_person(self, person_id):
        url = self.build_url(self._endpoints.get('get_person_by_id').format(person_id=person_id))
        data = self.con.delete(url)
        return Person(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class PlansEndpoint(ApiBridge):
    _endpoints = {'get_plans': '/plans',
                  'get_plan_by_id': '/plans/{plan_id}'}

    def __init__(self, parent):
        super(PlansEndpoint, self).__init__(parent)

    # TODO: Test params
    def get_plans(self, plan_type=None, enabled=None, enabled_for=None, search=None, operand=None, fields=None,
                  sort_by=None, sort_order=None, subscription_forms=None, at=None, offset=None, limit=None):
        params = {'planType': plan_type,
                  'enabled': enabled,
                  'enabledFor': enabled_for,
                  'search': ' '.join(search) if search else None,
                  'operand': operand,
                  'fields': fields,
                  'sortBy': sort_by,
                  'sortOrder': sort_order,
                  'subscription-forms': subscription_forms,
                  'at': self.process_time_param(at),
                  'offset': offset,
                  'limit': limit}
        url = self.build_url(self._endpoints.get('get_plans'))
        data = self.con.get(url, params=params)
        return Pagination(self, data, Plan, limit=limit) if data.get('data') else []

    def get_plan_by_id(self, plan_id, at=None):
        params = {'at': self.process_time_param(at)}
        url = self.build_url(self._endpoints.get('get_plan_by_id').format(person_id=plan_id))
        data = self.con.get(url, params=params)
        return Plan(self, data) if data else None

    # TODO: Test
    def create_plan(self, data):
        url = self.build_url(self._endpoints.get('get_plans'))
        data = self.con.post(url, data=data)
        return Plan(self, data) if data else None

    # TODO: Test
    def update_plan(self, data):
        url = self.build_url(self._endpoints.get('get_plans'))
        data = self.con.post(url, data=data)
        return Plan(self, data) if data else None

    # TODO: Test
    def delete_plan(self, plan_id):
        url = self.build_url(self._endpoints.get('get_plan_by_id').format(plan_id=plan_id))
        data = self.con.delete(url)
        return Plan(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class RolesEndpoint(ApiBridge):
    _endpoints = {'get_roles': '/roles'}

    def __init__(self, parent):
        super(RolesEndpoint, self).__init__(parent)

    # TODO: Test params
    def get_roles(self, name=None, allow_wildcards=None, offset=None, limit=None):
        params = {'name': name,
                  'allowWildcards': allow_wildcards,
                  'offset': offset,
                  'limit': limit}
        url = self.build_url(self._endpoints.get('get_roles'))
        data = self.con.get(url, params=params)
        return Pagination(self, data, Role, limit=limit) if data.get('data') else []

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ScenariosEndpoint(ApiBridge):
    _endpoints = {'get_scenarios': '/scenarios',
                  'get_scenario_by_id': '/scenarios/{scenario_id}'}

    def __init__(self, parent):
        super(ScenariosEndpoint, self).__init__(parent)

    # TODO: Test params
    def get_scenarios(self, search=None, operand=None, enabled_for=None, offset=None, limit=None):
        params = {'search': ' '.join(search) if search else None,
                  'operand': operand,
                  'enabledFor': enabled_for,
                  'offset': offset,
                  'limit': limit}
        url = self.build_url(self._endpoints.get('get_scenarios'))
        data = self.con.get(url, params=params)
        return Pagination(self, data, Scenario, limit=limit) if data.get('data') else []

    def get_scenario_by_id(self, scenario_id):
        url = self.build_url(self._endpoints.get('get_scenario_by_id').format(scenario_id=scenario_id))
        data = self.con.get(url)
        return Scenario(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ServicesEndpoint(ApiBridge):
    _endpoints = {'get_services': '/services',
                  'get_service_by_id': '/scenarios/{service_id}'}

    def __init__(self, parent):
        super(ServicesEndpoint, self).__init__(parent)

    # TODO: Test params
    def get_services(self, search=None, operand=None, fields=None, owned_by=None, offset=None, limit=None):
        params = {'search': ' '.join(search) if search else None,
                  'operand': operand,
                  'fields': fields,
                  'ownedBy': owned_by,
                  'offset': offset,
                  'limit': limit}
        url = self.build_url(self._endpoints.get('get_services'))
        data = self.con.get(url, params)
        return Pagination(self, data, Service, limit=limit) if data.get('data') else []

    def get_service_by_id(self, service_id):
        url = self.build_url(self._endpoints.get('get_service_by_id').format(service_id=service_id))
        data = self.con.get(url)
        return Service(self, data) if data else None

    # TODO: Test
    def create_service(self, data):
        url = self.build_url(self._endpoints.get('get_services'))
        data = self.con.post(url, data=data)
        return Service(self, data) if data else None

    # TODO: Test
    def update_service(self, data):
        url = self.build_url(self._endpoints.get('get_services'))
        data = self.con.post(url, data=data)
        return Service(self, data) if data else None

    # TODO: Test
    def delete_service(self, service_id):
        url = self.build_url(self._endpoints.get('get_service_by_id').format(service_id=service_id))
        data = self.con.delete(url)
        return Service(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class SitesEndpoint(ApiBridge):
    _endpoints = {'get_sites': '/sites',
                  'get_site_by_id': '/sites/{site_id}'}

    def __init__(self, parent):
        super(SitesEndpoint, self).__init__(parent)

    # TODO: Test params
    def get_sites(self, search=None, operand=None, fields=None, sort_by=None, sort_order=None, country=None,
                  geocoded=None, status=None, offset=None, limit=None):
        params = {'search': ' '.join(search) if search else None,
                  'operand': operand,
                  'fields': fields,
                  'sortBy': sort_by,
                  'sortOrder': sort_order,
                  'country': country,
                  'geocoded': geocoded,
                  'status': status,
                  'offset': offset,
                  'limit': limit}
        url = self.build_url(self._endpoints.get('get_sites'))
        data = self.con.get(url, params)
        return Pagination(self, data, Site, limit=limit) if data.get('data') else []

    def get_site_by_id(self, site_id, params=None):
        url = self.build_url(self._endpoints.get('get_site_by_id').format(site_id=site_id))
        data = self.con.get(url, params)
        return Site(self, data) if data else None

    # TODO: Test
    def create_site(self, data):
        url = self.build_url(self._endpoints.get('get_sites'))
        data = self.con.post(url, data=data)
        return Site(self, data) if data else None

    # TODO: Test
    def update_site(self, data):
        url = self.build_url(self._endpoints.get('get_sites'))
        data = self.con.post(url, data=data)
        return Site(self, data) if data else None

    # TODO: Test
    def delete_site(self, site_id):
        url = self.build_url(self._endpoints.get('get_site_by_id').format(site_id=site_id))
        data = self.con.delete(url)
        return Site(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class SubscriptionsEndpoint(ApiBridge):
    _endpoints = {'get_subscriptions': '/subscriptions',
                  'get_subscription_by_id': '/subscription-forms/{sub_id}',
                  'get_subscribers': '/subscribers',
                  'unsubscribe_person': '/subscribers/{person_id}'}

    def __init__(self, parent):
        super(SubscriptionsEndpoint, self).__init__(parent)

    # TODO: Test params
    def get_subscriptions(self, owner=None, subscriber=None, shared_with=None, managed_by=None, subscription_name=None,
                          subscription_description=None, subscription_form=None, offset=None, limit=None):
        params = {'owner': owner,
                  'subscriber': subscriber,
                  'sharedWith': shared_with,
                  'managedBy': managed_by,
                  'subscriptionName': subscription_name,
                  'subscriptionDescription': subscription_description,
                  'subscriptionForm': subscription_form,
                  'offset': offset,
                  'limit': limit}
        url = self.build_url(self._endpoints.get('get_subscriptions'))
        data = self.con.get(url, params=params)
        return Pagination(self, data, Subscription, limit=limit) if data else []

    def get_subscription_by_id(self, subscription_id):
        url = self.build_url(self._endpoints.get('get_subscription_by_id').format(sub_id=subscription_id))
        data = self.con.get(url)
        return SubscriptionForm(self, data) if data else None

    # TODO: Test
    def get_subscribers(self, subscription_id, offset=None, limit=None):
        params = {'id': subscription_id,
                  'offset': offset,
                  'limit': limit}
        url = self.build_url(self._endpoints.get('get_subscribers'))
        subscribers = self.con.get(url, params=params)
        return Pagination(self, subscribers, Person, limit=limit) if subscribers.get('data') else []

    # TODO: Test
    def unsubscribe_person(self, person_id):
        url = self.build_url(self._endpoints.get('unsubscribe_person').format(person_id=person_id))
        data = self.con.delete(url)
        return Subscription(self, data) if data else None

    # TODO: Test
    def create_subscription(self, data):
        url = self.build_url(self._endpoints.get('get_subscriptions'))
        data = self.con.post(url, data=data)
        return Subscription(self, data) if data else None

    # TODO: Test
    def update_subscription(self, data):
        url = self.build_url(self._endpoints.get('get_subscriptions'))
        data = self.con.post(url, data=data)
        return Subscription(self, data) if data else None

    # TODO: Test
    def delete_subscription(self, subscription_id):
        url = self.build_url(self._endpoints.get('get_subscription_by_id').format(sub_id=subscription_id))
        data = self.con.delete(url)
        return Subscription(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class SubscriptionFormsEndpoint(ApiBridge):
    _endpoints = {'get_subscription_forms': '/subscription-forms',
                  'get_subscription_form_id': '/subscription-forms/{sub_form_id}'}

    def __init__(self, parent):
        super(SubscriptionFormsEndpoint, self).__init__(parent)

    # TODO: Test params
    def get_subscription_forms(self, sort_by=None, sort_order=None, offset=None, limit=None):
        params = {'sortBy': sort_by,
                  'sortOrder': sort_order,
                  'offset': offset,
                  'limit': limit}
        url = self.build_url(self._endpoints.get('get_subscription_forms'))
        data = self.con.get(url, params=params)
        return Pagination(self, data, SubscriptionForm, limit=limit) if data.get('data') else []

    def get_subscription_form_by_id(self, sub_form_id):
        url = self.build_url(self._endpoints.get('get_subscription_form_by_id').format(sub_form_id=sub_form_id))
        data = self.con.get(url)
        return SubscriptionForm(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class TemporaryAbsencesEndpoint(ApiBridge):
    _endpoints = {'get_temporary_absences': '/temporary-absences',
                  'delete_temporary_absence': '/temporary-absences/{temp_abs_id}'}

    def __init__(self, parent):
        super(TemporaryAbsencesEndpoint, self).__init__(parent)

    # TODO: Test params
    def get_temporary_absences(self, member=None, groups=None, absence_type=None, from_time=None, to_time=None,
                               offset=None, limit=None):
        params = {'member': member,
                  'groups': groups,
                  'absenceType': absence_type,
                  'from': self.process_time_param(from_time),
                  'to': self.process_time_param(to_time),
                  'offset': offset,
                  'limit': limit}
        url = self.build_url(self._endpoints.get('get_temporary_absences'))
        data = self.con.get(url, params)
        return Pagination(self, data, TemporaryAbsence, limit=limit) if data.get('data') else []

    # TODO: Test
    def create_temporary_absence(self, data):
        url = self.build_url(self._endpoints.get('get_temporary_absences'))
        data = self.con.post(url, data=data)
        return TemporaryAbsence(self, data) if data else None

    # TODO: Test
    def delete_temporary_absence(self, temporary_absence_id):
        url = self.build_url(self._endpoints.get('delete_temporary_absence').format(temp_abs_id=temporary_absence_id))
        data = self.con.delete(url)
        return TemporaryAbsence(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


# TODO
class UploadUsersEndpoint(ApiBridge):
    _endpoints = {'upload_user_upload_file': '/uploads/users-v1',
                  'upload_epic_zipsync_file': '/uploads/epic-v1'}

    def __init__(self, parent):
        super(UploadUsersEndpoint, self).__init__(parent)

    def upload_user_upload_file(self, file_path):
        pass

    def upload_epic_zipsync_file(self, file_path):
        pass

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
