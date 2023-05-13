from rest_framework.views import Response
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 4

    def get_paginated_response(self, data):
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "total-objects": self.page.paginator.count,
                "total-pages": self.page.paginator.num_pages,
                "results": data,
            }
        )
