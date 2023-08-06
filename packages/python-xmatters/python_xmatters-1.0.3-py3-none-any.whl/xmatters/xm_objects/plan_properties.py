class Property(object):
    def __init__(self, data):
        self.id = data.get('id')
        self.property_type = data.get('propertyType')
        self.name = data.get('name')
        self.description = data.get('description')
        self.help_text = data.get('helpText')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Boolean(Property):
    def __init__(self, data):
        super(Boolean, self).__init__(data)
        self.default = data.get('default')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Hierarchy(Property):
    def __init__(self, data):
        super(Hierarchy, self).__init__(data)
        self.default = data.get('default')
        self.delimiter = data.get('delimiter')
        self.categories = data.get('categories', [])
        self.paths = data.get('paths', [])

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class MultLinkSelectList(Property):
    def __init__(self, data):
        super(MultLinkSelectList, self).__init__(data)
        self.items = data.get('items', [])

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class SingleSelectList(Property):
    def __init__(self, data):
        super(SingleSelectList, self).__init__(data)
        self.items = data.get('items', [])

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Number(Property):
    def __init__(self, data):
        super(Number, self).__init__(data)
        self.default = data.get('default')
        self.max_length = data.get('maxLength')
        self.min_length = data.get('minLength')
        self.units = data.get('units')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Password(Property):
    def __init__(self, data):
        super(Password, self).__init__(data)
        self.max_length = data.get('maxLength')
        self.min_length = data.get('minLength')
        self.pattern = data.get('pattern')
        self.validate = data.get('validate')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class Text(Property):
    def __init__(self, data):
        super(Text, self).__init__(data)
        self.max_length = data.get('maxLength')
        self.min_length = data.get('minLength')
        self.pattern = data.get('pattern')
        self.validate = data.get('validate')

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
