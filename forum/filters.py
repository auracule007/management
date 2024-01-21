from django.db.models import Q
from django_filters import filters as filtering
from django_filters.rest_framework import FilterSet

from .models import *


class ForumQuestionFilter(FilterSet):
    title = filtering.CharFilter(method="filter_by_title")

    class Meta:
        model = ForumQuestion
        fields = ["title"]

    @classmethod
    def filter_by_title(cls, queryset, name, value):
        names = value.strip().split(",")
        return (
            queryset.filter(title__icontains=names)
            .select_related("user", "course")
            .distinct()
        )
