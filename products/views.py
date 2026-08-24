from django.db.models import Sum, F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from products.models import Category, Products
from products.serializers import CategorySerializer, ProductSerializer



# Category ViewSet: Only has GET endpoint
# Items will be added from the database
class CategoryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'category', 'price']


    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


    @action(detail=False, methods=['get'], url_path='total-value')
    def get_total_value(self, request):
        total_value = Products.objects.aggregate(total_value=Sum(F('price')) * F('stock'))
        return Response({'total_value': total_value['total_value']})

    @action(detail=True, methods=['get'], url_path='max-price')
    def get_max_price(self, request, pk=None):
        max_price = Products.objects.filter(id=pk).aggregate(max_price=Sum(F('price') * F('stock')))
        return Response({'max_price': max_price['max_price']})