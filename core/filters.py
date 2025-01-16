import django_filters
from django_filters import rest_framework as filters
from .models import Task

class TaskFilter(filters.FilterSet):
    title_exact = filters.CharFilter(field_name='title', lookup_expr='exact')
    title_icontains = filters.CharFilter(field_name='title', lookup_expr='icontains')
    status = filters.CharFilter(field_name='status', lookup_expr='exact')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')

    class Meta:
        model = Task
        fields = [
            'title_exact',
            'title_icontains',
            'status',
            'created_before',
            'created_after',
        ]