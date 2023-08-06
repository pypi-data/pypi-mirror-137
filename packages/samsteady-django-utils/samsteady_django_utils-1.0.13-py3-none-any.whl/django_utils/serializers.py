from functools import wraps

from django_utils.fields import BigIntStrRepr, BigIntStrReprSerializerField, JsonFieldSerializerField
from django_utils.mock_request import MockRequest
from global_requests import get_thread_user
from guardian_queryset.serializers import ValidateForeignKeyUserMixin, AssignActiveUserDefaultPermissionMixin
from rest_framework import serializers
from reversable_primary_key.serializers import CreatedSerializerMixin
from jsonfield import JSONField


class BigIntStrReprSerializerMixin(serializers.Serializer):

    @property
    def serializer_field_mapping(self):
        mapping = super().serializer_field_mapping.copy()
        mapping[BigIntStrRepr] = BigIntStrReprSerializerField
        return mapping

class JsonFieldSerializerMixin(serializers.Serializer):
    @property
    def serializer_field_mapping(self):
        mapping = super().serializer_field_mapping.copy()
        mapping[JSONField] = JsonFieldSerializerField
        return mapping

class WithMockRequesterSerializerMixin(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "request" not in self._context:
            user = get_thread_user()
            self._context["request"] = MockRequest(user)


class RequireAllFieldsSerializerMixin(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        not_required_fields = []
        if hasattr(self.Meta, "not_required_fields"):
            not_required_fields = self.Meta.not_required_fields
        if not hasattr(self.Meta, "extra_kwargs"):
            self.Meta.extra_kwargs = {}
        fields_dict = self.get_fields()
        for name in fields_dict:
            value = fields_dict[name]
            if name not in not_required_fields and not value.read_only:
                if name not in self.Meta.extra_kwargs:
                    self.Meta.extra_kwargs[name] = {}
                self.Meta.extra_kwargs[name]["required"] = True
                self.Meta.extra_kwargs[name]["allow_null"] = False

class AddUserMixin(ValidateForeignKeyUserMixin):
    def validate(self, data):
        data = super(AddUserMixin, self).validate(data)
        current_user = self.context['request'].user
        return {
            **data,
            'user': current_user
        }

class IsValidExceptionSerializerMixin(serializers.Serializer):

    def is_valid(self, **kwargs):
        return super().is_valid(**{
            'raise_exception': True,
            **kwargs,
        })

class DefaultPrivateModelSerializer(AddUserMixin,
                                    AssignActiveUserDefaultPermissionMixin,
                                    IsValidExceptionSerializerMixin,
                                    CreatedSerializerMixin,
                                    ValidateForeignKeyUserMixin,
                                    BigIntStrReprSerializerMixin,
                                    WithMockRequesterSerializerMixin,
                                    serializers.ModelSerializer):
    pass

def with_serializer(
        fields=None,
        exclude=None,
        model=None,
        base=DefaultPrivateModelSerializer,
        serializer_class=None,
        meta={},
        serializer_fields = {},
        many_write=False,
        update=False,
        pass_only=False,
        validate=True,
):

    class OnTheFlySerializer(base):
        class Meta:
            pass
        setattr(Meta, "model", model)
        if fields:
            setattr(Meta, "fields", fields)
        if exclude:
            setattr(Meta, "exclude", exclude)

        for k in meta.keys():
            setattr(Meta, k, meta[k])

    for k in serializer_fields.keys():
        setattr(OnTheFlySerializer, k, serializer_fields[k])

    effective_serializer_cls = serializer_class or OnTheFlySerializer
    def decorator(func):
        @wraps(func)
        def wrapped_func(self, request, *args, **kwargs):
            if request.method == 'GET' or pass_only:
                return func(self, request, *args, serializer_class=effective_serializer_cls, **kwargs)
            elif update:
                context = self.get_serializer_context()
                class UpdateSerializer(effective_serializer_cls):
                    def __init__(self, instance, *args, **kwargs):
                        super().__init__(instance, *args, data=request.data, context=context, **kwargs)
                # def do_serialized_update(instance, *args, **kwargs):
                #     serializer =effective_serializer_cls(instance, *args, data=request.data, context=self.get_serializer_context(), **kwargs)
                #     serializer.is_valid()
                #     serializer.save()
                return func(self, request, *args, **kwargs, serializer_class=UpdateSerializer)
            else:
                serializer = effective_serializer_cls(data=request.data, context=self.get_serializer_context(), many=many_write)
                validate and serializer.is_valid()
                return func(self, request, *args, serializer=serializer, **kwargs)
        return wrapped_func
    return decorator

class ReadWriteSerializerMixin(object):
    """
    Overrides get_serializer_class to choose the read serializer
    for GET requests and the write serializer for POST requests.

    Set read_serializer_class and write_serializer_class attributes on a
    viewset.
    """

    read_serializer_class = None
    write_serializer_class = None

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return self.get_write_serializer_class()
        return self.get_read_serializer_class()

    def get_read_serializer_class(self):
        assert self.read_serializer_class is not None, (
                "'%s' should either include a `read_serializer_class` attribute,"
                "or override the `get_read_serializer_class()` method."
                % self.__class__.__name__
        )
        return self.read_serializer_class

    def get_write_serializer_class(self):
        assert self.write_serializer_class is not None, (
                "'%s' should either include a `write_serializer_class` attribute,"
                "or override the `get_write_serializer_class()` method."
                % self.__class__.__name__
        )
        return self.write_serializer_class