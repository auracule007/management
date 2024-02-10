from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    page_size = 10

class CoursesPagination(PageNumberPagination):
    page_size = 5

class CategoryPagination(PageNumberPagination):
    page_size = 5