import json
import pathlib
from abc import ABC, abstractmethod

from dateutil import tz, parser

MAX_API_LIMIT = 1000


class TimeAttribute(str):
    def datetime(self):
        """
        Create datetime object from str
        :return: datetime object with whichever timezone in str on creation (if present)
        :rtype: :class:`datetime.datetime`
        """
        return parser.isoparse(self)

    def isoformat(self):
        return self.datetime().isoformat()

    def datetime_local(self):
        """
        Create datetime object from str and adjust to local timezone
        :return: datetime object adjusted to local timezone
        :rtype: :class:`datetime.datetime`
        """
        return parser.isoparse(self).astimezone(tz.tzlocal())

    def isoformat_local(self):
        return self.datetime_local().isoformat()

    def datetime_utc(self):
        """
        Create datetime object from str and adjust to utc timezone.
        :return: datetime object adjusted to utc timezone
        :rtype: :class:`datetime.datetime`
        """
        return parser.isoparse(self).astimezone(tz.tzutc())

    def isoformat_utc(self):
        return self.datetime_utc().isoformat()

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self)


class TokenFileStorage(object):
    def __init__(self, token_filepath):
        if not isinstance(token_filepath, pathlib.Path):
            self.token_filepath = pathlib.Path(token_filepath)

    def read_token(self):
        if not self.token_filepath.is_file():
            return None
        else:
            with open(self.token_filepath, 'r') as f:
                return json.load(f)

    def write_token(self, token):
        with open(self.token_filepath, 'w') as f:
            json.dump(token, f, indent=4)

    @property
    def token(self):
        return self.read_token()

    @token.setter
    def token(self, token):
        self.write_token(token)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Factory(ABC):

    @property
    @abstractmethod
    def needs_parent(self):
        pass

    @property
    @abstractmethod
    def identifier_field(self):
        pass

    @property
    @abstractmethod
    def factory_objects(self):
        pass

    @classmethod
    def compose(cls, parent, item_data, default=None):
        identifier = item_data.get(cls.identifier_field)
        # noinspection PyUnresolvedReferences
        constructor = cls.factory_objects.get(identifier, default)

        if cls.needs_parent:
            return constructor(parent, item_data) if constructor else None
        else:
            return constructor(item_data) if constructor else None
