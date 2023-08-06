import xmatters.xm_objects.groups
import xmatters.xm_objects.audits
import xmatters.xm_objects.people
import xmatters.xm_objects.dynamic_teams
import xmatters.xm_objects.scenarios
import xmatters.xm_objects.device_names
import xmatters.xm_objects.plan_endpoints
import xmatters.xm_objects.plan_properties
import xmatters.xm_objects.forms
import xmatters.xm_objects.devices
import xmatters.utils


class DeviceFactory(xmatters.utils.Factory):
    needs_parent = True
    identifier_field = 'deviceType'
    factory_objects = {'EMAIL': xmatters.xm_objects.devices.EmailDevice,
                       'VOICE': xmatters.xm_objects.devices.VoiceDevice,
                       'TEXT_PHONE': xmatters.xm_objects.devices.SMSDevice,
                       'TEXT_PAGER': xmatters.xm_objects.devices.TextPagerDevice,
                       'APPLE_PUSH': xmatters.xm_objects.devices.ApplePushDevice,
                       'ANDROID_PUSH': xmatters.xm_objects.devices.AndroidPushDevice,
                       'FAX': xmatters.xm_objects.devices.FaxDevice,
                       'VOICE_IVR': xmatters.xm_objects.devices.PublicAddressDevice,
                       'GENERIC': xmatters.xm_objects.devices.GenericDevice}

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class RecipientFactory(xmatters.utils.Factory):
    needs_parent = True
    identifier_field = 'recipientType'
    factory_objects = {'GROUP': xmatters.xm_objects.groups.Group,
                       'PERSON': xmatters.xm_objects.people.Person,
                       'DEVICE': xmatters.xm_objects.devices.Device,
                       'DYNAMIC_TEAM': xmatters.xm_objects.dynamic_teams.DynamicTeam}

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class AuditFactory(xmatters.utils.Factory):
    needs_parent = True
    identifier_field = 'type'
    factory_objects = {'EVENT_ANNOTATED': xmatters.xm_objects.audits.AuditAnnotation,
                       'EVENT_CREATED': xmatters.xm_objects.audits.Audit,
                       'EVENT_SUSPENDED': xmatters.xm_objects.audits.Audit,
                       'EVENT_RESUMED': xmatters.xm_objects.audits.Audit,
                       'EVENT_COMPLETED': xmatters.xm_objects.audits.Audit,
                       'EVENT_TERMINATED': xmatters.xm_objects.audits.Audit,
                       'RESPONSE_RECEIVED': xmatters.xm_objects.audits.AuditResponse,
                       'NOTIFICATION_DELIVERED': xmatters.xm_objects.audits.AuditNotification,
                       'NOTIFICATION_FAILED': xmatters.xm_objects.audits.AuditNotification}

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class SectionFactory(xmatters.utils.Factory):
    needs_parent = True
    identifier_field = 'type'
    factory_objects = {'CONFERENCE_BRIDGE': xmatters.xm_objects.forms.ConferenceBridgeSection,
                       'CUSTOM_SECTION': xmatters.xm_objects.forms.CustomSectionItems,
                       'DEVICE_FILTER': xmatters.xm_objects.forms.DevicesSection,
                       'HANDLING_OPTIONS': xmatters.xm_objects.forms.HandlingSection,
                       'ATTACHMENTS': xmatters.xm_objects.forms.FormSection,
                       'SENDER_OVERRIDES': xmatters.xm_objects.forms.SenderOverridesSection,
                       'RECIPIENTS': xmatters.xm_objects.forms.RecipientsSection,
                       'RESPONSE_CHOICES': xmatters.xm_objects.forms.FormSection,
                       'INCIDENT': xmatters.xm_objects.forms.IncidentSection,
                       'DOCUMENT_UPLOAD': xmatters.xm_objects.forms.FormSection}

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class AuthFactory(xmatters.utils.Factory):
    needs_parent = False
    identifier_field = 'authenticationType'
    factory_objects = {'NO_AUTH': None,
                       'BASIC': xmatters.xm_objects.plan_endpoints.BasicAuthentication,
                       'OAUTH2': xmatters.xm_objects.plan_endpoints.OAuth2Authentication,
                       'OAUTH2_FORCE': xmatters.xm_objects.plan_endpoints.OAuth2Authentication,
                       'OAUTH_SLACK': xmatters.xm_objects.plan_endpoints.OAuth2Authentication,
                       'XMATTERS': xmatters.xm_objects.plan_endpoints.ServiceAuthentication,
                       'SERVICENOW': xmatters.xm_objects.plan_endpoints.ServiceAuthentication}

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class PropertiesFactory(xmatters.utils.Factory):
    needs_parent = False
    identifier_field = 'propertyType'
    factory_objects = {'BOOLEAN': xmatters.xm_objects.plan_properties.Boolean,
                       'HIERARCHY': xmatters.xm_objects.plan_properties.Hierarchy,
                       'LIST_TEXT_MULTI_SELECT': xmatters.xm_objects.plan_properties.MultLinkSelectList,
                       'LIST_TEXT_SINGLE_SELECT': xmatters.xm_objects.plan_properties.SingleSelectList,
                       'NUMBER': xmatters.xm_objects.plan_properties.Number,
                       'PASSWORD': xmatters.xm_objects.plan_properties.Password,
                       'TEXT': xmatters.xm_objects.plan_properties.Text}

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ScenarioPermFactory(xmatters.utils.Factory):
    needs_parent = True
    identifier_field = 'permissibleType'
    factory_objects = {'PERSON': xmatters.xm_objects.scenarios.ScenarioPermissionPerson,
                       'ROLE': xmatters.xm_objects.scenarios.ScenarioPermissionRole}

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class DeviceNameFactory(xmatters.utils.Factory):
    needs_parent = False
    identifier_field = 'deviceType'
    factory_objects = {
        'ANDROID_PUSH': xmatters.xm_objects.device_names.DeviceName,
        'APPLE_PUSH': xmatters.xm_objects.device_names.DeviceName,
        'EMAIL': xmatters.xm_objects.device_names.DeviceNameEmail,
        'FAX': xmatters.xm_objects.device_names.DeviceName,
        'GENERIC': xmatters.xm_objects.device_names.DeviceName,
        'TEXT_PAGER': xmatters.xm_objects.device_names.DeviceName,
        'TEXT_PHONE': xmatters.xm_objects.device_names.DeviceName,
        'VOICE': xmatters.xm_objects.device_names.DeviceName,
        'VOICE_IVR': xmatters.xm_objects.device_names.DeviceName}

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
