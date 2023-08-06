import xmatters.xm_objects.events
import xmatters.xm_objects.forms
import xmatters.factories as factory
import xmatters.utils
import xmatters.connection
import xmatters.xm_objects.people
import xmatters.xm_objects.plans
import xmatters.xm_objects.roles

from xmatters.xm_objects.common import Pagination, SelfLink


class ScenarioPermission(xmatters.connection.ApiBridge):
    def __init__(self, parent, data):
        super(ScenarioPermission, self).__init__(parent, data)
        self.permissible_type = data.get('permissibleType')
        self.editor = data.get('editor')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ScenarioPermissionPerson(ScenarioPermission):
    def __init__(self, parent, data):
        super(ScenarioPermissionPerson, self).__init__(parent, data)
        person = data.get('person')
        self.person = xmatters.xm_objects.people.PersonReference(self, person) if person else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ScenarioPermissionRole(ScenarioPermission):
    def __init__(self, parent, data):
        super(ScenarioPermissionRole, self).__init__(parent, data)
        role = data.get('role')
        self.role = xmatters.xm_objects.roles.Role(role) if role else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Scenario(xmatters.connection.ApiBridge):
    _endpoints = {'properties': '?embed=properties',
                  'plan': '?embed=properties',
                  'form': '?embed=form',
                  'properties_translations': '?embed=properties.translations'}

    def __init__(self, parent, data):
        super(Scenario, self).__init__(parent, data)
        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')
        self.priority = data.get('priority')
        self.position = data.get('position')
        self.bypass_phone_intro = data.get('bypassPhoneIntro')
        self.escalation_override = data.get('escalationOverride')
        self.expiration_in_minutes = data.get('expirationInMinutes')
        self.override_device_restrictions = data.get('overrideDeviceRestrictions')
        self.require_phone_password = data.get('requirePhonePassword')
        sos = data.get('senderOverrides')
        self.sender_overrides = xmatters.xm_objects.forms.SenderOverrides(sos) if sos else None
        vm_opts = data.get('voicemailOptions')
        self.voicemail_options = xmatters.xm_objects.events.VoicemailOptions(vm_opts) if vm_opts else None
        tdns = data.get('targetDeviceNames', {})
        self.target_device_names = Pagination(self, tdns, factory.DeviceNameFactory) if tdns.get('data') else []
        created = data.get('created')
        self.created = xmatters.utils.TimeAttribute(created) if created else None
        perm = data.get('permitted', {}).get('data')
        self.permitted = [factory.ScenarioPermFactory.compose(self, p) for p in perm] if perm else []
        rs = data.get('recipients')
        self.recipients = Pagination(self, rs, factory.RecipientFactory) if rs.get('data') else []
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None

    @property
    def properties(self):
        url = self.build_url(self._endpoints.get('properties'))
        data = self.con.get(url)
        return data.get('properties', {})

    @property
    def plan(self):
        url = self.build_url(self._endpoints.get('plan'))
        plan = self.con.get(url).get('plan', {})
        return xmatters.xm_objects.plans.Plan(self, plan) if plan else None

    @property
    def form(self):
        url = self.build_url(self._endpoints.get('form'))
        form = self.con.get(url).get('form', {})
        return xmatters.xm_objects.forms.Form(self, form) if form else None

    @property
    def properties_translations(self):
        url = self.build_url(self._endpoints.get('properties_translations'))
        data = self.con.get(url)
        return data.get('properties', {})

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
