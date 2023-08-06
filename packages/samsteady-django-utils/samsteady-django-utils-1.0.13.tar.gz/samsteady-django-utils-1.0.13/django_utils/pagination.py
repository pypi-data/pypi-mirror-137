from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('last_page', self.page.paginator.count),
            ('count', self.page.paginator.count),
            ('current', self.page.number),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
    def paginate_queryset(self, queryset, request, view=None):
        if 'no_page' in request.query_params:
            return None
        return super().paginate_queryset(queryset, request, view)