from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class EndlessPagination(PageNumberPagination):
    page_size = 20

    def __init__(self):
        super().__init__()
        self.has_next_page = False

    #分好页的queryset
    def paginate_queryset(self, queryset, request, view=None):
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        if 'created_at__gt' in request.query_params:
            created_at__gt = request.query_params['created_at__gt']
            queryset = queryset.filter(created_at__gt = created_at__gt)
            self.has_next_page = False
            return queryset.order_by('-created_at')

        if 'created_at__lt' in request.query_params:
            created_at__lt = request.query_params['created_at__lt']
            queryset = queryset.filter(created_at__lt = created_at__lt)

        queryset = queryset.order_by('-created_at')[:page_size + 1]
        self.has_next_page = (len(queryset) > page_size)
        return queryset[:self.page_size]

    def get_paginated_response(self, data):
        return Response({
            'has_next_page': self.has_next_page,
            'results': data,
        })
