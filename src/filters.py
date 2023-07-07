from django_filters import rest_framework as filters

from . import models


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    is_top = filters.BooleanFilter(field_name='is_top')

    class Meta:
        model = models.Product
        fields = ('min_price', 'max_price', 'is_top')
