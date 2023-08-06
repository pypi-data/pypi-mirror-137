import xmatters.utils as util
from xmatters.xm_objects.common import Recipient
from xmatters.xm_objects.people import PersonReference
from xmatters.connection import ApiBridge
import xmatters.xm_objects.events as events


class Notification(ApiBridge):
    def __init__(self, parent, data):
        super(Notification, self).__init__(parent, data)
        self.id = data.get('id')
        self.category = data.get('category')
        recipient = data.get('recipient')
        self.recipient = Recipient(parent, recipient) if recipient else None
        self.delivery_status = data.get('deliveryStatus')
        created = data.get('created')
        self.created = util.TimeAttribute(created) if created else None
        event = data.get('event')
        self.event = events.EventReference(parent, event) if event else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Response(ApiBridge):
    def __init__(self, parent, data):
        super(Response, self).__init__(parent, data)
        self.comment = data.get('comment')
        notification = data.get('notification')
        self.notification = Notification(self, notification) if notification else None
        options = data.get('options', {}).get('data')
        self.options = [events.ResponseOption(r) for r in options] if options else None
        self.source = data.get('source')
        received = data.get('received')
        self.received = util.TimeAttribute(received) if received else None
        self.response = data.get('response')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class AuditBase(ApiBridge):
    def __init__(self, parent, data):
        super(AuditBase, self).__init__(parent, data)
        self.id = data.get('id')
        self.type = data.get('type')
        self.order_id = data.get('orderId')
        at = data.get('at')
        self.at = util.TimeAttribute(at) if at else None

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.type)

    def __str__(self):
        return self.__repr__()


class Audit(AuditBase):
    def __init__(self, parent, data):
        super(Audit, self).__init__(parent, data)

        event = data.get('event')
        self.event = events.EventReference(parent, event) if event else None

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.type)

    def __str__(self):
        return self.__repr__()


class Annotation(ApiBridge):
    def __init__(self, parent, data):
        super(Annotation, self).__init__(parent, data)
        event = data.get('event')
        self.event = events.EventReference(parent, event) if event else None
        author = data.get('author')
        self.author = PersonReference(parent, author) if author else None
        self.comment = data.get('comment')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class AuditNotification(AuditBase):
    def __init__(self, parent, data):
        super(AuditNotification, self).__init__(parent, data)
        notification = data.get('notification')
        self.notification = Notification(self, notification) if notification else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class AuditAnnotation(AuditBase):
    def __init__(self, parent, data):
        super(AuditAnnotation, self).__init__(parent, data)
        annotation = data.get('annotation')
        self.annotation = Annotation(self, annotation) if annotation else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class AuditResponse(AuditBase):
    def __init__(self, parent, data):
        super(AuditResponse, self).__init__(parent, data)
        response = data.get('response')
        self.response = Response(self, response) if response else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
