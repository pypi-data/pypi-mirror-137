from xmatters import factories as factory
from xmatters.connection import ApiBridge
from xmatters.xm_objects.oncall import ShiftReference
from xmatters.xm_objects.people import PersonReference
from xmatters.xm_objects.shifts import GroupReference


class OnCallSummary(ApiBridge):
    def __init__(self, parent, data):
        super(OnCallSummary, self).__init__(parent, data)
        group = data.get('group')
        self.group = GroupReference(self, group) if group else None
        shift = data.get('shift')
        self.shift = ShiftReference(self, shift) if shift else None
        recipient = data.get('recipient')
        self.recipient = factory.RecipientFactory.compose(self, recipient) if recipient else None
        absence = data.get('absence')
        self.absence = PersonReference(self, absence) if absence else None
        self.delay = data.get('delay')
        self.escalation_level = data.get('escalationLevel')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


