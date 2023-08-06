# When the _meta object was formalized, this exception was moved to
# django.core.exceptions. It is retained here for backwards compatibility
# purposes.
# from primary_key import make_id

import json

from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
# When the _meta object was formalized, this exception was moved to
# django.core.exceptions. It is retained here for backwards compatibility
# purposes.
from django.db import connection
from django.db import models
from django.db.models import IntegerField
from django.utils.functional import cached_property
from rest_framework import serializers


class StringArrayField(models.CharField):
    description = "A string array field that automatically dumps and loads between json and string for db storage."

    def get_db_prep_value(self, value, *args, **kwargs):
        if value is None:
            return None
        return json.dumps(value)

    def to_python(self, value):
        try:
            return json.loads(value)
        except Exception as e:
            raise ValidationError(e)

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)


class BigIntStrReprSerializerField(serializers.IntegerField):
    def to_internal_value(self, data):
        if isinstance(data, str) and len(data) > self.MAX_STRING_LENGTH:
            self.fail('max_string_length')

        try:
            data = self.re_decimal.sub('', str(data))
        except (ValueError, TypeError):
            self.fail('invalid')
        return data

    def to_representation(self, value):
        if value is None:
            return None
        return str(value)

class JsonFieldSerializerField(serializers.Field):

    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        return data

class IntStrMinValueValidator(MinValueValidator):
    def compare(self, a, b):
        return int(a) < int(b)


class IntStrMaxValueValidator(MaxValueValidator):
    def compare(self, a, b):
        return int(a) > int(b)

class BigIntStrRepr(models.BigIntegerField):
    description = "A Big Integer field that gets converted to a string for python / serialization use."

    @cached_property
    def validators(self):
        # These validators can't be added at field initialization time since
        # they're based on values retrieved from `connection`.
        validators_ = super(IntegerField, self).validators
        internal_type = self.get_internal_type()
        min_value, max_value = connection.ops.integer_field_range(internal_type)
        if min_value is not None and not any(
                (
                        isinstance(validator, validators.MinValueValidator) and (
                        validator.limit_value()
                        if callable(validator.limit_value)
                        else validator.limit_value
                ) >= min_value
                ) for validator in validators_
        ):
            validators_.append(IntStrMinValueValidator(min_value))
        if max_value is not None and not any(
                (
                        isinstance(validator, validators.MaxValueValidator) and (
                        validator.limit_value()
                        if callable(validator.limit_value)
                        else validator.limit_value
                ) <= max_value
                ) for validator in validators_
        ):
            validators_.append(IntStrMaxValueValidator(max_value))
        return validators_

    def get_db_prep_value(self, value, *args, **kwargs):
        if value is None:
            return None
        elif isinstance(value, str):
            try:
                return int(value)
            except Exception as e:
                raise ValidationError(e)
        else:
            return value

    def to_python(self, value):
        if value is None:
            return None
        try:
            return str(value)
        except Exception as e:
            raise ValidationError(e)

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)

    def to_representation(self, value):
        if value is None:
            return None
        return str(value)

