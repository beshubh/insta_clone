from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)

class PostLimitPagination(LimitOffsetPagination):
    max_limit = 20
    default_limit = 10
class PostPageNumberPagination(PageNumberPagination):
    page_size = 20

