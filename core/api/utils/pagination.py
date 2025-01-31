from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response ({
            'total': self.page.paginator.count,
            'per_page': self.get_page_size(self.request),
            'current_page': self.page.number,
            'last_page': self.page.paginator.num_pages,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })