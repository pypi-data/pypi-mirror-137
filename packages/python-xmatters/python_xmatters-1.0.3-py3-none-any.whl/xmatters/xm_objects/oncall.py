import xmatters.utils as util
import xmatters.factories
from xmatters.xm_objects.common import SelfLink, Pagination
from xmatters.connection import ApiBridge
from xmatters.xm_objects.shifts import GroupReference, Shift


class Replacer(ApiBridge):
    def __init__(self, parent, data):
        super(Replacer, self).__init__(parent, data)
        self.id = data.get('id')
        self.target_name = data.get('targetName')
        self.recipient_type = data.get('recipientType')
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None
        self.first_name = data.get('firstName')
        self.last_name = data.get('lastName')
        self.status = data.get('status')

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.target_name)

    def __str__(self):
        return self.__repr__()


class ShiftOccurrenceMember(ApiBridge):
    def __init__(self, parent, data):
        super(ShiftOccurrenceMember, self).__init__(parent, data)
        member = data.get('member')
        self.member = xmatters.factories.RecipientFactory.compose(self, member) if member else None
        self.position = data.get('position')
        self.delay = data.get('delay')
        self.escalation_type = data.get('escalationType')
        replacements = data.get('replacements', {})
        self.replacements = Pagination(self, replacements, TemporaryReplacement) if replacements.get('data') else []

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.member.target_name)

    def __str__(self):
        return self.__repr__()


class ShiftReference(ApiBridge):
    def __init__(self, parent, data):
        super(ShiftReference, self).__init__(parent, data)
        self.id = data.get('id')
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None
        self.name = data.get('name')

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.__repr__()


class TemporaryReplacement(ApiBridge):
    def __init__(self, parent, data):
        super(TemporaryReplacement, self).__init__(parent, data)
        start = data.get('start')
        self.start = util.TimeAttribute(start) if start else None
        end = data.get('end')
        self.end = util.TimeAttribute(end) if end else None
        replacement = data.get('replacement')
        self.replacement = TemporaryReplacement(self, replacement) if replacement else None


class OnCall(ApiBridge):
    def __init__(self, parent, data):
        super(OnCall, self).__init__(parent)
        # save shift self link for use with 'shift' property to return full Shift object (not just ShiftReference)
        self._shift_link = data.get('shift', {}).get('links', {}).get('self')
        group = data.get('group')
        self.group = GroupReference(parent, group) if group else None
        start = data.get('start')
        self.start = util.TimeAttribute(start) if start else None
        end = data.get('end')
        self.end = util.TimeAttribute(end) if end else None
        members = data.get('members', {})
        self.members = Pagination(self, members, ShiftOccurrenceMember) if members.get('data') else []

    @property
    def shift(self):
        if self._shift_link:
            url = '{}{}'.format(self.con.instance_url, self._shift_link)
            data = self.con.get(url)
            return Shift(self, data) if data else None
        else:
            return None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
