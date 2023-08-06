from rest_framework.filters import SearchFilter, OrderingFilter, BaseFilterBackend

class UserFilterForgiving(BaseFilterBackend):
    """
    A filter backend that limits results to those where they are the foreign key 'user'
    """

    def filter_queryset(self, request, queryset, view):
        try:
            return queryset.filter(user=request.user)
        except:
            return queryset

class WithCreatedSearchFilter(SearchFilter):

    def get_search_terms(self, request):
        original_terms = super().get_search_terms(request)
        if "created" in original_terms:
            original_terms.remove("created")
            original_terms.append("id")
        return original_terms

class WithCreatedOrderingFilter(OrderingFilter):

    def get_ordering(self, request, queryset, view):
        params = request.query_params.get(self.ordering_param)
        if params:
            fields = [param.strip() for param in params.split(',')]
            if "created" in fields:
                fields[fields.index("created")] = "id"
            if "-created" in fields:
                fields[fields.index("-created")] = "-id"
            ordering = self.remove_invalid_fields(queryset, fields, view, request)
            if ordering:
                return ordering


class OnTheFlySearchFilter(WithCreatedSearchFilter):

    def filter_queryset(self, request, queryset, search_fields=None, serializer_class=None):

        class DummyView:
            pass

        if search_fields:
            setattr(DummyView, "search_fields", search_fields)

        if serializer_class:
            setattr(DummyView, "get_serializer_class", lambda self: serializer_class)

        return super().filter_queryset(request, queryset, DummyView)

class OnTheFlyOrderingFilter(WithCreatedOrderingFilter):

    def filter_queryset(self, request, queryset, ordering_fields=None, ordering=None, serializer_class=None):

        class DummyView:
            pass

        if ordering_fields:
            setattr(DummyView, "ordering_fields", ordering_fields)

        if ordering:
            setattr(DummyView, "ordering", ordering)

        if serializer_class:
            setattr(DummyView, "get_serializer_class", lambda self: serializer_class)

        return super().filter_queryset(request, queryset, DummyView)
