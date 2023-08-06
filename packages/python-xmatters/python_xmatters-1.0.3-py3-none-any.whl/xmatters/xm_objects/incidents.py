import xmatters.utils as utils
from xmatters.xm_objects.common import SelfLink
from xmatters.xm_objects.people import PersonReference
from xmatters.connection import ApiBridge


class IncidentProperty(object):

    def __init__(self, data):
        self.name = data.get('name')
        self.level = data.get('level')

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()


class Incident(ApiBridge):
    _endpoints = {'add_timeline_note': '/timeline-entries'}

    def __init__(self, parent, data):
        super(Incident, self).__init__(parent, data)
        self.id = data.get('id')
        self.incident_identifier = data.get('incidentIdentifier')
        self.summary = data.get('summary')
        self.description = data.get('description')
        severity = data.get('severity')
        self.severity = IncidentProperty(severity) if severity else None
        status = data.get('status')
        self.status = IncidentProperty(status) if status else None
        initiated_by = data.get('initiatedBy')
        self.initiated_by = PersonReference(self, initiated_by) if initiated_by else None
        commander = data.get('commander')
        self.commander = PersonReference(self, commander) if commander else None
        self.request_id = data.get('requestId')
        self.impacted_services = data.get('impactedServices')
        reporter = data.get('reporter')
        self.reporter = PersonReference(self, reporter) if reporter else None
        created_at = data.get('createdAt')
        self.created_at = utils.TimeAttribute(created_at) if created_at else None
        updated_at = data.get('updated_at')
        self.updated_at = utils.TimeAttribute(updated_at) if updated_at else None
        acknowledged_at = data.get('acknowledgeAt')
        self.acknowledged_at = utils.TimeAttribute(acknowledged_at) if acknowledged_at else None
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None

    # TODO: Test
    def add_timeline_note(self, text):
        data = {'entryType': 'TIMELINE_NOTE',
                'text': text}
        url = self.build_url(self._endpoints.get('add_timeline_note'))
        data = self.con.post(url, data=data)
        return IncidentNote(self, data) if data else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class IncidentNote(ApiBridge):
    def __init__(self, parent, data):
        super(IncidentNote, self).__init__(parent, data)
        self.id = data.get('id')
        at = data.get('at')
        self.at = utils.TimeAttribute(at) if at else None
        self.entry_type = data.get('entryType')
        self.text = data.get('text')
        added_by = data.get('addedBy')
        self.added_dy = PersonReference(self, added_by) if added_by else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class IncidentDetails(object):
    def __init__(self, data):
        self.summary = data.get('summary')
        self.description = data.get('description')
        self.severity = data.get('severity')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
