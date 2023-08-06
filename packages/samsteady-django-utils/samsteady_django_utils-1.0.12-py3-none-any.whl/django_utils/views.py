from functools import wraps

from django.db import models
from django.db.models import QuerySet
from django.http import HttpResponse
from django_utils.filters import OnTheFlyOrderingFilter, OnTheFlySearchFilter, WithCreatedSearchFilter, \
    WithCreatedOrderingFilter
from django_utils.permissions import CustomObjectPermissions
from guardian_queryset.filters import GuardianViewPermissionsFilter
from rest_framework import mixins, generics
from rest_framework import status
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class DefaultPrivateApiViewMixin(generics.GenericAPIView):
    filter_backends = [WithCreatedOrderingFilter,WithCreatedSearchFilter,GuardianViewPermissionsFilter, filters.OrderingFilter]
    permission_classes = [CustomObjectPermissions]
    ordering = ['-id']


class DefaultPrivateViewSetMixin(DefaultPrivateApiViewMixin):


    def get_defaults(self):
        return {'user': self.request.user}

    def get_queryset(self):
        return self.queryset.filter(**self.get_defaults())

    def perform_create(self, serializer):
        serializer.save(**self.get_defaults())

class PaginatedListViewSetMixin(viewsets.GenericViewSet):

    def get_paginated_list_response(self, queryset, serializer_class=None):
        page = self.paginate_queryset(queryset)
        if page is not None:
            effective_queryset = page
        else:
            effective_queryset = queryset
        if serializer_class:
            context = self.get_serializer_context()
            serializer = serializer_class(effective_queryset, many=True, context=context)
        else:
            serializer = self.get_serializer(effective_queryset, many=True)
        return self.get_paginated_response(serializer.data)


def as_response(
        paginate=True,
        many=True,
        filter=True,
        filter_backends=None,
        filter_all_backends=False,
        order_fields=None,
        ordering=None,
        search_fields=None,
        serializer_class=None,
        status=status.HTTP_200_OK
):

    def decorator(func):
        _serializer_class = serializer_class
        @wraps(func)
        def wrapped_func(self, request, *args, **kwargs):
            serializer_class=kwargs["serializer_class"] if "serializer_class" in kwargs else None
            try:
                res = func(self, request, *args, **kwargs)
            except TypeError:
                kwargs.pop("serializer_class")
                res = func(self, request, *args, **kwargs)
            if isinstance(res, QuerySet) or isinstance(res, models.Model):
                querysetOrObj = res
            elif isinstance(res, HttpResponse):
                return res
            elif res is None:
                return Response(status=status)
            else:
                raise ValueError("Return value must be a QuerySet, HttpResponse or None")
            effective_serializer_class = _serializer_class or serializer_class or self.get_serializer_class()
            if isinstance(querysetOrObj, QuerySet):
                if filter_backends:
                    for backend in list(filter_backends):
                        querysetOrObj = backend().filter_queryset(self.request, querysetOrObj, self)
                    if filter_all_backends:
                        querysetOrObj = self.filter_queryset(querysetOrObj)
                elif filter:
                    querysetOrObj = self.filter_queryset(querysetOrObj)
                if ordering:
                    querysetOrObj = OnTheFlyOrderingFilter().filter_queryset(request, querysetOrObj, order_fields, ordering, effective_serializer_class)
                if search_fields:
                    querysetOrObj = OnTheFlySearchFilter().filter_queryset(request, querysetOrObj, search_fields, effective_serializer_class)
                if paginate:
                    return PaginatedListViewSetMixin.get_paginated_list_response(self, querysetOrObj, effective_serializer_class)
            context = self.get_serializer_context()
            serializer = effective_serializer_class(querysetOrObj, many=many, context=context)
            return Response(serializer.data)
        return wrapped_func
    return decorator

class NonUpdateModelViewset(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    pass
