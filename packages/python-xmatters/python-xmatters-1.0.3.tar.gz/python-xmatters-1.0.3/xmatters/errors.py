import xmatters.utils


class ErrorObject(object):
    """ xMatters Error common object"""

    def __init__(self, data):
        self.code = data.get('code')
        self.subcode = data.get('subcode')
        self.reason = data.get('reason')
        self.message = data.get('message')

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.code)

    def __str__(self):
        return self.__repr__()


class Error(Exception):
    pass


class XMSessionError(Error):
    def __init__(self, msg):
        super(XMSessionError, self).__init__(msg)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class AuthorizationError(Error):
    def __init__(self, msg):
        super(AuthorizationError, self).__init__(msg)


class ApiError(Error):
    def __init__(self, data):
        msg = ' '.join(['{}: {}'.format(k, v) for k, v in data.items()])
        super(ApiError, self).__init__(msg)


class NoContentError(ApiError):
    def __init__(self, data):
        super(NoContentError, self).__init__(data)


class BadRequestError(ApiError):
    def __init__(self, data):
        super(BadRequestError, self).__init__(data)


class UnauthorizedError(ApiError):
    def __init__(self, data):
        super(UnauthorizedError, self).__init__(data)


class ForbiddenError(ApiError):
    def __init__(self, data):
        super(ForbiddenError, self).__init__(data)


class NotFoundError(ApiError):
    def __init__(self, data):
        super(NotFoundError, self).__init__(data)


class NotAcceptableError(ApiError):
    def __init__(self, data):
        super(NotAcceptableError, self).__init__(data)


class ConflictError(ApiError):
    def __init__(self, data):
        super(ConflictError, self).__init__(data)


class UnsupportedMediaError(ApiError):
    def __init__(self, data):
        super(UnsupportedMediaError, self).__init__(data)


class TooManyRequestsError(ApiError):
    def __init__(self, data):
        super(TooManyRequestsError, self).__init__(data)


class ErrorFactory(xmatters.utils.Factory):
    needs_parent = False
    identifier_field = 'code'
    factory_objects = {204: NoContentError,
                       400: BadRequestError,
                       401: UnauthorizedError,
                       403: ForbiddenError,
                       404: NotFoundError,
                       406: NotAcceptableError,
                       409: ConflictError,
                       415: UnsupportedMediaError,
                       429: TooManyRequestsError}

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
