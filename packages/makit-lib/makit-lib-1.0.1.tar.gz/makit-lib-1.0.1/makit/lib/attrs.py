#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: LiangChao
@email：liangchao@noboauto.com
@desc: 
"""
import re

from makit.lib import validate
from makit.lib.validate import ValidateError


class Attr:
    def __init__(self, default=None, converter=None, validators=None, change=None, none=True, assign_once=False):
        self.default = default
        self.value = None
        self._converters = []
        self._validators = []
        self._change = change
        self._converter = converter
        self.allow_none = none
        self._assign_once = assign_once
        if validators:
            self.add_validator(validators)

    def __get__(self, instance, owner):
        self.instance = instance
        return self.value

    def __set__(self, instance, value):
        self.instance = instance
        value = self.convert(value)
        self.validate(value)
        changed = self.value == value
        old, self.value = self.value, value
        if changed and self._change:
            self._change(self.instance, old, value)  # 触发值改变事件

    def validate(self, value):
        if self.allow_none and value is None:
            return
        errors = []
        if not self.allow_none and value is None:
            errors.append(f'{value} should not None!')
        else:
            for validator in self._validators:
                try:
                    if isinstance(validator, Validator):
                        validator.validate(value, self)
                    else:
                        validator(value, self)
                except Exception as e:
                    errors.append(str(e))
        if errors:
            raise ValidateError(self.instance, self, errors)

    def convert(self, value):
        if self._converter:
            return self._converter(value)
        return value

    def add_validator(self, validator):
        if isinstance(validator, list):
            self._validators.extend(validator)
        elif callable(validator) or isinstance(validator, Validator):
            self._validators.append(validator)
        else:
            raise InvalidValidatorError(self.instance, self, validator)


class StringAttr(Attr):
    def __init__(self, default=None, none=True, validators=None,
                 prefix=None, suffix=None, options=None,
                 pattern=None, assign_once=False, converter=None):
        super().__init__(
            default=default,
            none=none,
            validators=validators,
            converter=converter,
            assign_once=assign_once
        )
        if prefix:
            self._validators.append(lambda v: v.startswith(prefix))
        if suffix:
            self._validators.append(lambda v: v.endswith(prefix))
        if options and isinstance(options, (list, tuple)):
            self._validators.append(lambda v: v in options)
        if pattern:
            self._validators.append(lambda v: re.match(pattern, v) is not None)


class IntAttr(Attr):
    def __init__(self, default=0, none=False, validators=None,
                 converter=None,
                 min=None, max=None):
        validators = (validators or []).append(lambda v: validate.check_int(v, min=min, max=max, raise_error=True))
        super().__init__(default=default, none=none, validators=validators, converter=converter)

    def validate(self, value):
        if not isinstance(value, int):
            raise ValidateError(f'{value} is not int!')
        super().validate(value)


class FloatAttr(Attr):
    def __init__(self, default=0.0, none=False, validators=None, converter=None):
        super().__init__(
            default=default,
            none=none,
            validators=validators,
            converter=converter
        )

    def __set__(self, instance, value):
        Attr.__set__(self, instance, value)

    def validate(self, value):
        if not isinstance(value, float):
            raise ValidateError(f'{value} is not float!')
        super().validate(value)


class NumberAttr(Attr):
    def __init__(self, default=None, none=True, validators=None, converter=None):
        validators = (validators or []).append()
        super().__init__(
            default=default,
            none=none,
            validators=validators,
            converter=converter
        )


class Bool(Attr):
    def __init__(self, none=False, validator=None, **kwargs):
        validator = (validator or []).append(lambda v: none is True or isinstance(v, bool))
        super().__init__(none=none, validator=validator, **kwargs)


class Type(Attr):
    def __init__(self, value_type, **kwargs):
        super().__init__(**kwargs)


# region validators

class Validator:
    def validate(self, value, attr):
        raise NotImplementedError


def not_none(value, attr):
    return value is not None


# endregion

class InvalidValidatorError(Exception):
    def __init__(self, model, attr, validator):
        self.model = model
        self.attr = attr
        self.validator = validator
