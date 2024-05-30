import django_filters
from .models import Activity


class ActivityFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter()
    name = django_filters.CharFilter(lookup_expr='iexact')
    description = django_filters.CharFilter(lookup_expr='eq')
    km_count = django_filters.NumberFilter()
    place = django_filters.CharFilter(lookup_expr='iexact')
    date = django_filters.DateFilter()

    class Meta:
        model = Activity
        fields = '__all__'
