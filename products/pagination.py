from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class GuestLimitedPagination(PageNumberPagination):
    """
    Custom pagination used across the whole API:
    - Guests (unauthenticated): max 20 items per page
    - Authenticated users: up to 100 items per page
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    django_paginator_class = Paginator   # ✅ use the actual class, not a string

    def get_page_size(self, request):
        # Guests get locked to 20 max
        if not request.user.is_authenticated:
            return min(20, self.max_page_size)

        # Logged-in users can use ?page_size= up to 100
        if request.query_params.get(self.page_size_query_param):
            try:
                requested = int(request.query_params[self.page_size_query_param])
                return min(requested, self.max_page_size)
            except (TypeError, ValueError):
                pass

        return self.page_size

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'page_size': self.get_page_size(self.request),
            'results': data
        })
