from flask_request_validator import AbstractRule
import re


class AbstractRuleWithCustomError(AbstractRule):
    def __init__(self, error=None):
        """
        :param str pattern:
        """
        self.error_message = error


class Pattern(AbstractRuleWithCustomError):

    def __init__(self, pattern, **kw):
        """
        :param str pattern:
        """
        self.pattern = re.compile(pattern)
        super(Pattern, self).__init__(**kw)

    def validate(self, value):
        errors = []
        if not self.pattern.search(value):
            if self.error_message is not None:
                errors.append(self.error_message)
            else:
                errors.append('Value "%s" does not match pattern %s' %
                              (value, self.pattern.pattern))
        return errors


class Enum(AbstractRuleWithCustomError):

    def __init__(self, *allowed_values, **kw):
        self.allowed_values = allowed_values
        super(Pattern, self).__init__(**kw)

    def validate(self, value):
        errors = []
        if value not in self.allowed_values:
            if self.error_message is not None:
                errors.append(self.error_message)
            else:
                errors.append('Incorrect value "%s". Allowed values: %s' %
                              (value, self.allowed_values))
        return errors


class MaxLength(AbstractRuleWithCustomError):

    def __init__(self, length, **kw):
        """
        :param int length:
        """
        self.length = length
        super(MaxLength, self).__init__(**kw)

    def validate(self, value):
        errors = []
        if len(value) > self.length:
            if self.error_message is not None:
                errors.append(self.error_message)
            else:
                errors.append('Invalid length for value "%s". Max length = %s' %
                              (value, self.length))
        return errors


class MinLength(AbstractRuleWithCustomError):

    def __init__(self, length, **kw):
        """
        :param int length:
        """
        self.length = length
        super(MinLength, self).__init__(**kw)

    def validate(self, value):
        errors = []
        if len(value) < self.length:
            if self.error_message is not None:
                errors.append(self.error_message)
            else:
                errors.append('Invalid length for value "%s". Min length = %s'
                              % (value, self.length))
        return errors
