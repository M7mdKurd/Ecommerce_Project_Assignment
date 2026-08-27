import django_filters

from products.models import Products


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Products
        fields = {
            'name'  :  ['icontains', 'iexact'],
            'price' :  ['exact', 'lt', 'gt', 'range'],
        }